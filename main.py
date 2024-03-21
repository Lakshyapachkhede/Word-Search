import pygame
import random
from string import ascii_uppercase, ascii_lowercase
import sys
import linecache

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 601
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Search")

font = pygame.font.Font(r'E:\projects\games\wordSearch\font\comic\COMICSANS.ttf', 22) 
win_font = pygame.font.Font(r'E:\projects\games\wordSearch\font\comic\COMICSANS.ttf', 50)  
word_font = pygame.font.Font(r'E:\projects\games\wordSearch\font\comic\COMICSANS.ttf', 30)  

# Set up grid parameters
grid_size = 40  # Adjust the size of each grid square
num_rows = 12
num_cols = 12

WHITE = (255, 255, 255)  # Color of the grid lines
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BG = (232, 153, 153)
WIN_COLOR = (252, 197, 78)
WORD_COLOR = (170, 57, 250)
text_matrix = [[' ' for _ in range(num_cols)] for _ in range(num_rows)]
matrix = [[(x+11, y+4) for y in range(0, screen_width, grid_size)] for x in range(0, screen_height, grid_size)]
lines = []
matrix_lines = []



def get_random_words(filename, num_lines=10):
    lines = []
    total_lines = sum(1 for line in open(filename))
    while True:
        random_line_num = random.randint(1, total_lines)
        random_line = linecache.getline(filename, random_line_num).strip()
        if len(random_line) < 10:
            lines.append(random_line)
        if len(lines) == 10:
            return lines


words = get_random_words(r"E:\projects\games\wordSearch\words\words.txt")



#space for inserting text
# --------------------------------------------------------------------------------
def check_exists(lst, target_tuple):
    for sub_list in lst:
        if target_tuple in sub_list:
            return True
    return False

def generate_coordinate():
    return random.randint(0, 11), random.randint(0, 11)

def check_empty(row, column):
    return text_matrix[row][column] == ' '

def place_words_coordinates(words):
    placed_chars = []
    word_index = 0
    while True:
        row, column = generate_coordinate()
        is_vertical = random.choice([0, 1])
        word_coordinates = []
        if is_vertical and ((row + len(words[word_index])) > len(text_matrix)):
            row -= (row + len(words[word_index]) - len(text_matrix))
        elif not is_vertical and ((column + len(words[word_index])) > len(text_matrix)):
            column -= (column + len(words[word_index]) - len(text_matrix))

        if is_vertical:
            for i in range(row ,row + len(words[word_index])):
                if check_exists(placed_chars, (i, column)):
                    word_coordinates = []
                    word_index -= 1
                    break
                else:
                    word_coordinates.append((i, column))
        else:
            for j in range(column ,column + len(words[word_index])):
                if check_exists(placed_chars, (row, j)):
                    word_coordinates = []
                    word_index -= 1
                    break
                else:
                    word_coordinates.append((row, j))
        if not word_coordinates == []:
            placed_chars.append(word_coordinates)
        if len(placed_chars) == len(words):
            break
        word_index+= 1
    return placed_chars
# --------------------------------------------------------------------------------

def check_win():
    if len(matrix_lines) == 10:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                screen.fill(WIN_COLOR)
                win_text = win_font.render("Victory !", True, (57, 77, 250))
                screen.blit(win_text, ((screen_width - win_text.get_width())//2, (screen_height - win_text.get_height())//2))
                pygame.display.flip()



    return False

def place_words(coordinates, words):
    for word_coordinate, word in zip(coordinates, words):
        for char_coordinate, character in zip(word_coordinate, word):
            text_matrix[char_coordinate[1]][char_coordinate[0]] = character.upper()

    for i in range(len(text_matrix)):
        for j in range(len(text_matrix)):
            if text_matrix[i][j] == ' ':
                text_matrix[i][j] = random.choice(ascii_uppercase)
    
    
def get_words_coordinates():
    word_start_end = []
    for all_chars in placed_chars:
        word_start_end.append([all_chars[0], all_chars[-1]])
    return word_start_end

# Function to draw the grid
def draw_grid():

    for x in range(0, screen_width - 120, grid_size):
        pygame.draw.line(screen, WHITE, (x, 0), (x, screen_height - 170))
    for y in range(0, screen_height - 150, grid_size):
        pygame.draw.line(screen, WHITE, (0, y), (screen_width - 120, y))

# Function to draw text 
def draw_text():
    for blit_row, row in zip(matrix, text_matrix):
        for blit_column ,alphabet in zip(blit_row, row):
            character = font.render(alphabet, True, BLACK)
            screen.blit(character, blit_column)
   




# Function to get cell indices based on mouse position
def get_cell_indices(mouse_pos):
    col = mouse_pos[0] // grid_size
    row = mouse_pos[1] // grid_size
    return row, col

def draw_line():
    # Draw each line stored in the lines list
    
    for line_start, line_end in matrix_lines:
        pygame.draw.line(screen, GREEN, (line_start[1] * grid_size+20, line_start[0] * grid_size+20), (line_end[1] * grid_size+20, line_end[0] * grid_size+20), 5)

def press_line(start_pos, end_pos):
    if check_word(start_pos, end_pos):
        start_cell = get_cell_indices(start_pos)
        end_cell = get_cell_indices(end_pos)
        if [start_cell, end_cell] not in matrix_lines:
            matrix_lines.append([start_cell, end_cell])
            check_win()
        
        pygame.draw.line(screen, GREEN, start_pos, end_pos, 5)
    else:
        pygame.draw.line(screen, RED, start_pos, end_pos, 5)
        

def check_word(start_pos, end_pos):
    start_pos = get_cell_indices(start_pos)
    end_pos = get_cell_indices(end_pos)

    for word_positions in word_start_end:
        if [start_pos, end_pos] == word_positions or [end_pos, start_pos] == word_positions:

            return True

    return False


def display_words():
    row = 510
    words_per_row = min(len(words), (screen_width - 100) // 150)  # Calculate words per row dynamically
    word_spacing = (screen_width - 100) // words_per_row
    
    pygame.draw.line(screen, YELLOW, (50, 490), (550, 490), 3)
    completed_words = word_font.render(str(len(matrix_lines)), True, WORD_COLOR)
    divide = word_font.render("__", True, WORD_COLOR)
    total_words = word_font.render(str(10), True, WORD_COLOR)

    screen.blit(completed_words, (510, 110))
    screen.blit(divide, (500, 120))
    screen.blit(total_words, (500, 160))

    for i, word in enumerate(words):
        column = 50 + (i % words_per_row) * word_spacing
        blit_word = word_font.render(word, True, WORD_COLOR)
        
        # Center-align the word within the grid cell
        text_rect = blit_word.get_rect(center=(column + word_spacing // 2, row))
        
        screen.blit(blit_word, text_rect)
        
        if (i + 1) % words_per_row == 0:  # Move to the next row
            row += 40  # Adjust the vertical spacing between rows

# Main loop
placed_chars = place_words_coordinates(words)
place_words(placed_chars, words)
word_start_end = get_words_coordinates()



def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    line_start = pygame.mouse.get_pos()  # Set the start position of the line
    
        mouse_buttons = pygame.mouse.get_pressed()

        # Fill the screen with black
        screen.fill(BG)
        draw_grid()
        draw_text()
        draw_line()
        display_words()
        # THIS is for continous line while mouse get pressed
        if mouse_buttons[0]:  # 0 represents the left mouse button
            line_end = pygame.mouse.get_pos()
            press_line(line_start, line_end)





        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()