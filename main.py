import pygame as pg
import math
import os
from game import Game
from network import network


#Init stuffs
pg.mixer.init()
pg.font.init()
pg.init()
pg.display.set_caption("WOOOO CHESS!")
pack = "Default"

#Event
REPEAT_SOUND = pg.USEREVENT + 1

#Const Var Inits
WIDTH = 900
HEIGHT = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
OFFSET_X = WIDTH//2-(8*80//2)
OFFSET_Y = HEIGHT//2-(8*80//2)+20

FPS = 60

#Fonts
BIG_DEFAULT_FONT = pg.font.SysFont('comicsans', 80)
NORMAL_DEFAULT_FONT = pg.font.SysFont('comicsans', 40)
SMALL_DEFAULT_FONT = pg.font.SysFont("comicsans", 20)

#Sounds
SOUNDTRACK = pg.mixer.Sound(os.path.join(f'Assets/{pack}/Music', 'Match.wav'))
SOUNDTRACK.set_volume(.5)
GAME_END = pg.mixer.Sound(os.path.join(f'Assets/{pack}/Music', 'Game_End.wav'))
GAME_END.set_volume(.5)

#Black Unit images
BLACK_PAWN = pg.image.load(os.path.join(f"Assets/{pack}", "Black Pawn.svg"))
BLACK_KNIGHT_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Knight.svg"))
BLACK_ROOK_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Rook.svg"))
BLACK_BISHOP_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Bishop.svg"))
BLACK_QUEEN_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Queen.svg"))
BLACK_KING_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black King.svg"))

#White Unit Images
WHITE_PAWN = pg.image.load(os.path.join(f"Assets/{pack}", "White Pawn.svg"))
WHITE_KNIGHT_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Knight.svg"))
WHITE_ROOK_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Rook.svg"))
WHITE_BISHOP_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Bishop.svg"))
WHITE_QUEEN_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Queen.svg"))
WHITE_KING_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White King.svg"))

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Global Vars
grid = [
    ["BR", "BK", "BF", "BQ", "BG", "BF", "BK", "BR"],
    ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
    ["WR", "WK", "WF", "WQ", "WG", "WF", "WK", "WR"],
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
grabbed = ""
grabbed_pos = [0, 0]
tile = ""
console_text = ''
command = ''
show_debug = False
debug_message = []
debug_time = []
debugs = [
    "Mouse Pos: ",
    "Grid Pos: ",
    "Tile: ",
    "Grabbed: ",
    "Clock: ",
    "Volume: "
]


def reload_assets():
    global SOUNDTRACK
    global GAME_END
    global BLACK_PAWN
    global BLACK_KNIGHT_IMAGE
    global BLACK_ROOK_IMAGE
    global BLACK_BISHOP_IMAGE
    global BLACK_QUEEN_IMAGE
    global BLACK_KING_IMAGE
    global WHITE_PAWN
    global WHITE_KNIGHT_IMAGE
    global WHITE_ROOK_IMAGE
    global WHITE_BISHOP_IMAGE
    global WHITE_QUEEN_IMAGE
    global WHITE_KING_IMAGE
    #Sounds
    SOUNDTRACK = pg.mixer.Sound(os.path.join(f'Assets/{pack}/Music', 'Match.wav'))
    SOUNDTRACK.set_volume(.5)
    GAME_END = pg.mixer.Sound(os.path.join(f'Assets/{pack}/Music', 'Game_End.wav'))
    GAME_END.set_volume(.5)

    #Black Unit images
    BLACK_PAWN = pg.image.load(os.path.join(f"Assets/{pack}", "Black Pawn.svg"))
    BLACK_KNIGHT_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Knight.svg"))
    BLACK_ROOK_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Rook.svg"))
    BLACK_BISHOP_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Bishop.svg"))
    BLACK_QUEEN_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black Queen.svg"))
    BLACK_KING_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "Black King.svg"))

    #White Unit Images
    WHITE_PAWN = pg.image.load(os.path.join(f"Assets/{pack}", "White Pawn.svg"))
    WHITE_KNIGHT_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Knight.svg"))
    WHITE_ROOK_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Rook.svg"))
    WHITE_BISHOP_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Bishop.svg"))
    WHITE_QUEEN_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White Queen.svg"))
    WHITE_KING_IMAGE = pg.image.load(os.path.join(f"Assets/{pack}", "White King.svg"))


