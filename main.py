import pygame as pg
import math
import os
import json
import datetime

#Init stuffs
pg.mixer.init()
pg.font.init()
pg.init()
pg.display.set_caption("WOOOO CHESS!")
pack = "Default"

#Const Var Inits

WIDTH = 900
HEIGHT = 700
SCREEN = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
GRID_SIZE = 8
CELL_SIZE = 80
OFFSET_X = WIDTH//2-(GRID_SIZE*CELL_SIZE//2)
OFFSET_Y = HEIGHT//2-(GRID_SIZE*CELL_SIZE//2)+20

FPS = 60

#Move Dictionaries
BLACK_MOVES = {"Pawn":[(1, 0)]}
WHITE_MOVES = {"Pawn":[(-1, 0)]}
MOVES = {
    "Knight":[(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)],
    "Rook":(4, 8),
    "Bishop": (4, 8),
    "Queen": (8, 8),
    "King": [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    }


#Custom Event ID's
ON_WHITE_CHECK = 1
ON_BLACK_CHECK = 2
ON_NO_WHITE_CHECK = 3
ON_NO_BLACK_CHECK = 4
#Command Events
ON_RETRY = 1

#Events
REPEAT_SOUND = pg.USEREVENT + 1
#Check Events
WHITE_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=ON_WHITE_CHECK)
BLACK_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=ON_BLACK_CHECK)
NO_WHITE_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=ON_NO_WHITE_CHECK)
NO_BLACK_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=ON_NO_BLACK_CHECK)
#Command Events
RETRY = pg.event.Event(pg.USEREVENT + 2, MyOwnType=ON_RETRY)

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
    ["1BR", "1BK", "1BF", "BQ", "BG", "2BF", "2BK", "2BR"],
    ["1BP", "2BP", "3BP", "4BP", "5BP", "6BP", "7BP", "8BP"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["1WP", "2WP", "3WP", "4WP", "5WP", "6WP", "7WP", "8WP"],
    ["1WR", "1WK", "1WF", "WQ", "WG", "2WF", "2WK", "2WR"],
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


class button():
    def __init__(self, pos, size, text, colour):
        self.pos = pos
        self.size = size
        self.text = text
        self.colour = colour

    def draw(self, screen):
        pg.draw.rect(screen, self.colour, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        text = NORMAL_DEFAULT_FONT.render(self.text, 1, BLACK)
        screen.blit(text, (self.pos[0]+self.size[0]//2-text.get_width()//2, self.pos[1]+self.size[1]//2-text.get_height()//2))
    
    def click(self, pos):
        if self.pos[0] <= pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= pos[1] <= self.pos[1] + self.size[1]:
            return True
        else:
            return False


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


#Custom clamp function to keep grid index in range
def clamp(val, min, max):
    if val > max:
        val = max
    if val < min:
        val = min
    return val


def save(board):
    time_stamp = datetime.datetime.now()
    with open(os.path.join("Saves/", f"save-{time_stamp}"), "x") as f:
        json.dumps(board)


#Handle the logic
def get_tile(x, y, offset_x, offset_y):
    global grid_x
    global grid_y
    global tile
    grid_x = clamp(math.floor((x - offset_x)//CELL_SIZE), 0, 7)
    grid_y = clamp(math.floor((y - offset_y)//CELL_SIZE), 0, 7)
    tile = grid[grid_y][grid_x]


def handle_commands():
    global show_debug
    global grid
    global grid_x
    global grid_y
    if command == "debug":
        if show_debug:
            show_debug = False
            return
        show_debug = True
    elif command == "retry":
        pg.event.post(RETRY)

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
    elif command == "Royalty":
        grid = [
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
        grid = [
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
        grid = [
                ["1BR", "1BK", "1BF", "BQ", "BG", "2BF", "2BK", "2BR"],
                ["1BP", "2BP", "3BP", "4BP", "5BP", "6BP", "7BP", "8BP"],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["", "", "", "", "", "", "", ""],
                ["1WP", "2WP", "3WP", "4WP", "5WP", "6WP", "7WP", "8WP"],
                ["1WR", "1WK", "1WF", "WQ", "WG", "2WF", "2WK", "2WR"],
            ]
    elif command == "fill":
        grid = [
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
        get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
        old_grid[grid_y][grid_x] = grid[grid_y][grid_x]
        grid[grid_y][grid_x] = grid[grid_y][grid_x] + "O"
        grabbed = args[1]
        grabbed_pos[0] = grid_y
        grabbed_pos[1] = grid_x
        find_pos(grabbed, grabbed_pos)


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


def handle_check(grabbed_unit, grabbed_pos):
    if "G" in grabbed_unit:
        for possible  in MOVES["King"]:
            possible_x = grabbed_pos[1] + possible[1]
            possible_y = grabbed_pos[0] + possible[0]
            if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                continue
            if "W" in grid[possible_y][possible_x] and "W" in grabbed_unit:
                continue
            if "B" in grid[possible_y][possible_x] and "B" in grabbed_unit:
                continue
            if "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"

    if "Q" in grabbed_unit:
        direction = 1
        for i in range(MOVES["Queen"][0]):
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0]
            for possible in range(MOVES["Queen"][1]):
                if direction == 1:#|
                    possible_y = possible_y - 1
                elif direction == 2:#/
                    possible_x = possible_x + 1
                    possible_y = possible_y - 1
                elif direction == 3:#-
                    possible_x = possible_x + 1
                elif direction == 4:#\
                    possible_x = possible_x + 1
                    possible_y = possible_y + 1
                elif direction == 5:#|
                    possible_y = possible_y + 1
                elif direction == 6:#/
                    possible_x = possible_x - 1
                    possible_y = possible_y + 1
                elif direction == 7:#-
                    possible_x = possible_x - 1
                elif direction == 8:#\
                    possible_x = possible_x - 1
                    possible_y = possible_y - 1
                
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue
                
                if "W" in grid[possible_y][possible_x]:
                    if "B" in grabbed_unit and "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"
                    break
                elif "B" in grid[possible_y][possible_x]:
                    if "W" in grabbed_unit and "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"
                    break
            direction += 1

    if "F" in grabbed_unit:
        direction = 1
        for i in range(MOVES["Bishop"][0]):
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0]
            for possible in range(MOVES["Bishop"][1]):
                if direction == 1:
                    possible_x = possible_x + 1
                    possible_y = possible_y + 1
                elif direction == 2:
                    possible_x = possible_x + 1
                    possible_y = possible_y - 1
                elif direction == 3:
                    possible_x = possible_x - 1
                    possible_y = possible_y - 1
                elif direction == 4:
                    possible_x = possible_x - 1
                    possible_y = possible_y + 1
                
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue

                if "W" in grid[possible_y][possible_x]:
                    if "B" in grabbed_unit and "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"
                    break
                elif "B" in grid[possible_y][possible_x]:
                    if "W" in grabbed_unit and "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"
                    break
            direction += 1

    if "R" in grabbed_unit:
        direction = 1
        for i in range(MOVES["Rook"][0]):
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0]
            for possible in range(MOVES["Rook"][1]):
                if direction == 1:
                    possible_y = clamp(possible_y + 1, 0, 7)
                elif direction == 2:
                    possible_x = clamp(possible_x + 1, 0, 7)
                elif direction == 3:
                    possible_y = clamp(possible_y - 1, 0, 7)
                elif direction == 4:
                    possible_x = clamp(possible_x - 1, 0, 7)

                if "W" in grid[possible_y][possible_x]:
                    if "B" in grabbed_unit and "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"
                    break
                elif "B" in grid[possible_y][possible_x]:
                    if "W" in grabbed_unit and "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"
                    break
            direction += 1

    if "K" in grabbed_unit:
        for possible  in MOVES["Knight"]:
            possible_x = grabbed_pos[1] + possible[1]
            possible_y = grabbed_pos[0] + possible[0]
            if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                continue
            if "W" in grid[possible_y][possible_x] and "W" in grabbed_unit:
                continue
            if "B" in grid[possible_y][possible_x] and "B" in grabbed_unit:
                continue
            if "G" in grid[possible_y][possible_x] and "X" not in grid[possible_y][possible_x]:
                grid[possible_y][possible_x] = grid[possible_y][possible_x] + "X"

    if "BP" in grabbed_unit:
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + BLACK_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1

        if possible_y > 7:
            return

        if kill_x1 <= 7 and "W" in grid[possible_y][kill_x1] and "G" in grid[possible_y][kill_x1] and "X" not in grid[possible_y][kill_x1]:
            grid[possible_y][kill_x1] = grid[possible_y][kill_x1] + "X"
        if kill_x2 >= 0 and "W" in grid[possible_y][kill_x2] and "G" in grid[possible_y][kill_x2] and "X" not in grid[possible_y][kill_x2]:
            grid[possible_y][kill_x2] = grid[possible_y][kill_x2] + "X"
            
    if "WP" in grabbed_unit:
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + WHITE_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1

        if possible_y < 0:
            return

        if kill_x1 <= 7 and "B" in grid[possible_y][kill_x1] and "G" in grid[possible_y][kill_x1] and "X" not in grid[possible_y][kill_x1]:
            grid[possible_y][kill_x1] = grid[possible_y][kill_x1] + "X"
        if kill_x2 >= 0 and "B" in grid[possible_y][kill_x2] and "G" in grid[possible_y][kill_x2] and "X" not in grid[possible_y][kill_x2]:
            grid[possible_y][kill_x2] = grid[possible_y][kill_x2] + "X"


def check_check():
    global grid
    for cell_y in range(GRID_SIZE):
        for cell_x in range(GRID_SIZE):
            handle_check(grid[cell_y][cell_x], (cell_y, cell_x))


#Find all the valid locations to move
def find_pos(grabbed_unit, grabbed_pos):
    if "G" in grabbed_unit:
        for possible  in MOVES["King"]:
            possible_x = grabbed_pos[1] + possible[1]
            possible_y = grabbed_pos[0] + possible[0]
            if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                continue
            if "W" in grid[possible_y][possible_x] and "W" in grabbed_unit:
                continue
            if "B" in grid[possible_y][possible_x] and "B" in grabbed_unit:
                continue
            grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"

    if "Q" in grabbed_unit:
        direction = 1
        for i in range(MOVES["Queen"][0]):
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0]
            for possible in range(MOVES["Queen"][1]):
                if direction == 1:#|
                    possible_y = possible_y - 1
                elif direction == 2:#/
                    possible_x = possible_x + 1
                    possible_y = possible_y - 1
                elif direction == 3:#-
                    possible_x = possible_x + 1
                elif direction == 4:#\
                    possible_x = possible_x + 1
                    possible_y = possible_y + 1
                elif direction == 5:#|
                    possible_y = possible_y + 1
                elif direction == 6:#/
                    possible_x = possible_x - 1
                    possible_y = possible_y + 1
                elif direction == 7:#-
                    possible_x = possible_x - 1
                elif direction == 8:#\
                    possible_x = possible_x - 1
                    possible_y = possible_y - 1
                
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue

                if grid[possible_y][possible_x] == "":
                    grid[possible_y][possible_x] = "O"
                elif "W" in grid[possible_y][possible_x]:
                    if "B" in grabbed_unit:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"
                    break
                elif "B" in grid[possible_y][possible_x]:
                    if "W" in grabbed_unit:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"
                    break
            direction += 1

    if "F" in grabbed_unit:
        direction = 1
        for i in range(MOVES["Bishop"][0]):
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0]
            for possible in range(MOVES["Bishop"][1]):
                if direction == 1:
                    possible_x = possible_x + 1
                    possible_y = possible_y + 1
                elif direction == 2:
                    possible_x = possible_x + 1
                    possible_y = possible_y - 1
                elif direction == 3:
                    possible_x = possible_x - 1
                    possible_y = possible_y - 1
                elif direction == 4:
                    possible_x = possible_x - 1
                    possible_y = possible_y + 1
                
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue

                if grid[possible_y][possible_x] == "":
                    grid[possible_y][possible_x] = "O"
                elif "W" in grid[possible_y][possible_x]:
                    if "B" in grabbed_unit:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"
                    break
                elif "B" in grid[possible_y][possible_x]:
                    if "W" in grabbed_unit:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"
                    break
            direction += 1

    if "R" in grabbed_unit:
        direction = 1
        for i in range(MOVES["Rook"][0]):
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0]
            for possible in range(MOVES["Rook"][1]):
                if direction == 1:
                    possible_y = clamp(possible_y + 1, 0, 7)
                elif direction == 2:
                    possible_x = clamp(possible_x + 1, 0, 7)
                elif direction == 3:
                    possible_y = clamp(possible_y - 1, 0, 7)
                elif direction == 4:
                    possible_x = clamp(possible_x - 1, 0, 7)

                if grid[possible_y][possible_x] == "":
                    grid[possible_y][possible_x] = "O"
                elif "W" in grid[possible_y][possible_x]:
                    if "B" in grabbed_unit:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"
                    break
                elif "B" in grid[possible_y][possible_x]:
                    if "W" in grabbed_unit:
                        grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"
                    break
            direction += 1

    if "K" in grabbed_unit:
        for possible  in MOVES["Knight"]:
            possible_x = grabbed_pos[1] + possible[1]
            possible_y = grabbed_pos[0] + possible[0]
            if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                continue
            if "W" in grid[possible_y][possible_x] and "W" in grabbed_unit:
                continue
            if "B" in grid[possible_y][possible_x] and "B" in grabbed_unit:
                continue
            grid[possible_y][possible_x] = grid[possible_y][possible_x] + "O"

    if "BP" in grabbed_unit:
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + BLACK_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1

        if possible_y > 7:
            return

        if grid[possible_y][possible_x] == "":
            grid[possible_y][possible_x] = "O"
            if grid[clamp(possible_y+1, 0, 7)][possible_x] == "" and grabbed_pos[0] == 1:
                grid[clamp(possible_y+1, 0, 7)][possible_x] = "O"

        if kill_x1 <= 7 and "W" in grid[possible_y][kill_x1]:
            grid[possible_y][kill_x1] = grid[possible_y][kill_x1] + "O"
        if kill_x2 >= 0 and "W" in grid[possible_y][kill_x2]:
            grid[possible_y][kill_x2] = grid[possible_y][kill_x2] + "O"
            
    if "WP" in grabbed_unit:
        possible_x = grabbed_pos[1]
        possible_y = grabbed_pos[0] + WHITE_MOVES["Pawn"][0][0]
        kill_x1 = grabbed_pos[1] + 1
        kill_x2 = grabbed_pos[1] - 1

        if possible_y < 0:
            return
    
        if grid[possible_y][possible_x] == "":
            grid[possible_y][possible_x] = "O"
            if grid[clamp(possible_y-1, 0, 7)][possible_x] == "" and grabbed_pos[0] == 6:
                grid[clamp(possible_y-1, 0, 7)][possible_x] = "O"

        if kill_x1 <= 7 and "B" in grid[possible_y][kill_x1]:
            grid[possible_y][kill_x1] = grid[possible_y][kill_x1] + "O"
        if kill_x2 >= 0 and "B" in grid[possible_y][kill_x2]:
            grid[possible_y][kill_x2] = grid[possible_y][kill_x2] + "O"

#Because it doesn't like removing circles
def remove_pos(grabbed_unit, grabbed_pos):
    global grid
    for cell_y in range(GRID_SIZE):
        for cell_x in range(GRID_SIZE):
            point = grid[cell_y][cell_x].replace("O", "")
            grid[cell_y][cell_x] = point
            point = grid[cell_y][cell_x].replace("X", "")
            grid[cell_y][cell_x] = point
            check_check()

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


def draw_screen(grid_size, cell_size, grabbed_unit, turn, check, board, move_y, save_button):
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
        if "BP" in grabbed_unit:
            SCREEN.blit(BLACK_PAWN, (mouse_pos[0]-(BLACK_PAWN.get_width()//2), mouse_pos[1]-(BLACK_PAWN.get_height()//2) + move_y))
        if "BK" in grabbed_unit:
            SCREEN.blit(BLACK_KNIGHT_IMAGE, (mouse_pos[0]-(BLACK_KNIGHT_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_KNIGHT_IMAGE.get_height()//2) + move_y))
        if "BR" in grabbed_unit:
            SCREEN.blit(BLACK_ROOK_IMAGE, (mouse_pos[0]-(BLACK_ROOK_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_ROOK_IMAGE.get_height()//2) + move_y))
        if "BF" in grabbed_unit:
            SCREEN.blit(BLACK_BISHOP_IMAGE, (mouse_pos[0]-(BLACK_BISHOP_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_BISHOP_IMAGE.get_height()//2) + move_y))
        if "BQ" in grabbed_unit:
            SCREEN.blit(BLACK_QUEEN_IMAGE, (mouse_pos[0]-(BLACK_QUEEN_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_QUEEN_IMAGE.get_height()//2) + move_y))
        if "BG" in grabbed_unit:
            SCREEN.blit(BLACK_KING_IMAGE, (mouse_pos[0]-(BLACK_KING_IMAGE.get_width()//2), mouse_pos[1]-(BLACK_KING_IMAGE.get_height()//2) + move_y))
        if "WP" in grabbed_unit:
            SCREEN.blit(WHITE_PAWN, (mouse_pos[0]-(WHITE_PAWN.get_width()//2), mouse_pos[1]-(WHITE_PAWN.get_height()//2) + move_y))
        if "WK" in grabbed_unit:
            SCREEN.blit(WHITE_KNIGHT_IMAGE, (mouse_pos[0]-(WHITE_KNIGHT_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_KNIGHT_IMAGE.get_height()//2) + move_y))
        if "WR" in grabbed_unit:
            SCREEN.blit(WHITE_ROOK_IMAGE, (mouse_pos[0]-(WHITE_ROOK_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_ROOK_IMAGE.get_height()//2) + move_y))
        if "WF" in grabbed_unit:
            SCREEN.blit(WHITE_BISHOP_IMAGE, (mouse_pos[0]-(WHITE_BISHOP_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_BISHOP_IMAGE.get_height()//2) + move_y))
        if "WQ" in grabbed_unit:
            SCREEN.blit(WHITE_QUEEN_IMAGE, (mouse_pos[0]-(WHITE_QUEEN_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_QUEEN_IMAGE.get_height()//2) + move_y))
        if "WG" in grabbed_unit:
            SCREEN.blit(WHITE_KING_IMAGE, (mouse_pos[0]-(WHITE_KING_IMAGE.get_width()//2), mouse_pos[1]-(WHITE_KING_IMAGE.get_height()//2) + move_y))

    draw_moves(board)
    save_button.draw(SCREEN)

    if show_debug:
        draw_debug()
    draw_debug_message()
    draw_console()
    pg.display.update()


def draw_moves(board):
    y = -20
    for i in board:
        y += 20
    for move in board:
        if "B" in move:
            colour = BLACK
        else:
            colour = WHITE
        draw_move = SMALL_DEFAULT_FONT.render(str(move), 1, colour)
        SCREEN.blit(draw_move, (WIDTH-draw_move.get_width(), y))
        y -= 20


def draw_board(offset_x, offset_y, grid_size, cell_size, m_y):
    move_y = offset_y
    colour = WHITE
    for cell_y in range(grid_size):
        move_x = offset_x
        for cell_x in range(grid_size):
            cell = pg.Rect(move_x, move_y + m_y, cell_size, cell_size)
            pg.draw.rect(SCREEN, colour, cell)
            if "BP" in grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_PAWN, (move_x, move_y + m_y))
            if "BK" in grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_KNIGHT_IMAGE, (move_x, move_y + m_y))
            if "BR" in grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_ROOK_IMAGE, (move_x, move_y + m_y))
            if "BF" in grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_BISHOP_IMAGE, (move_x, move_y + m_y))
            if "BQ" in grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_QUEEN_IMAGE, (move_x, move_y + m_y))
            if "BG" in grid[cell_y][cell_x]:
                SCREEN.blit(BLACK_KING_IMAGE, (move_x, move_y + m_y))
                if "X" in grid[cell_y][cell_x]:
                    pg.draw.circle(SCREEN, RED, (move_x + (cell_size//2), move_y + (cell_size//2)), cell_size//3, 5)
                    pg.event.post(BLACK_CHECK_EVENT)
                else:
                    pg.event.post(NO_BLACK_CHECK_EVENT)
            if "WP" in grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_PAWN, (move_x, move_y + m_y))
            if "WK" in grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_KNIGHT_IMAGE, (move_x, move_y + m_y))
            if "WR" in grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_ROOK_IMAGE, (move_x, move_y + m_y))
            if "WF" in grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_BISHOP_IMAGE, (move_x, move_y + m_y))
            if "WQ" in grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_QUEEN_IMAGE, (move_x, move_y + m_y))
            if "WG" in grid[cell_y][cell_x]:
                SCREEN.blit(WHITE_KING_IMAGE, (move_x, move_y + m_y))
                if "X" in grid[cell_y][cell_x]:
                    pg.draw.circle(SCREEN, RED, (move_x + (cell_size//2), move_y + (cell_size//2)), cell_size//3, 5)
                    pg.event.post(WHITE_CHECK_EVENT)
                else:
                    pg.event.post(NO_WHITE_CHECK_EVENT)

            if "O" in grid[cell_y][cell_x]:
                if len(grid[cell_y][cell_x]) > 1:
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
    play_button.draw(SCREEN)
    #play_text = NORMAL_DEFAULT_FONT.render("PLAY CHESS", 1, BLACK)
    #SCREEN.blit(play_text, (WIDTH//2 - play_text.get_width()//2, play_button.y + 20))
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
    retry_button.draw(SCREEN)
    #SCREEN.blit(play_text, (WIDTH//2 - play_text.get_width()//2, retry_button.y + 20))

    if show_debug:
        draw_debug()
    draw_debug_message()
    draw_console()
    pg.display.update()


def retry_screen(winner):
    global WIDTH
    global HEIGHT
    global grid
    SOUNDTRACK.stop()
    move_y = HEIGHT * -1
    retry_button = button((WIDTH//2-150, HEIGHT//2-50), (300, 100), "Replay?", WHITE)

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
                if mouse[0] and retry_button.click(mouse_pos):
                    if button_set:
                        run = False
                        grid = [
                            ["1BR", "1BK", "1BF", "BQ", "BG", "2BF", "2BK", "2BR"],
                            ["1BP", "2BP", "3BP", "4BP", "5BP", "6BP", "7BP", "8BP"],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["1WP", "2WP", "3WP", "4WP", "5WP", "6WP", "7WP", "8WP"],
                            ["1WR", "1WK", "1WF", "WQ", "WG", "2WF", "2WK", "2WR"],
                        ]
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
            move_y = clamp(move_y + 10, HEIGHT * -1, 0)
            retry_button.pos = (WIDTH//2-150, HEIGHT//2-50+move_y)
        else:
            button_set = True

        if show_debug:
            handle_debugs("O")
        draw_retry_screen(move_y, retry_button, winner)

    main()


#Title screen loop
def title():
    global WIDTH
    global HEIGHT

    pg.time.set_timer(REPEAT_SOUND, int(SOUNDTRACK.get_length() * 1000))
    play_button = button((WIDTH//2-150, HEIGHT//2-50), (300, 100), "PLAY CHESS!", WHITE)
    
    clock = pg.time.Clock()
    run = True
    console = False
    global console_text
    global command
    SOUNDTRACK.play()
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
                if mouse[0] and play_button.click(mouse_pos):
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
    save_button = button((50, HEIGHT-50), (40, 40), "S", WHITE)
    move_y = HEIGHT * -1
    board_set = False
    run = True
    turn = "White"
    winner = "Jester"
    console = False
    check = ["", ""]
    queen_count = [0, 0]
    board = []
    global console_text
    global command
    global grid
    global old_grid
    global grabbed
    global grabbed_pos
    while run:
        WIDTH, HEIGHT = SCREEN.get_size()
        OFFSET_X = WIDTH//2-(GRID_SIZE*CELL_SIZE//2)
        OFFSET_Y = HEIGHT//2-(GRID_SIZE*CELL_SIZE//2)+20
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.display.quit()
            
            if event.type == REPEAT_SOUND:
                SOUNDTRACK.play()
                
            if board_set:
                if event.type == pg.USEREVENT:
                    if event.MyOwnType == ON_WHITE_CHECK:
                        check[0] = "White"
                    if event.MyOwnType == ON_BLACK_CHECK:
                        check[1] = "Black"
                    if event.MyOwnType == ON_NO_WHITE_CHECK:
                        check[0] = ""
                    if event.MyOwnType == ON_NO_BLACK_CHECK:
                        check[1] = ""
                
                if event.type == pg.USEREVENT + 2:
                    if event.MyOwnType == ON_RETRY:
                        run = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse = pg.mouse.get_pressed()
                    mouse_pos = pg.mouse.get_pos()
                    if mouse[0]:
                        get_tile(mouse_pos[0], mouse_pos[1], OFFSET_X, OFFSET_Y)
                        if grabbed == "":
                            if not turn[:1] in grid[grid_y][grid_x]:
                                continue
                            old_grid[grid_y][grid_x] = grid[grid_y][grid_x]
                            grabbed = grid[grid_y][grid_x].replace("O", "")
                            grabbed_pos[0] = grid_y
                            grabbed_pos[1] = grid_x
                            find_pos(grabbed, grabbed_pos)
                            grid[grid_y][grid_x] = ""
                        else:
                            if "O" in grid[grid_y][grid_x]:
                                board.append(grabbed+str(grabbed_pos[0])+str(grabbed_pos[1]))
                                remove_pos(grabbed, grabbed_pos)
                                if "WP" in grabbed and grid_y == 0:
                                    queen_count[0] += 1
                                    grabbed = f"WQ{queen_count[0]}"
                                if "BP" in grabbed and grid_y == 7:
                                    queen_count[1] += 1
                                    grabbed = f"BQ{queen_count[1]}"
                                if "G" in grid[grid_y][grid_x]:
                                    if "W" in grid[grid_y][grid_x]:
                                        winner = "Black"
                                    if "B" in grid[grid_y][grid_x]:
                                        winner = "White"
                                    run = False
                                grid[grid_y][grid_x] = grabbed
                                remove_pos(grabbed, grabbed_pos)
                                check_check()
                                grabbed = ""
                                if "W" in turn:
                                    turn = "Black"
                                else:
                                    turn = "White"

                            else:
                                grid[grabbed_pos[0]][grabbed_pos[1]] = old_grid[grabbed_pos[0]][grabbed_pos[1]]
                                remove_pos(grabbed, grabbed_pos)
                                check_check()
                                grabbed = ""
                            
                        if mouse[0] and save_button.click(mouse_pos):
                            save(board)

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
            move_y = clamp(move_y + 10, HEIGHT * -1, 0)
        else:
            board_set = True
        
        for debug in range(len(debug_message)):
            if pg.time.get_ticks() - debug_time[debug-1] >= 5000:
                debug_message.pop(debug-1)
                debug_time.pop(debug-1)

        draw_screen(GRID_SIZE, CELL_SIZE, grabbed, turn, check, board, move_y, save_button)

    pg.time.wait(500)
    retry_screen(winner)


if __name__ == "__main__":
    title()