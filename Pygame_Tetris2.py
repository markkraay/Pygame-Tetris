# Command Line Tetris

import random
import pygame
import time

forbidden_block = '0'
shape_block = '#'
filler_block = '-'
amt_rows = 20
amt_columns = 10
score = 0
run = True

# Screen Variables
screen_width = 600
screen_height = screen_width + 200
play_width = screen_width // 2
play_height = screen_height - 200
block_width = play_width // amt_columns
block_height = play_height // amt_rows
left_most_play = (screen_width // 2) - (play_width // 2)
top_most_play = 100

# SHAPE FORMATS

S = ['.....',
     '.....',
     '..00.',
     '.00..',
     '.....']

Z = ['.....',
     '.....',
     '.00..',
     '..00.',
     '.....']

I = ['..0..',
     '..0..',
     '..0..',
     '..0..',
     '.....']

O = ['.....',
     '.....',
     '.00..',
     '.00..',
     '.....']

J = ['.....',
     '.0...',
     '.000.',
     '.....',
     '.....']

L = ['.....',
     '...0.',
     '.000.',
     '.....',
     '.....']

T = ['.....',
     '..0..',
     '.000.',
     '.....',
     '.....']

# Rotations
S_R = [[[1, 0], [0, 1], [1, -2], [0, -1]], [[-1, 0], [0, -1], [-1, 2], [0, 1]]]

Z_R = [[[1, -1], [0, 1], [1, 0], [0, 2]], [[-1, 1], [0, -1], [-1, 0], [0, -2]]]

I_R = [[[0, 2], [1, 1], [2, 0], [3, -1]], [[1, -2], [0, -1], [-1, 0], [-2, 1]]]

O_R = [[[0, 0], [0, 0], [0, 0], [0, 0]]]

J_R = [[[0, -1], [1, -2], [0, 0], [-1, 1]], [[-1, 1], [-1, 1], [0, -1], [0, -1]], [[1, -1], [0, 0], [-1, 2], [0, 1]],
       [[0, 1], [0, 1], [1, -1], [1, -1]]]

L_R = [[[0, 1], [0, -1], [-1, 0], [-1, 0]], [[-1, 1], [0, 0], [1, -1], [0, 2]], [[1, 0], [1, 0], [0, 1], [0, -1]],
       [[0, -2], [-1, 1], [0, 0], [1, -1]]]

T_R = [[[0, 0], [0, -1], [0, -1], [-1, 1]], [[-1, 1], [0, 0], [0, 0], [0, 0]], [[1, -1], [0, 1], [0, 1], [0, 0]],
       [[0, 0], [0, 0], [0, 0], [1, -1]]]

def create_grid():
    grid = [[(filler_block) for i in (range(amt_columns))] for i in range(amt_rows + 5)]
    for row in grid:
        row.append(forbidden_block)
        row.insert(0, forbidden_block)
    grid.insert(0, [(forbidden_block) for i in range(amt_columns + 2)])
    grid.append([(forbidden_block) for i in range(amt_columns + 2)])
    return grid

shapes = [S, Z, I, O, J, L, T]
shape_colors = ['a', 'b', 'c', 'd', 'e', 'f', 'g']


class Shape():
    def __init__(self, shape, rotation_pos):
        self.falling = False
        self.positions = []
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        self.shape = shape
        self.rotation_pos = rotation_pos


def get_shape(shapes):
    random_shape = random.choice(shapes)
    if random_shape == S:
        rotation_pos = S_R
    elif random_shape == Z:
        rotation_pos = Z_R
    elif random_shape == I:
        rotation_pos = I_R
    elif random_shape == O:
        rotation_pos = O_R
    elif random_shape == J:
        rotation_pos = J_R
    elif random_shape == L:
        rotation_pos = L_R
    elif random_shape == T:
        rotation_pos = T_R
    return Shape(random_shape, rotation_pos)


def add_shape_to_grid(grid, shape):
    r, c = 1, amt_columns // 2
    for row in shape.shape:
        for column in row:
            if column == '0':
                if grid[r][c] == filler_block:
                    shape.positions.append([r, c])
                    grid[r].pop(c)
                    grid[r].insert(c, shape_block)

            c += 1
        c = amt_columns // 2
        r += 1
    shape.falling = True


def shift_down():
    positions = shape.positions
    positions.sort(key=lambda positions: positions[0])
    positions.reverse()
    new_positions = []

    for i in range(len(positions)):
        pos = positions[i]
        pos_y = pos[0]
        pos_x = pos[1]
        if grid[pos_y + 1][pos_x] == filler_block:
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, filler_block)
            pos_y += 1
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, shape_block)
            new_positions.append([pos_y, pos_x])

        elif grid[pos_y + 1][pos_x] == forbidden_block:
            shape.falling = False
            break

        elif grid[pos_y + 1][pos_x] != filler_block or grid[pos_y + 1][pos_x] != forbidden_block:
            # There must be a color block
            shape.falling = False
            break
    if len(new_positions) == len(positions):
        shape.positions = new_positions
    else:
        for i in range(len(new_positions)):
            pos = new_positions[i]
            pos_y = pos[0]
            pos_x = pos[1]
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, filler_block)