def handle_commands(g):
    if command == "debug":
        if show_debug:
            show_debug = False
            return
        show_debug = True
    elif command == "retry":
        pg.event.post(g.RETRY)


    elif command == "clear":
        g.grid = [
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""]
            ]
    elif command == "Royalty":
        g.grid = [
                ["BG", "BG", "BG", "BG", "BG", "BG", "BG", "BG"],
                ["BG", "BG", "BG", "BG", "BG", "BG", "BG", "BG"],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["WG", "WG", "WG", "WG", "WG", "WG", "WG", "WG"],
                ["WG", "WG", "WG", "WG", "WG", "WG", "WG", "WG"]
            ]
    elif command == "Royalty2":
        g.grid = [
                ["BQ", "BQ", "BQ", "BQ", "BG", "BQ", "BQ", "BQ"],
                ["BQ", "BQ", "BQ", "BQ", "BQ", "BQ", "BQ", "BQ"],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["WQ", "WQ", "WQ", "WQ", "WQ", "WQ", "WQ", "WQ"],
                ["WQ", "WQ", "WQ", "WQ", "WG", "WQ", "WQ", "WQ"]
            ]
    elif command == "restart":
        g.grid = [
                ["BR", "BK", "BF", "BQ", "BG", "BF", "BK", "BR"],
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                ["WR", "WK", "WF", "WQ", "WG", "WF", "WK", "WR"],
            ]
    elif command == "fill":
        g.grid = [
                ["BR", "BK", "BF", "BQ", "BG", "BF", "BK", "BR"],
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
                ["WR", "WK", "WF", "WQ", "WG", "WF", "WK", "WR"]
            ]
    elif "pack" in command:
        args = command.split()
        args.append(None)
        global pack
        if args[1] == None:
                debug_message.append("Missing argument (1).")
                debug_time.append(pg.time.get_ticks())
        if args[1] == "list":
            debug_message.append(os.listdir("Assets"))
            debug_time.append(pg.time.get_ticks())
        if args[1] == "current":
            debug_message.append(pack)
            debug_time.append(pg.time.get_ticks())
        if args[1] == "set":
            if args[2] == None:
                debug_message.append("Missing argument (2).")
                debug_time.append(pg.time.get_ticks())
                return
            draw_debug_message()
            if args[2] in os.listdir("Assets"):
                pack = args[2]
                reload_assets()
                debug_message.append(f"Resource Pack set to {pack}")
                debug_time.append(pg.time.get_ticks())
                return
            debug_message.append(f"Pack {args[2]} not in Assets folder.")
            debug_time.append(pg.time.get_ticks())

    elif "set" in command:
        args = command.split()
        if args[0] == "set_volume":
            if args[1] == None:
                debug_message.append("Missing argument (1).")
                debug_time.append(pg.time.get_ticks())
            SOUNDTRACK.set_volume(float(args[1]))

    elif "spawn" in command:
        global grabbed
        global grabbed_pos
        args = command.split()
        mouse_pos = pg.mouse.get_pos()
        g.get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
        g.old_grid[g.grid_y][g.grid_x] = g.grid[g.grid_y][g.grid_x]
        g.grid[g.grid_y][g.grid_x] = g.grid[g.grid_y][g.grid_x] + "O"
        g.grabbed = args[1]
        g.grabbed_pos[0] = g.grid_y
        g.grabbed_pos[1] = g.grid_x
        g.find_pos(g.grabbed, g.grabbed_pos)


