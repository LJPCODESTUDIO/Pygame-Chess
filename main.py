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

#Events
REPEAT_SOUND = pg.USEREVENT + 1

#Fonts
NORMAL_DEFAULT_FONT = pg.font.SysFont('comicsans', 40)
SMALL_DEFAULT_FONT = pg.font.SysFont("comicsans", 20)

#Sounds
SOUNDTRACK = pg.mixer.Sound(os.path.join('Music', 'Jedmester_the_ditty.wav'))
SOUNDTRACK.set_volume(.5)

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Global Vars
grid = [
    ["O", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "O", "", ""],
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
    "Clock: ",
    "Volume: "
]


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
    if command == "debug":
        if show_debug:
            show_debug = False
            return
        show_debug = True
    elif "set" in command:
        args = command.split()
        if args[0] == "set_volume":
            SOUNDTRACK.set_volume(float(args[1]))


def handle_debugs():
    global debugs
    mouse_pos = pg.mouse.get_pos()
    get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
    debugs[0] = "Mouse Pos: " + str(mouse_pos)
    debugs[1] = f"Grid Pos: ({grid_x}, {grid_y})"
    debugs[2] = f"Tile: {tile}"
    debugs[3] = "Clock: " + str(pg.time.get_ticks())
    debugs[4] = "Volume: %" + str(SOUNDTRACK.get_volume()*100)


def draw_debug():
    y = -5
    for debug in debugs:
        draw_debug = SMALL_DEFAULT_FONT.render(str(debug), 1, GREEN)
        SCREEN.blit(draw_debug, (0, y))
        y += 20


def draw_console():
    text = SMALL_DEFAULT_FONT.render(console_text, 1, GREEN)
    SCREEN.blit(text, (10, HEIGHT - text.get_height() - 5))


def draw_screen(grid_size, cell_size):
    SCREEN.fill((0, 150, 150))
    draw_board(OFFSET_X, OFFSET_Y, grid_size, cell_size)
    title = NORMAL_DEFAULT_FONT.render("Chess Match!", 1, WHITE)
    SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, -5))
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
            if grid[cell_y][cell_x] == "O":
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
    pg.time.set_timer(REPEAT_SOUND, 139800)
    clock = pg.time.Clock()
    run = True
    console = True
    global console_text
    global command
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
                    if grid[grid_y][grid_x] == "":
                       grid[grid_y][grid_x] = "O"
                    elif grid[grid_y][grid_x]:
                        grid[grid_y][grid_x] = ""

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
            handle_debugs()
        
        draw_screen(GRID_SIZE, CELL_SIZE)

    main()


if __name__ == "__main__":
    main()