def shift_left():
    positions = shape.positions
    positions.sort(key=lambda positions: positions[1])
    new_positions = []
    for i in range(len(positions)):
        pos = positions[i]
        pos_y = pos[0]
        pos_x = pos[1]
        if grid[pos_y][pos_x - 1] == filler_block:
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, filler_block)
            pos_x -= 1
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, shape_block)
            new_positions.append([pos_y, pos_x])

    if len(new_positions) == len(positions):
        shape.positions = new_positions
    else:
        for i in range(len(new_positions)):
            pos = new_positions[i]
            pos_y = pos[0]
            pos_x = pos[1]
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, filler_block)


def shift_right():
    positions = shape.positions
    positions.sort(key=lambda positions: positions[1])
    positions.reverse()
    new_positions = []
    for i in range(len(shape.positions)):
        pos = shape.positions[i]
        pos_y = pos[0]
        pos_x = pos[1]
        if grid[pos_y][pos_x + 1] == filler_block:
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, filler_block)
            pos_x += 1
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, shape_block)
            new_positions.append([pos_y, pos_x])

    if len(new_positions) == len(positions):
        shape.positions = new_positions
    else:
        for i in range(len(new_positions)):
            pos = new_positions[i]
            pos_y = pos[0]
            pos_x = pos[1]
            grid[pos_y].pop(pos_x)
            grid[pos_y].insert(pos_x, filler_block)

pygame.init()
pygame.display.set_caption('Tetris')
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("retrogamingttf", 72)
font2 = pygame.font.SysFont("retrogamingttf", 32)
font3 = pygame.font.SysFont("retrogamingttf", 40)
Tetris_Logo = font.render("Tetris", True, (255, 154, 59))
Tetris_Logo2 = font.render("Tetris", True, (13, 33, 186))