def handle_debugs(grabbed_unit, g):
    global debugs
    mouse_pos = pg.mouse.get_pos()
    tile = g.get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
    debugs[0] = "Mouse Pos: " + str(mouse_pos)
    debugs[1] = f"Grid Pos: ({g.grid_x}, {g.grid_y})"
    debugs[2] = f"Tile: {tile}"
    debugs[3] = f"Grabbed: {grabbed_unit}"
    debugs[4] = "Clock: " + str(pg.time.get_ticks())
    debugs[5] = "Volume: %" + str(SOUNDTRACK.get_volume()*100)


#Draw the screen
def draw_debug():
    y = -5
    for debug in debugs:
        draw_debug = SMALL_DEFAULT_FONT.render(str(debug), 1, GREEN)
        SCREEN.blit(draw_debug, (0, y))
        y += 20


def draw_debug_message():
    y = HEIGHT - 40
    for i in debug_message:
        y -= 20
    for debug in debug_message:
        draw_debug = SMALL_DEFAULT_FONT.render(str(debug), 1, GREEN)
        SCREEN.blit(draw_debug, (0, y))
        y += 20


def draw_console():
    text = SMALL_DEFAULT_FONT.render(console_text, 1, GREEN)
    SCREEN.blit(text, (10, HEIGHT - text.get_height() - 5))


