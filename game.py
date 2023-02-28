import pygame as pg
import math

class Game():
    def __init__(self, id):
        self.id = id
        self.GRID_SIZE = 8
        self.CELL_SIZE = 80
        self.BLACK_MOVES = {"Pawn":[(1, 0)]}
        self.WHITE_MOVES = {"Pawn":[(-1, 0)]}
        self.MOVES = {
                "Knight":[(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)],
                "Rook":(4, 8),
                "Bishop": (4, 8),
                "Queen": (8, 8),
                "King": [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
                }
        
        #Custom Event ID's
        self.ON_WHITE_CHECK = 1
        self.ON_BLACK_CHECK = 2
        self.ON_NO_WHITE_CHECK = 3
        self.ON_NO_BLACK_CHECK = 4
        #Command Events
        self.ON_RETRY = 1

        #Check Events
        self.WHITE_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=self.ON_WHITE_CHECK)
        self.BLACK_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=self.ON_BLACK_CHECK)
        self.NO_WHITE_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=self.ON_NO_WHITE_CHECK)
        self.NO_BLACK_CHECK_EVENT = pg.event.Event(pg.USEREVENT, MyOwnType=self.ON_NO_BLACK_CHECK)
        #Command Events
        self.RETRY = pg.event.Event(pg.USEREVENT + 2, MyOwnType=self.ON_RETRY)

        #Global Vars
        self.turn = "White"
        self.grid = [
            ["BR", "BK", "BF", "BQ", "BG", "BF", "BK", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WK", "WF", "WQ", "WG", "WF", "WK", "WR"],
        ]
        self.old_grid = [
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
        ]
        self.grid_x = 0
        self.grid_y = 0
        self.grabbed = ""
        self.grabbed_pos = [0, 0]
        self.tile = ""
        self.console_text = ''
        self.command = ''
        self.show_debug = False
        self.debug_message = []
        self.debug_time = []
        self.debugs = [
            "Mouse Pos: ",
            "Grid Pos: ",
            "Tile: ",
            "Grabbed: ",
            "Clock: ",
            "Volume: "
        ]
    
    def reset(self):
        self.grid = [
            ["BR", "BK", "BF", "BQ", "BG", "BF", "BK", "BR"],
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"],
            ["WR", "WK", "WF", "WQ", "WG", "WF", "WK", "WR"],
        ]
        self.turn = "White"
    
    #Custom clamp function to keep grid index in range
    def clamp(self, val, min, max):
        if val > max:
            val = max
        if val < min:
            val = min
        return val
    
    def get_tile(self, x, y, offset_x, offset_y):
        self.grid_x = self.clamp(math.floor((x - offset_x)/self.CELL_SIZE), 0, 7)
        self.grid_y = self.clamp(math.floor((y - offset_y)//self.CELL_SIZE), 0, 7)
        self.tile = self.grid[self.grid_y][self.grid_x]
        return self.tile
    
    def handle_check(self, grabbed_unit, grabbed_pos):
        if "G" in grabbed_unit:
            for possible  in self.MOVES["King"]:
                possible_x = grabbed_pos[1] + possible[1]
                possible_y = grabbed_pos[0] + possible[0]
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue
                if "W" in self.grid[possible_y][possible_x] and "W" in grabbed_unit:
                    continue
                if "B" in self.grid[possible_y][possible_x] and "B" in grabbed_unit:
                    continue
                if "G" in self.grid[possible_y][possible_x]:
                    self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"

        if "Q" in grabbed_unit:
            direction = 1
            for i in range(self.MOVES["Queen"][0]):
                possible_x = grabbed_pos[1]
                possible_y = grabbed_pos[0]
                for possible in range(self.MOVES["Queen"][1]):
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
                
                    if "W" in self.grid[possible_y][possible_x]:
                        if "B" in grabbed_unit and "G" in self.grid[possible_y][possible_x]:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"
                        break
                    elif "B" in self.grid[possible_y][possible_x]:
                        if "W" in grabbed_unit and "G" in self.grid[possible_y][possible_x]:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"
                        break
                direction += 1


        if "F" in grabbed_unit:
            direction = 1
            for i in range(self.MOVES["Bishop"][0]):
                possible_x = grabbed_pos[1]
                possible_y = grabbed_pos[0]
                for possible in range(self.MOVES["Bishop"][1]):
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

                    if "W" in self.grid[possible_y][possible_x]:
                        if "B" in grabbed_unit and "G" in self.grid[possible_y][possible_x]:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"
                        break
                    elif "B" in self.grid[possible_y][possible_x]:
                        if "W" in grabbed_unit and "G" in self.grid[possible_y][possible_x]:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"
                        break
                direction += 1

        if "R" in grabbed_unit:
            direction = 1
            for i in range(self.MOVES["Rook"][0]):
                possible_x = grabbed_pos[1]
                possible_y = grabbed_pos[0]
                for possible in range(self.MOVES["Rook"][1]):
                    if direction == 1:
                        possible_y = self.clamp(possible_y + 1, 0, 7)
                    elif direction == 2:
                        possible_x = self.clamp(possible_x + 1, 0, 7)
                    elif direction == 3:
                        possible_y = self.clamp(possible_y - 1, 0, 7)
                    elif direction == 4:
                        possible_x = self.clamp(possible_x - 1, 0, 7)

                    if "W" in self.grid[possible_y][possible_x]:
                        if "B" in grabbed_unit and "G" in self.grid[possible_y][possible_x]:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"
                        break
                    elif "B" in self.grid[possible_y][possible_x]:
                        if "W" in grabbed_unit and "G" in self.grid[possible_y][possible_x]:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"
                        break
                direction += 1

        if "K" in grabbed_unit:
            for possible  in self.MOVES["Knight"]:
                possible_x = grabbed_pos[1] + possible[1]
                possible_y = grabbed_pos[0] + possible[0]
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue
                if "W" in self.grid[possible_y][possible_x] and "W" in grabbed_unit:
                    continue
                if "B" in self.grid[possible_y][possible_x] and "B" in grabbed_unit:
                    continue
                if "G" in self.grid[possible_y][possible_x]:
                    self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "X"


        if grabbed_unit == "BP":
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0] + self.BLACK_MOVES["Pawn"][0][0]
            kill_x1 = grabbed_pos[1] + 1
            kill_x2 = grabbed_pos[1] - 1

            if possible_y > 7:
                return

            if kill_x1 <= 7 and "W" in self.grid[possible_y][kill_x1] and "G" in self.grid[possible_y][kill_x1]:
                self.grid[possible_y][kill_x1] = self.grid[possible_y][kill_x1] + "X"
            if kill_x2 >= 0 and "W" in self.grid[possible_y][kill_x2] and "G" in self.grid[possible_y][kill_x2]:
                self.grid[possible_y][kill_x2] = self.grid[possible_y][kill_x2] + "X"
            
        if grabbed_unit == "WP":
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0] + self.WHITE_MOVES["Pawn"][0][0]
            kill_x1 = grabbed_pos[1] + 1
            kill_x2 = grabbed_pos[1] - 1

            if possible_y < 0:
                return

            if kill_x1 <= 7 and "B" in self.grid[possible_y][kill_x1] and "G" in self.grid[possible_y][kill_x1]:
                self.grid[possible_y][kill_x1] = self.grid[possible_y][kill_x1] + "X"
            if kill_x2 >= 0 and "B" in self.grid[possible_y][kill_x2] and "G" in self.grid[possible_y][kill_x2]:
                self.grid[possible_y][kill_x2] = self.grid[possible_y][kill_x2] + "X"
            
        return self.grid
    

    def check_check(self):
        for cell_y in range(self.GRID_SIZE):
            for cell_x in range(self.GRID_SIZE):
                self.handle_check(self.grid[cell_y][cell_x], (cell_y, cell_x))
        
        return self.grid
    

    #Find all the valid locations to move
    def find_pos(self, grabbed_unit, grabbed_pos):
        if "G" in grabbed_unit:
            for possible  in self.MOVES["King"]:
                possible_x = grabbed_pos[1] + possible[1]
                possible_y = grabbed_pos[0] + possible[0]
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue
                if "W" in self.grid[possible_y][possible_x] and "W" in grabbed_unit:
                    continue
                if "B" in self.grid[possible_y][possible_x] and "B" in grabbed_unit:
                    continue
                self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"

        if "Q" in grabbed_unit:
            direction = 1
            for i in range(self.MOVES["Queen"][0]):
                possible_x = grabbed_pos[1]
                possible_y = grabbed_pos[0]
                for possible in range(self.MOVES["Queen"][1]):
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

                    if self.grid[possible_y][possible_x] == "":
                        self.grid[possible_y][possible_x] = "O"
                    elif "W" in self.grid[possible_y][possible_x]:
                        if "B" in grabbed_unit:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"
                        break
                    elif "B" in self.grid[possible_y][possible_x]:
                        if "W" in grabbed_unit:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"
                        break
                direction += 1

        if "F" in grabbed_unit:
            direction = 1
            for i in range(self.MOVES["Bishop"][0]):
                possible_x = grabbed_pos[1]
                possible_y = grabbed_pos[0]
                for possible in range(self.MOVES["Bishop"][1]):
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

                    if self.grid[possible_y][possible_x] == "":
                        self.grid[possible_y][possible_x] = "O"
                    elif "W" in self.grid[possible_y][possible_x]:
                        if "B" in grabbed_unit:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"
                        break
                    elif "B" in self.grid[possible_y][possible_x]:
                        if "W" in grabbed_unit:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"
                        break
                direction += 1

        if "R" in grabbed_unit:
            direction = 1
            for i in range(self.MOVES["Rook"][0]):
                possible_x = grabbed_pos[1]
                possible_y = grabbed_pos[0]
                for possible in range(self.MOVES["Rook"][1]):
                    if direction == 1:
                        possible_y = self.clamp(possible_y + 1, 0, 7)
                    elif direction == 2:
                        possible_x = self.clamp(possible_x + 1, 0, 7)
                    elif direction == 3:
                        possible_y = self.clamp(possible_y - 1, 0, 7)
                    elif direction == 4:
                        possible_x = self.clamp(possible_x - 1, 0, 7)

                    if self.grid[possible_y][possible_x] == "":
                        self.grid[possible_y][possible_x] = "O"
                    elif "W" in self.grid[possible_y][possible_x]:
                        if "B" in grabbed_unit:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"
                        break
                    elif "B" in self.grid[possible_y][possible_x]:
                        if "W" in grabbed_unit:
                            self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"
                        break
                direction += 1

        if "K" in grabbed_unit:
            for possible  in self.MOVES["Knight"]:
                possible_x = grabbed_pos[1] + possible[1]
                possible_y = grabbed_pos[0] + possible[0]
                if possible_x > 7 or possible_y > 7 or possible_x < 0 or possible_y < 0:
                    continue
                if "W" in self.grid[possible_y][possible_x] and "W" in grabbed_unit:
                    continue
                if "B" in self.grid[possible_y][possible_x] and "B" in grabbed_unit:
                    continue
                self.grid[possible_y][possible_x] = self.grid[possible_y][possible_x] + "O"

        if grabbed_unit == "BP":
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0] + self.BLACK_MOVES["Pawn"][0][0]
            kill_x1 = grabbed_pos[1] + 1
            kill_x2 = grabbed_pos[1] - 1

            if possible_y > 7:
                return

            if self.grid[possible_y][possible_x] == "":
                self.grid[possible_y][possible_x] = "O"
                if self.grid[self.clamp(possible_y+1, 0, 7)][possible_x] == "" and grabbed_pos[0] == 1:
                    self.grid[self.clamp(possible_y+1, 0, 7)][possible_x] = "O"

            if kill_x1 <= 7 and "W" in self.grid[possible_y][kill_x1]:
                self.grid[possible_y][kill_x1] = self.grid[possible_y][kill_x1] + "O"
            if kill_x2 >= 0 and "W" in self.grid[possible_y][kill_x2]:
                self.grid[possible_y][kill_x2] = self.grid[possible_y][kill_x2] + "O"
            
        if grabbed_unit == "WP":
            possible_x = grabbed_pos[1]
            possible_y = grabbed_pos[0] + self.WHITE_MOVES["Pawn"][0][0]
            kill_x1 = grabbed_pos[1] + 1
            kill_x2 = grabbed_pos[1] - 1

            if possible_y < 0:
                return
    
            if self.grid[possible_y][possible_x] == "":
                self.grid[possible_y][possible_x] = "O"
                if self.grid[self.clamp(possible_y-1, 0, 7)][possible_x] == "" and grabbed_pos[0] == 6:
                    self.grid[self.clamp(possible_y-1, 0, 7)][possible_x] = "O"

            if kill_x1 <= 7 and "B" in self.grid[possible_y][kill_x1]:
                self.grid[possible_y][kill_x1] = self.grid[possible_y][kill_x1] + "O"
            if kill_x2 >= 0 and "B" in self.grid[possible_y][kill_x2]:
                self.grid[possible_y][kill_x2] = self.grid[possible_y][kill_x2] + "O"
            
        return self.grid

    #Because it doesn't like removing circles
    def remove_pos(self):
        for cell_y in range(self.GRID_SIZE):
            for cell_x in range(self.GRID_SIZE):
                point = self.grid[cell_y][cell_x].replace("O", "")
                self.grid[cell_y][cell_x] = point
                point = self.grid[cell_y][cell_x].replace("X", "")
                self.grid[cell_y][cell_x] = point
                self.check_check()
        
        return self.grid