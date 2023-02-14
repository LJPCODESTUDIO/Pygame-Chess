import pygame as pg
import math
import os

#Init stuffs
pg.mixer.init()
pg.font.init()
pg.init()
pg.display.set_caption("WOOOO CHESS!")

#Const Var Inits
WIDTH, HEIGHT = 900, 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
GRID_SIZE = 8
CELL_SIZE = 80
OFFSET_X = WIDTH//2-(GRID_SIZE*CELL_SIZE//2)
OFFSET_Y = HEIGHT//2-(GRID_SIZE*CELL_SIZE//2)+20

FPS = 60

#Move Dictionaries
BLACK_MOVES = {"Pawn":[[1, 0]]}
WHITE_MOVES = {"Pawn":[[-1, 0]]}

#Events
REPEAT_SOUND = pg.USEREVENT + 1

#Fonts
NORMAL_DEFAULT_FONT = pg.font.SysFont('comicsans', 40)
SMALL_DEFAULT_FONT = pg.font.SysFont("comicsans", 20)

#Sounds
SOUNDTRACK = pg.mixer.Sound(os.path.join('Music', 'Space Jazz.wav'))
SOUNDTRACK.set_volume(.5)

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Black Unit images
BLACK_PAWN_IMAGE = pg.image.load(os.path.join("Assets", "Black Pawn.svg"))
BLACK_PAWN = BLACK_PAWN_IMAGE

#White Unit Images
WHITE_PAWN_IMAGE = pg.image.load(os.path.join("Assets", "White Pawn.svg"))
WHITE_PAWN = WHITE_PAWN_IMAGE

#Global Vars
grid = [
    ["", "", "", "", "", "", "", ""],
    ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
    ["", "", "", "", "", "", "", ""],
]
old_grid = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
]
grid_x = 0
grid_y = 0
tile = ""
console_text = ''
command = ''
show_debug = False
debugs = [
    "Mouse Pos: ",
    "Grid Pos: ",
    "Tile: ",
    "Grabbed: ",
    "Clock: ",
    "Volume: "
]