def draw_screen(grid_size, cell_size, grabbed_unit, turn, check, board_set, move_y):
    bg = pg.Rect(0, move_y, WIDTH, HEIGHT)
    pg.draw.rect(SCREEN, (0, 150, 150), bg)
    draw_board(OFFSET_X, OFFSET_Y, grid_size, cell_size, move_y)
    if "W" in turn:
        colour = WHITE
    else:
        colour = BLACK
    title_text = NORMAL_DEFAULT_FONT.render(f"{turn}'s Turn!", 1, colour)
    SCREEN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, -5 + move_y))

    if "W" in check[0]:
        check_text1 = BIG_DEFAULT_FONT.render("CHECK! PANIC!", 1, BLUE)
        #check_text1 = pg.transform.rotate(check_text1, pg.time.get_ticks()//4)
        y = math.cos(pg.time.get_ticks()/150) * -100 + 600
        SCREEN.blit(check_text1, (WIDTH//2 - check_text1.get_width()//2, y))
    if "B" in check[1]:
        check_text2 = BIG_DEFAULT_FONT.render("CHECK! PANIC!", 1, RED)
        #check_text2 = pg.transform.rotate(check_text2, pg.time.get_ticks()//-4)
        y = math.cos(pg.time.get_ticks()/150) * 100
        SCREEN.blit(check_text2, (WIDTH//2 - check_text2.get_width()//2, y))

    if grabbed_unit != "":
        mouse_pos = pg.mouse.get_pos()
        if grabbed_unit == "BP":
            SCREEN.blit(BLACK_PAWN, (mouse_pos[0]-(BLACK_PAWN.get_width()//2), mouse_pos[1]-(BLACK_PAWN.get_height()//2) + move_y))
        elif grabbed_unit == "BK":
            SCREEN.blit(BLACK_KNIGHT_IMAGE, (mouse_pos[0]-(BLACK_KNIGHT_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_KNIGHT_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "BR":
            SCREEN.blit(BLACK_ROOK_IMAGE, (mouse_pos[0]-(BLACK_ROOK_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_ROOK_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "BF":
            SCREEN.blit(BLACK_BISHOP_IMAGE, (mouse_pos[0]-(BLACK_BISHOP_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_BISHOP_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "BQ":
            SCREEN.blit(BLACK_QUEEN_IMAGE, (mouse_pos[0]-(BLACK_QUEEN_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_QUEEN_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "BG":
            SCREEN.blit(BLACK_KING_IMAGE, (mouse_pos[0]-(BLACK_KING_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_KING_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "WP":
            SCREEN.blit(WHITE_PAWN, (mouse_pos[0]-(WHITE_PAWN.get_width()//2), mouse_pos[1]-(WHITE_PAWN.get_height()//2) + move_y))
        elif grabbed_unit == "WK":
            SCREEN.blit(WHITE_KNIGHT_IMAGE, (mouse_pos[0]-(WHITE_KNIGHT_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_KNIGHT_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "WR":
            SCREEN.blit(WHITE_ROOK_IMAGE, (mouse_pos[0]-(WHITE_ROOK_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_ROOK_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "WF":
            SCREEN.blit(WHITE_BISHOP_IMAGE, (mouse_pos[0]-(WHITE_BISHOP_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_BISHOP_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "WQ":
            SCREEN.blit(WHITE_QUEEN_IMAGE, (mouse_pos[0]-(WHITE_QUEEN_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_QUEEN_IMAGE.get_height()//2) + move_y))
        elif grabbed_unit == "WG":
            SCREEN.blit(WHITE_KING_IMAGE, (mouse_pos[0]-(WHITE_KING_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_KING_IMAGE.get_height()//2) + move_y))

    if show_debug:
        draw_debug()
    draw_debug_message()
    draw_console()
    pg.display.update()


def draw_board(offset_x, offset_y, grid_size, cell_size, m_y, g):
    move_y = offset_y
    colour = WHITE
    for cell_y in range(grid_size):
        move_x = offset_x
        for cell_x in range(grid_size):
            cell = pg.Rect(move_x, move_y + m_y, cell_size, cell_size)
            pg.draw.rect(SCREEN, colour, cell)
            if "BP" in g.grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_PAWN, (move_x, move_y + m_y))
            if "BK" in g.grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_KNIGHT_IMAGE, (move_x, move_y + m_y))
            if "BR" in g.grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_ROOK_IMAGE, (move_x, move_y + m_y))
            if "BF" in g.grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_BISHOP_IMAGE, (move_x, move_y + m_y))
            if "BQ" in g.grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_QUEEN_IMAGE, (move_x, move_y + m_y))
            if "BG" in g.grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_KING_IMAGE, (move_x, move_y + m_y))
                if "X" in g.grid[cell_y][cell_x]:
                    pg.draw.circle(SCREEN, RED, (move_x + (cell_size//2), move_y + (cell_size//2)), cell_size//3, 5)
                    pg.event.post(g.BLACK_CHECK_EVENT)
                else:
                    pg.event.post(g.NO_BLACK_CHECK_EVENT)
            if "WP" in g.grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_PAWN, (move_x, move_y + m_y))
            if "WK" in g.grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_KNIGHT_IMAGE, (move_x, move_y + m_y))
            if "WR" in g.grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_ROOK_IMAGE, (move_x, move_y + m_y))
            if "WF" in g.grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_BISHOP_IMAGE, (move_x, move_y + m_y))
            if "WQ" in g.grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_QUEEN_IMAGE, (move_x, move_y + m_y))
            if "WG" in g.grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_KING_IMAGE, (move_x, move_y + m_y))
                if "X" in grid[cell_y][cell_x]:
                    pg.draw.circle(SCREEN, RED, (move_x + (cell_size//2), move_y + (cell_size//2)), cell_size//3, 5)
                    pg.event.post(g.WHITE_CHECK_EVENT)
                else:
                    pg.event.post(g.NO_WHITE_CHECK_EVENT)

            if "O" in g.grid[cell_y][cell_x]:
                if len(g.grid[cell_y][cell_x]) > 1:
                    pg.draw.circle(SCREEN, RED, (move_x + (cell_size//2), move_y + (cell_size//2)), cell_size//3, 5)
                else:
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


#Draw the title screen
def draw_title(play_button):
    SCREEN.fill((0, 150, 150))
    title_text = BIG_DEFAULT_FONT.render("CHESS!!! PLAY NOW!", 1, WHITE)
    SCREEN.blit(title_text, ((WIDTH//2 - title_text.get_width()//2, 75)))
    pg.draw.rect(SCREEN, WHITE, play_button)
    play_text = NORMAL_DEFAULT_FONT.render("PLAY CHESS", 1, BLACK)
    SCREEN.blit(play_text, (WIDTH//2 - play_text.get_width()//2, play_button.y + 20))
    if show_debug:
        draw_debug()
    draw_debug_message()
    draw_console()
    pg.display.update()


def draw_retry_screen(move_y, retry_button, winner):
    bg = pg.Rect(0, move_y, WIDTH, HEIGHT)
    pg.draw.rect(SCREEN, (0, 150, 150), bg)

    title_text = BIG_DEFAULT_FONT.render(f"{winner} won! Replay?", 1, WHITE)
    SCREEN.blit(title_text, ((WIDTH//2 - title_text.get_width()//2, 75 + move_y)))
    pg.draw.rect(SCREEN, WHITE, retry_button)
    play_text = NORMAL_DEFAULT_FONT.render("PLAY CHESS", 1, BLACK)
    SCREEN.blit(play_text, (WIDTH//2 - play_text.get_width()//2, retry_button.y + 20))

    if show_debug:
        draw_debug()
    draw_debug_message()
    draw_console()
    pg.display.update()


def retry_screen(winner, g):
    global WIDTH
    global HEIGHT
    SOUNDTRACK.stop()
    move_y = HEIGHT * -1
    retry_button_bounds = [(WIDTH//2 - 150, WIDTH//2 - 150 + 300), (300, 400)]
    g.grid = [
            ["BR", "BK", "BF", "BQ", "BG", "BF", "BK", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WK", "WF", "WQ", "WG", "WF", "WK", "WR"],
        ]

    button_set = False
    clock = pg.time.Clock()
    run = True
    GAME_END.play()
    while run:
        WIDTH, HEIGHT = SCREEN.get_size()
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
           
            if event.type == REPEAT_SOUND:
                SOUNDTRACK.play()
           
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pressed()
                mouse_pos = pg.mouse.get_pos()
                if mouse[0] and ((mouse_pos[0] >=retry_button_bounds[0][0] and mouse_pos[0] <=retry_button_bounds[0][1]) and (mouse_pos[1] >=retry_button_bounds[1][0] and mouse_pos[1] <=retry_button_bounds[1][1])):
                    if button_set:
                        run = False
                        break
           
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
           
                if event.key == pg.K_F1 or event.key == pg.K_SLASH:
                        console = True
                        console_text = '>' + command
   
        if move_y < 0:
            move_y = g.clamp(move_y + 10, HEIGHT * -1, 0)
        else:
            button_set = True
       
        retry_button = pg.Rect(WIDTH//2 - 150, 300 + move_y, 300, 100)

        if show_debug:
            handle_debugs("O")
        draw_retry_screen(move_y, retry_button, winner)

    main()


#Title screen loop
def title():
    global WIDTH
    global HEIGHT

    pg.time.set_timer(REPEAT_SOUND, int(SOUNDTRACK.get_length() * 1000))
   
    clock = pg.time.Clock()
    run = True
    console = False
    global console_text
    global command
    SOUNDTRACK.play()
    while run:
        WIDTH, HEIGHT = SCREEN.get_size()
        play_button = pg.Rect(WIDTH//2 - 150, 300, 300, 100)
        play_bounds = [(WIDTH//2 - 150, WIDTH//2 - 150 + 300), (300, 400)]
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
           
            if event.type == REPEAT_SOUND:
                SOUNDTRACK.play()
           
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pressed()
                mouse_pos = pg.mouse.get_pos()
                if mouse[0] and ((mouse_pos[0] >=play_bounds[0][0] and mouse_pos[0] <=play_bounds[0][1]) and (mouse_pos[1] >=play_bounds[1][0] and mouse_pos[1] <=play_bounds[1][1])):
                    run = False
                    break

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
           
                if event.key == pg.K_F1 or event.key == pg.K_SLASH:
                        console = True
                        console_text = '>' + command
       
        if show_debug:
            handle_debugs("O")
       
        draw_title(play_button)

    main()


#Main game loop
def main():
    global WIDTH
    global HEIGHT
    global OFFSET_X
    global OFFSET_Y
    GAME_END.stop()
    pg.time.set_timer(REPEAT_SOUND, int(SOUNDTRACK.get_length() * 1000))
    clock = pg.time.Clock()
    move_y = HEIGHT * -1
    board_set = False
    run = True
    winner = "Jester"
    console = False
    check = ["", ""]
    n = network()
    global console_text
    global command
    global grid
    global old_grid
    global grabbed
    global grabbed_pos
    while run:
        try:
            g = n.send_data("get")
            WIDTH, HEIGHT = SCREEN.get_size()
            OFFSET_X = WIDTH//2-(g.GRID_SIZE*g.CELL_SIZE//2)
            OFFSET_Y = HEIGHT//2-(g.GRID_SIZE*g.CELL_SIZE//2)+20
        except Exception as e:
            print(e)
            run = False
            print("1Couldn't get game")
            break

        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
           
            if event.type == REPEAT_SOUND:
                SOUNDTRACK.play()
               
            if board_set:
                if event.type == pg.USEREVENT:
                    if event.MyOwnType == g.ON_WHITE_CHECK:
                        check[0] = "White"
                    if event.MyOwnType == g.ON_BLACK_CHECK:
                        check[1] = "Black"
                    if event.MyOwnType == g.ON_NO_WHITE_CHECK:
                        check[0] = ""
                    if event.MyOwnType == g.ON_NO_BLACK_CHECK:
                        check[1] = ""
               
                if event.type == pg.USEREVENT + 2:
                    if event.MyOwnType == g.ON_RETRY:
                        run = False
               
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pressed()
                    if mouse[0]:
                        mouse_pos = pg.mouse.get_pos()
                        tile = g.get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
                        if g.grabbed == "":
                            if not g.turn[:1] in g.grid[g.grid_y][g.grid_x]:
                                continue
                            g.old_grid[g.grid_y][g.grid_x] = g.grid[g.grid_y][g.grid_x]
                            g.grabbed = g.grid[g.grid_y][g.grid_x].replace("O", "")
                            g.grabbed_pos[0] = g.grid_y
                            g.grabbed_pos[1] = g.grid_x
                            g.find_pos(g.grabbed, g.grabbed_pos)
                            g.grid[g.grid_y][g.grid_x] = ""
                        else:
                            if "O" in g.grid[g.grid_y][g.grid_x]:
                                g.remove_pos()
                                if "WP" in g.grabbed and g.grid_y == 0:
                                    g.grabbed = "WQ"
                                if "BP" in g.grabbed and g.grid_y == 7:
                                    g.grabbed = "BQ"
                                if "G" in g.grid[g.grid_y][g.grid_x]:
                                    if "W" in g.grid[g.grid_y][g.grid_x]:
                                        winner = "Black"
                                    if "B" in g.grid[g.grid_y][g.grid_x]:
                                        winner = "White"
                                    run = False
                                g.grid[g.grid_y][g.grid_x] = g.grabbed
                                g.remove_pos()
                                g.check_check()
                                g.grabbed = ""
                                if "W" in turn:
                                    turn = "Black"
                                else:
                                    turn = "White"

                            else:
                                g.grid[g.grabbed_pos[0]][g.grabbed_pos[1]] = g.old_grid[g.grabbed_pos[0]][g.grabbed_pos[1]]
                                g.remove_pos()
                                g.check_check()
                                g.grabbed = ""


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
           
                if event.key == pg.K_F1 or event.key == pg.K_SLASH:
                        console = True
                        console_text = '>' + command


        if show_debug:
            handle_debugs(grabbed)
       
        if move_y < 0:
            move_y = g.clamp(move_y + 10, HEIGHT * -1, 0)
        else:
            board_set = True
       
        for debug in range(len(debug_message)):
            if pg.time.get_ticks() - debug_time[debug-1] >= 5000:
                debug_message.pop(debug-1)
                debug_time.pop(debug-1)
       
        draw_screen(g.GRID_SIZE, g.CELL_SIZE, g.grabbed, g.turn, check, board_set, move_y)

    pg.time.wait(500)
    retry_screen(winner)


if __name__ == "__main__":
    title()