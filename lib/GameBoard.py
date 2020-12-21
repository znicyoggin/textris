from TetrisBlock import *
from logger import *
from Config import *

"""

Game board

"""
    
class GameBoard(object):
    def __init__(self, rows, columns):
        self.num_rows        =    rows
        self.num_columns    =    columns
    
        self.coordinates = {}
    
        for x in range(self.num_rows):
            for y in range(self.num_columns):
                self.coordinates[(x,y)] = None
                
        self.calculate_start_location()
        
        self.piece_list = []
                
    #Place a tetris piece    
    def calculate_start_location(self):
        start_x = 0
        start_y = int((self.num_columns / 2))
        print(start_y)
        self.start_loc = (start_x, start_y)
    
    def start(self):
        return self.start_loc
        
    def place_block(self, shape, anchor_position):
        newTetrisPiece = TetrisPiece(shape, anchor_position)
        coordinates  = newTetrisPiece.get_coordinates()
        
        can_place = True
        for position in coordinates:
            curr_shape = self.at(position)
            if curr_shape == False:
                log_error("Cannot place {} at {}.  Location is out of bounds.  Board is {} by {}.".format(shape, position, self.num_rows, self.num_columns))
                can_place = False
                break
            if curr_shape != None:
                can_place = False
                log_error("Cannot place {} at {}.  Already populated by {}.".format(shape, position, curr_shape))
                break
        if can_place:
            for position in coordinates:
                self.coordinates[position] = shape
            self.piece_list.append(newTetrisPiece())
            return True
        else: return False
    
    #Is a location populated with a block?
    def not_empty(self, coordinates):
        return True if self.coordinates[coordinates] is not None else False
    
    #Is a location populated with a block?
        def empty(self, coordinates):
            return False if self.coordinates[coordinates] is not None else True
            
    #Set a single block
    def set(self, coordinates, shape):
        if shape not in block_types: 
            log_error("Not a valid shape")
            return False
            
        self.coordinates[coordinates] = shape
        return True
    
    #What type of block is here?
    def at(self, coordinates):
        (x, y) = coordinates
        if x < 0 or x >= self.num_rows or y < 0 or y >= self.num_columns:
            log_error("invalid coordinates")
            return False
            
        return self.coordinates[coordinates]
        
    def display_board(self):
        for x in range(self.num_rows):
            print("\r")
            line = ""
            for y in range(self.num_columns): 
                if self.not_empty((x,y)): line += "X"
                else: line += "_"
            print(line)
        
if __name__ == "__main__":
    config = Config("CLASSIC_TETRIS")
    
    num_rows = config.num_rows 
    num_cols = config.num_columns
    test_game_board = GameBoard(num_rows, num_cols)
    
    #Place part of a line at 4, 2
    test_coordinates = (4, 2)
    test_game_board.set(test_coordinates, "LINE")
    
    
    #Place multiple pieces without colision
    test_game_board.place_block("Z-PIECE", (7,0))
    test_game_board.place_block("LINE", (9,2))
    
    #Place a block at the starting location
    start_loc = test_game_board.start()
    test_game_board.place_block("Z-PIECE", start_loc)
    
    test_game_board.display_board()
    
    """Make pieces fall
           is_falling - should the board know, or should the individual pieces know? - make a toggle so that the board determines and the pieces keep track
         def fall(self):
        new_coordinates = []
        can_fall = True
        for i in range(4):
            x, y = self.coordinates[i]
            new_coordinates[i] = (x, y+1)
            if self.empty(
    """
    
                
    