def print_grid():
    logo_width = Tetris_Logo.get_width()
    screen.fill((0, 0, 0))
    screen.blit(Tetris_Logo2, ((screen_width//2)-(logo_width//2)+5, 5))
    screen.blit(Tetris_Logo, ((screen_width//2)-(logo_width//2), 0))

    new_grid = grid[6:]

    pygame.draw.rect(screen, (0, 0, 0), (left_most_play, top_most_play, play_width, play_height))
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, 100))
    global score
    Score_Logo = font2.render("Score", True, (255, 154, 59))
    screen.blit(Score_Logo, (0, 0))
    Score = font2.render(str(score), True, (255, 154, 59))
    screen.blit(Score, (0, 30))

    for i in range(0, len(new_grid)):
        for j in range(len(new_grid[i])):
            if new_grid[i][j] == shape_block:
                if shape.color == 'a':
                    pygame.draw.rect(screen, (245, 147, 66), (
                        left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                        block_height))
                elif shape.color == 'b':
                    pygame.draw.rect(screen, (102, 245, 66), (
                        left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                        block_height))
                elif shape.color == 'c':
                    pygame.draw.rect(screen, (66, 245, 227), (
                        left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                        block_height))
                elif shape.color == 'd':
                    pygame.draw.rect(screen, (66, 78, 245), (
                        left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                        block_height))
                elif shape.color == 'e':
                    pygame.draw.rect(screen, (197, 66, 245), (
                        left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                        block_height))
                elif shape.color == 'f':
                    pygame.draw.rect(screen, (220, 66, 66), (
                        left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                        block_height))
                elif shape.color == 'g':
                    pygame.draw.rect(screen, (245, 233, 66), (
                        left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                        block_height))

            if new_grid[i][j] == 'a':
                pygame.draw.rect(screen, (245, 147, 66), (
                    left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                    block_height))
            if new_grid[i][j] == 'b':
                pygame.draw.rect(screen, (102, 245, 66), (
                    left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                    block_height))
            if new_grid[i][j] == 'c':
                pygame.draw.rect(screen, (66, 245, 227), (
                    left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                    block_height))
            if new_grid[i][j] == 'd':
                pygame.draw.rect(screen, (66, 78, 245), (
                    left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                    block_height))
            if new_grid[i][j] == 'e':
                pygame.draw.rect(screen, (197, 66, 245), (
                    left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                    block_height))
            if new_grid[i][j] == 'f':
                pygame.draw.rect(screen, (245, 66, 66), (
                    left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                    block_height))
            if new_grid[i][j] == 'g':
                pygame.draw.rect(screen, (245, 233, 66), (
                    left_most_play + block_width * (j - 1), top_most_play + (block_height * i), block_width,
                    block_height))

    for i in range(0, amt_columns + 1):
        pygame.draw.line(screen, (105, 105, 105), (left_most_play + (block_width * i), top_most_play),
                         (left_most_play + (block_width * i), top_most_play + play_height))
    for i in range(0, amt_rows + 1):
        pygame.draw.line(screen, (105, 105, 105), (left_most_play, top_most_play + (block_height * i)),
                         (left_most_play + play_width, top_most_play + (block_height * i)))

    pygame.display.update()


def solidfy_shape():
    for i in range(len(shape.positions)):
        pos = shape.positions[i]
        pos_y = pos[0]
        pos_x = pos[1]
        grid[pos_y].pop(pos_x)
        grid[pos_y].insert(pos_x, shape.color)
        shape.falling = False


def rotate_shape():
    shape.rotation += 1
    if shape.rotation > len(shape.rotation_pos) - 1:
        shape.rotation = 0
        transformation = shape.rotation_pos[-1]
    elif shape.rotation == 1:
        transformation = shape.rotation_pos[0]
    elif shape.rotation == 2:
        transformation = shape.rotation_pos[1]
    elif shape.rotation == 3:
        transformation = shape.rotation_pos[2]
    elif shape.rotation == 4:
        transformation = shape.rotation_pos[3]

    positions = shape.positions
    positions.sort(key=lambda x: (x[0], x[1]))
    new_pos = []

    for i in range(len(transformation)):
        trans = transformation[i]
        pos = positions[i]

        tempvar = []
        for j in range(2):
            g = pos[j] - trans[j]
            tempvar.append(g)
        new_pos.append(tempvar)

    for i in range(len(positions)):
        pos = positions[i]
        y = pos[0]
        x = pos[1]
        grid[y].pop(x)
        grid[y].insert(x, filler_block)

    count = 0
    for i in range(len(new_pos)):
        try:
            new_y = new_pos[i][0]
            new_x = new_pos[i][1]
            if grid[new_y][new_x] == filler_block:
                count += 1
        except:
            pass

    new_pos_2 = []
    if count == (len(new_pos)):
        for i in range(len(new_pos)):
            new_y = new_pos[i][0]
            new_x = new_pos[i][1]
            new_pos_2.append([new_y, new_x])
            grid[new_y].pop(new_x)
            grid[new_y].insert(new_x, shape_block)
        shape.positions = new_pos_2

    else:
        for i in range(len(positions)):
            pos = positions[i]
            new_y = pos[0]
            new_x = pos[1]
            grid[new_y].pop(new_x)
            grid[new_y].insert(new_x, shape_block)
        shape.positions = positions
        shape.rotation -= 1


def check_full_row():
    for i in range(1, len(grid) - 1):
        count = 0
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] != filler_block:
                count += 1

        if count == amt_columns:
            grid.pop(i)
            grid.insert(1, [(filler_block) for _ in (range(amt_columns))])
            grid[1].append(forbidden_block)
            grid[1].insert(0, forbidden_block)
            global score
            score += 10

def check_lost():
    count = 0
    for i in range(1, len(grid[4]) - 1):
        if grid[5][i] == filler_block or grid[5][i] == shape_block:
            count += 1
    if count == amt_columns:
        return False
    else:
        return True

# Game Loop
r = 0
grid = create_grid()
while run:
    sleep_time = .27
    x = check_lost()
    if x:
        #Writing to score file
        f = open("scores1.txt", "a")
        f.write("\n" + (str(score)))
        f.close()
        decision = True
        fader = 0
        red = 150
        g = 100
        b = 50
        while decision:
            time.sleep(0.01)
            if fader == 98:
                fader = 0
            elif fader < 49:
                red -= 3
                g -= 2
                b -= 1
                fader += 1
            elif fader >= 49:
                red += 3
                g += 2
                b += 1
                fader += 1

            # Displaying quit screen
            screen.fill((0, 0, 0))

            # Blit Game Over
            game_over = font.render("Game Over", True, (red, g, b))
            logo_width = game_over.get_width()
            logo_height = game_over.get_height()
            game_over2 = font.render("Game Over", True, (b, g, red))
            screen.blit(game_over2,
                        (
                            (screen_width // 2) - (logo_width // 2) + 5, (screen_height // 2) - (logo_height // 2) + 5))
            screen.blit(game_over,
                        ((screen_width // 2) - (logo_width // 2), (screen_height // 2) - (logo_height // 2)))

            #Blit Score
            Score_log = font.render("Score", True, (255, 154, 59))
            Score_log_width = Score_log.get_width()
            Score_log_height = Score_log.get_height()
            screen.blit(Score_log,
                        ((screen_width // 2) - (Score_log_width // 2), 200))
            Score = font.render(str(score), True, (255, 154, 59))
            score_width = Score.get_width()
            score_height = Score.get_height()
            screen.blit(Score,
                        ((screen_width // 2) - (score_width // 2),
                         260))

            #Blit Control Options
            press_enter = font3.render("Press ENTER to Play Again", True, (red, g, b))
            press_enter_width = press_enter.get_width()
            press_enter_height = press_enter.get_height()
            press_space = font3.render("Press SPACE to Quit", True, (red, g, b))
            press_space_width = press_space.get_width()
            screen.blit(press_enter, (screen_width//2 - press_enter_width//2, screen_height//2 - press_enter_height//2 + 100))
            screen.blit(press_space, (
            screen_width // 2 - press_space_width // 2, screen_height // 2 - press_enter_height // 2 + 170))

            #Blit High Score
            with open("scores1.txt") as file:
                lines = [line.rstrip('\n') for line in file]
            maxScore = max(lines)
            max_Score = font3.render("High Score: " + str(maxScore), True, (255, 154, 59))
            max_Score_width = max_Score.get_width()
            max_score_height = max_Score.get_height()
            screen.blit(max_Score, (screen_width//2 - max_Score_width//2, 100))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        decision = False
                        run = False
                        break
                    if event.key == pygame.K_RETURN:
                        r = 0
                        decision = False
                        score = 0
                        grid = create_grid()
                        break

    else:
        if r == 0:
            shape = get_shape(shapes)
            grid = create_grid()
        if shape.falling:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        shift_left()
                    if event.key == pygame.K_RIGHT:
                        shift_right()
                    if event.key == pygame.K_DOWN:
                        sleep_time = .15
                    if event.key == pygame.K_SPACE:
                        run = False
                    if event.key == pygame.K_UP:
                        rotate_shape()

        if shape.falling is False:
            shape = get_shape(shapes)
            add_shape_to_grid(grid, shape)
            b = 0
        if shape.falling:
            shift_down()
        if shape.falling is False:
            solidfy_shape()
            check_full_row()

        print_grid()
        r += 1
        time.sleep(sleep_time)
