from TetrisBlock import *
from logger import *
from Config import *
from utilities import combine_unique

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
        
        #All pieces currently on the board
        self.piece_list = []
        
        #Tetris piece which is currently being controlled"
        self.current_piece_index = None
        
        #Flag for when multiple blocks will be falling (Instead of just the current piece)
        self.multi_fall = False
                
    #Place a tetris piece    
    def calculate_start_location(self):
        start_x = int(self.num_rows/ 2) - 1
        start_y = self.num_columns - 1
        print(start_y)
        self.start_loc = (start_x, start_y)
    
    #Return the default location to begin dropping a new tetris piece
    def DropSpot(self):
        return self.start_loc
     
     #Place a tetris piece at a location
    def place_block(self, shape, anchor_position, frozen = False):
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
            self.piece_list.append(newTetrisPiece)
            self.current_piece_index = len(self.piece_list) - 1
            if not frozen: self.piece_list[self.current_piece_index].falling()
            return True
        else: return False
     
    def apply_gravity(self):
        #Verify only one piece is falling
        if len(self.piece_list) == 0:
            log_error("No tetris pieces on the board.  Nothing is going to fall", "DEBUG")
            return
        if self.multi_fall:
            log_error("Multi falling is enabled")
            return
        new_block_locations = []
        current_piece = self.piece_list[self.current_piece_index]
        if not current_piece.is_falling: 
            log_error("Nothing is falling.", "DEBUG")
            return
        shape = current_piece.shape()
        curr_block_locations = current_piece.get_coordinates()
        done_falling = False
        for (x,y) in curr_block_locations:
            if x <= 0 or x > self.num_rows or y <= 0 or y > self.num_columns: 
                log_error("Cannot apply gravity to {} at {}.  It is out of bounds".format(shape, (x, y)))
                return
            temp_loc = (x, y-1)
            if self.not_empty(temp_loc) and temp_loc not in curr_block_locations:
                log_error("{} has stopped falling since it has reached {} which is populated by {}".format(shape, temp_loc, self.at(temp_loc)), "DEBUG")
                return
            if y-1 == 0: done_falling = True
            new_block_locations.append(temp_loc)
        if done_falling:
            log_error("Piece is done falling", "DEBUG")
            current_piece.grounded()
            return
        #loop through all unique positions and apply the movement to the board
        for position in combine_unique(curr_block_locations, new_block_locations):
            print(position )
            if position not in new_block_locations: self.set(position, None) 
            else: self.set(position, shape)
        #Commit new locations to the current piece
        log_error("{} has successfully fallen.  Replacing old coordinates".format(shape))
        current_piece.set_coordinates(new_block_locations)
        
    def valid_coordinate(self, coordinate):
        is_valid = True
        (x, y) = coordinate
        #out of bounds
        if self.is_coordinate_out_of_bounds(coordinate): is_valid = False
        
        #detect collision
        elif self.not_empty(coordinate): is_valid = False
        return is_valid
        
    def is_coordinate_out_of_bounds(self, coordinate):
        (x,y) = coordinate
        return False if x <= 0 or x > self.num_rows or y <= 0 or y > self.num_columns else True
        
    #Is a location populated with a block?
    def not_empty(self, coordinate):
        return True if self.coordinates[coordinate] is not None else False
    
    #Is a location populated with a block?
    def empty(self, coordinate):
        return False if self.coordinates[coordinate] is not None else True

    #Set a single block
    def set(self, coordinate, shape):
        if shape is not None and shape not in block_types: 
            log_error("Not a valid shape")
            return False
            
        self.coordinates[coordinate] = shape
        return True
        
   #Move current piece left or right - arbitrarily right by default
    def move_lateral(move_right = True):
        if not isInstance(move_right, types.BooleanType):
            log_error("Parameter 'move_right' should be a boolean. move_right = {}".format(move_right))
        current_piece = self.piece_list[self.current_piece_index]
        x_adjust = 0
        if move_right: x_adjust = 1
        else: x_adjust = -1
        
        new_coordinates = current_piece.transform_coordinates(0,x_adjust)
        #validate
        return False#Only return true if the move is committed
    
    #What type of block is here?
    def at(self, coordinates):
        (x, y) = coordinates
        if x < 0 or x >= self.num_rows or y < 0 or y >= self.num_columns:
            log_error("invalid coordinates")
            return False
            
        return self.coordinates[coordinates]
    
    def rotate_piece(self, index = None):
        if index is None: index = self.current_piece_index
        
        return index
        
    #Display a textual version of the game board
    def display_board(self, hide_column_count = 0, coordinates_only = False):
        for y in range(self.num_columns-1-hide_column_count, 0, -1):
            print("\r")
            line = ""
            for x in range(self.num_rows): 
                if coordinates_only: line += "({},{})".format(x, y)
                elif self.not_empty((x,y)): line += "X"
                else: line += "_"
            print(line)
        
if __name__ == "__main__":
    #Perform tests and learn the syntax
    config = Config("CLASSIC_TETRIS")
    
    num_rows = config.num_rows 
    num_cols = config.num_columns
    display_cols = config.hide_column_count
    test_game_board = GameBoard(num_rows, num_cols)
    
    
    """
    #Place part of a line at 4, 2
    test_coordinates = (4, 2)
    test_game_board.set(test_coordinates, "LINE")
    """
    """
    #Place multiple pieces without colision
    #test_game_board.place_block("Z-PIECE", (7,0))
    #test_game_board.place_block("LINE", (3,4))
    """
    """
    #Place a block at the starting location
    start_loc = test_game_board.DropSpot()
    test_game_board.place_block("Z-PIECE", start_loc)
    """
    """
    #Display the coordinates [hide columns count, coordinates only]
    test_game_board.display_board(0, True)
    """
    
    #Testing Gravity
    test_game_board.display_board(display_cols)
    start_loc = test_game_board.DropSpot()
    print("After falling:")
    for j in range(40):
        test_game_board.place_block("Z-PIECE", start_loc)
        
        for i in range(40):
            if i + display_cols >= num_cols: test_game_board.display_board(display_cols)
            test_game_board.apply_gravity()
            dir = input("Press Enter to continue. Try moving a piece with l or r")
            #right = True
            #left = False
            #if dir == "l": test_game_board.move_lateral(right)
            #elif dir == "r": test_game_board.move_lateral(left)
 

    