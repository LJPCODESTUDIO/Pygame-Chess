import pygame as pg
import os

#Init stuffs
pg.mixer.init()
pg.font.init()
pg.init()
pg.display.set_caption("WOOOO CHESS!")

#Const Var Inits
WIDTH, HEIGHT = 900, 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

FPS = 60

#Events
REPEAT_SOUND = pg.USEREVENT + 1

#Fonts
NORMAL_DEFAULT_FONT = pg.font.SysFont('comicsans', 40)
SMALL_DEFAULT_FONT = pg.font.SysFont("comicsans", 20)

#Sounds
SOUNDTRACK = pg.mixer.Sound(os.path.join('Music', 'Jedmester_the_ditty.wav'))

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Global Vars
grid = [
    ["X", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "X", "", ""],
]
console_text = ''
command = ''
show_debug = False
debugs = [
    "Mouse Pos: ",
    "Clock: "
]


def handle_commands():
    global show_debug
    if command == "debug":
        if show_debug:
            show_debug = False
            return
        show_debug = True


def draw_debug():
    global debugs
    y = -5
    mouse_pos = pg.mouse.get_pos()
    debugs[0] = "Mouse Pos: " + str(mouse_pos)
    debugs[1] = "Clock: " + str(pg.time.get_ticks())
    for debug in debugs:
        draw_debug = SMALL_DEFAULT_FONT.render(str(debug), 1, GREEN)

        SCREEN.blit(draw_debug, (0, y))
        y += 20


def draw_console():
    text = SMALL_DEFAULT_FONT.render(console_text, 1, GREEN)
    SCREEN.blit(text, (10, HEIGHT - text.get_height() - 5))


def draw_screen(grid_size, cell_size):
    SCREEN.fill((0, 150, 150))
    offset_x = WIDTH//2-(grid_size*cell_size//2)
    offset_y = HEIGHT//2-(grid_size*cell_size//2)+20
    draw_board(offset_x, offset_y, grid_size, cell_size)
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
            if grid[cell_y][cell_x] == "X":
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
    grid_size = 8
    cell_size = 80
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
            
                if event.key == pg.K_F3:
                        console = True
                        console_text = '>' + command
        
        draw_screen(grid_size, cell_size)

    main()


if __name__ == "__main__":
    main()