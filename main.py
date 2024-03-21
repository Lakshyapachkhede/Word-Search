import pygame
import random
from string import ascii_uppercase, ascii_lowercase
import sys

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 601
screen_height = 601
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid Example")

font = pygame.font.Font(r'E:\projects\games\wordSearch\font\comic\COMICSANS.ttf', 36)  # None uses the default system font, 36 is the font size


# Set up grid parameters
grid_size = 50  # Adjust the size of each grid square
num_rows = screen_height // grid_size
num_cols = screen_width // grid_size

WHITE = (255, 255, 255)  # Color of the grid lines
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
bg_color = (232, 153, 153)
text_matrix = [[' ' for _ in range(screen_width // grid_size)] for _ in range(screen_height // grid_size)]
matrix = [[(x+10, y+3) for y in range(0, screen_width, grid_size)] for x in range(0, screen_height, grid_size)]
lines = []
words = ["story","young","fact","month","different","lot","right","study","book","eye","job"]



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

    for x in range(0, screen_width, grid_size):
        pygame.draw.line(screen, WHITE, (x, 0), (x, screen_height))
    for y in range(0, screen_height, grid_size):
        pygame.draw.line(screen, WHITE, (0, y), (screen_width, y))

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
    print(lines)

    for line_start, line_end in lines:
        pygame.draw.line(screen, GREEN, line_start, line_end, 5)

def press_line(start_pos, end_pos):
    if check_word(start_pos, end_pos):
        if [start_pos, end_pos] not in lines and [end_pos, start_pos] not in lines:
            lines.append([start_pos, end_pos])
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
        screen.fill(bg_color)
        draw_grid()
        draw_text()
        draw_line()

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