#Handle the logic
def get_tile(x, y, offset_x, offset_y):
    global grid_x
    global grid_y
    global tile
    grid_x = math.floor((x - offset_x)//CELL_SIZE)
    grid_y = math.floor((y - offset_y)//CELL_SIZE)
    if grid_x > 7:
        grid_x = 7
    elif grid_x < 0:
        grid_x = 0
    if grid_y > 7:
        grid_y = 7
    elif grid_y < 0:
        grid_y = 0
    tile = grid[grid_y][grid_x]


def handle_commands():
    global show_debug
    global grid
    if command == "debug":
        if show_debug:
            show_debug = False
            return
        show_debug = True
    elif command == "clear":
        grid = [
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""]
            ]
    elif command == "fill":
        grid = [
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"]
            ]
    elif "set" in command:
        args = command.split()
        if args[0] == "set_volume":
            SOUNDTRACK.set_volume(float(args[1]))


def handle_debugs(grabbed_unit):
    global debugs
    mouse_pos = pg.mouse.get_pos()
    get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
    debugs[0] = "Mouse Pos: " + str(mouse_pos)
    debugs[1] = f"Grid Pos: ({grid_x}, {grid_y})"
    debugs[2] = f"Tile: {tile}"
    debugs[3] = f"Grabbed: {grabbed_unit}"
    debugs[4] = "Clock: " + str(pg.time.get_ticks())
    debugs[5] = "Volume: %" + str(SOUNDTRACK.get_volume()*100)

#Find all the valid locations to move
def find_pos(grabbed_unit, grabbed_pos):
    if grabbed_unit == "BP":
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + BLACK_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1
        if possible_y > 7:
            return
        if grid[possible_y][possible_x] == "":
            grid[possible_y][possible_x] = "O"
        if kill_x1 <= 7:
            if "W" in grid[possible_y][kill_x1]:
                grid[possible_y][kill_x1] = grid[possible_y][kill_x1] + "O"
        if kill_x2 >= 0:
            if "W" in grid[possible_y][kill_x2]:
                grid[possible_y][kill_x2] = grid[possible_y][kill_x2] + "O"
    if grabbed_unit == "WP":
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + WHITE_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1
        if possible_y < 0:
            return
        if grid[possible_y][possible_x] == "":
            grid[possible_y][possible_x] = "O"
        if kill_x1 <= 7:
            if "B" in grid[possible_y][kill_x1]:
                grid[possible_y][kill_x1] = grid[possible_y][kill_x1] + "O"
        if kill_x2 >= 0:
            if "B" in grid[possible_y][kill_x2]:
                grid[possible_y][kill_x2] = grid[possible_y][kill_x2] + "O"

#Because it doesn't like removing circles
def remove_pos(grabbed_unit, grabbed_pos):
    global grid
    if grabbed_unit == "BP":
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + BLACK_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1
        if grid[possible_y][possible_x] == "":
            grid[possible_y][possible_x] = "O"
        if kill_x1 <= 7:
            if "W" in grid[possible_y][kill_x1]:
                grid[possible_y][kill_x1] = grid[possible_y][kill_x1] + "O"
        if kill_x2 >= 0:
            if "W" in grid[possible_y][kill_x2]:
                grid[possible_y][kill_x2] = grid[possible_y][kill_x2] + "O"
    if grabbed_unit == "WP":
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + WHITE_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1
        if grid[possible_y][possible_x] == "O":
            grid[possible_y][possible_x] = ""
        if kill_x1 <= 7:
            if "B" in grid[possible_y][kill_x1]:
                point = grid[possible_y][kill_x1].replace("O", "")
                grid[possible_y][kill_x1] = point
        if kill_x2 >= 0:
            if "B" in grid[possible_y][kill_x2]:
                point = grid[possible_y][kill_x2].replace("O", "")
                grid[possible_y][kill_x2] = point

#Draw the screen
def draw_debug():
    y = -5
    for debug in debugs:
        draw_debug = SMALL_DEFAULT_FONT.render(str(debug), 1, GREEN)
        SCREEN.blit(draw_debug, (0, y))
        y += 20


def draw_console():
    text = SMALL_DEFAULT_FONT.render(console_text, 1, GREEN)
    SCREEN.blit(text, (10, HEIGHT - text.get_height() - 5))


def draw_screen(grid_size, cell_size, grabbed_unit):
    SCREEN.fill((0, 150, 150))
    draw_board(OFFSET_X, OFFSET_Y, grid_size, cell_size)
    title = NORMAL_DEFAULT_FONT.render("Chess Match!", 1, WHITE)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, -5))
    if grabbed_unit != "":
        mouse_pos = pg.mouse.get_pos()
        if grabbed_unit == "BP":
            SCREEN.blit(BLACK_PAWN, (mouse_pos[0]-(cell_size//2)+15, mouse_pos[1]-(cell_size//2)))
        elif grabbed_unit == "WP":
            SCREEN.blit(WHITE_PAWN, (mouse_pos[0]-(cell_size//2)+15, mouse_pos[1]-(cell_size//2)))
    if show_debug:
        draw_debug()
    draw_console()
    pg.display.update()


def draw_board(offset_x, offset_y, grid_size, cell_size):
    move_y = offset_y
    colour = WHITE
    for cell_y in range(grid_size):
        move_x = offset_x
        for cell_x in range(grid_size):
            cell = pg.Rect(move_x, move_y, cell_size, cell_size)
            pg.draw.rect(SCREEN, colour, cell)
            if "BP" in grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_PAWN, (move_x+15, move_y))
            if "WP" in grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_PAWN, (move_x+15, move_y))
            if "O" in grid[cell_y][cell_x]:
                pg.draw.circle(SCREEN, BLUE, (move_x + (cell_size//2), move_y + (cell_size//2)), cell_size//3, 5)
            move_x += cell_size
            if colour == WHITE:
                colour = BLACK
            else:
                colour = WHITE
        move_y += cell_size
        if colour == WHITE:
                colour = BLACK
        else:
            colour = WHITE


def main():
    pg.time.set_timer(REPEAT_SOUND, int(SOUNDTRACK.get_length() * 1000))
    clock = pg.time.Clock()
    run = True
    console = True
    grabbed_unit = ""
    grabbed_pos = [0, 0]
    global console_text
    global command
    global grid
    global old_grid
    SOUNDTRACK.play()
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
            
            if event.type == REPEAT_SOUND:
                SOUNDTRACK.play()
            
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pressed()
                if mouse[0]:
                    mouse_pos = pg.mouse.get_pos()
                    get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
                    if grabbed_unit == "":
                        old_grid[grid_y][grid_x] = grid[grid_y][grid_x]
                        grabbed_unit = grid[grid_y][grid_x]
                        grabbed_pos[0] = grid_y
                        grabbed_pos[1] = grid_x
                        find_pos(grabbed_unit, grabbed_pos)
                        grid[grid_y][grid_x] = ""
                    else:
                        if "O" in grid[grid_y][grid_x]:
                            remove_pos(grabbed_unit, grabbed_pos)  
                            grid[grid_y][grid_x] = grabbed_unit
                            grabbed_unit = ""
                        else:
                            grid[grabbed_pos[0]][grabbed_pos[1]] = old_grid[grabbed_pos[0]][grabbed_pos[1]]
                            remove_pos(grabbed_unit, grabbed_pos)
                            grabbed_unit = ""

            if event.type == pg.KEYDOWN:
                if console:
                    if event.key == pg.K_BACKSPACE:
                        if len(command)>0:
                            command = command[:-1]
                    elif event.key == pg.K_RETURN:
                        console = False
                        handle_commands()
                        console_text = ''
                        command = ''
                        continue
                    else:
                        command += event.unicode
                    
                    console_text = '>' + command
            
                if event.key == pg.K_F1:
                        console = True
                        console_text = '>' + command

        if show_debug:
            handle_debugs(grabbed_unit)
        
        draw_screen(GRID_SIZE, CELL_SIZE, grabbed_unit)

    main()


if __name__ == "__main__":
    main()