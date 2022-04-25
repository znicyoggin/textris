from utilities import combine_unique
from logger import *
from lib.Config import *
from lib.TetrisPiece import *


"""

Game board

"""
    
class GameBoard(object):
    def __init__(self, rows, columns):
        self.logger = Logger(".\logs\GameBoard.log", "DEBUG")
        self.num_rows        =    rows
        self.num_columns    =    columns
    
        self.coordinates = {}
    
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                self.coordinates[(x,y)] = None
                
        self.calculate_start_location()
        
        #All pieces currently on the board
        self.piece_list = []
        
        #Tetris piece which is currently being controlled"
        self.current_piece_index = None
        
        #Flag for when multiple blocks will be falling (Instead of just the current piece)
        self.multi_fall = False
                
    #Calculate where pieces will drop frome    
    def calculate_start_location(self):
        start_x = int(self.num_columns/ 2) - 1
        start_y = self.num_rows- 1
        self.logger.debug("Starting location is ({}, {})".format(start_x, start_y))
        self.start_loc = (start_x, start_y)
    
    #Return the default location to begin dropping a new tetris piece
    def DropSpot(self):
        return self.start_loc
     
     #Place a tetris piece at a location
    def place_block(self, shape, anchor_position, frozen = False):
        newTetrisPiece = TetrisPiece(shape, anchor_position)
        coordinates  = newTetrisPiece.get_coordinates()
        if len(coordinates) != 4: self.logger.error("{} has {} coordinates.".format(shape, len(coordinates)))
        self.logger.debug("Placing a new {}\n\nNEW COORDINATES: {}".format(newTetrisPiece.get_shape(), coordinates))

        can_place = True
        for position in coordinates:
            curr_shape = self.at(position)
            if curr_shape == False:
                self.logger.error("Cannot place {} at {}.  Location is out of bounds.  Board is {} by {}.".format(shape, position, self.num_rows, self.num_columns))
                can_place = False
                break
            if curr_shape != None:
                can_place = False
                self.logger.error("Cannot place {} at {}.  Already populated by {}.".format(shape, position, curr_shape))
                break
        if can_place:
            for position in coordinates:
                self.coordinates[position] = shape
            self.piece_list.append(newTetrisPiece)
            self.current_piece_index = len(self.piece_list) - 1
            if not frozen: self.piece_list[self.current_piece_index].falling()
            return True
        else: return False
        
    def is_something_falling(self):
        for piece in self.piece_list:
            if piece.is_currently_falling(): return True
        return False
        
    def move_piece(self, move_type):
        if move_type == None: return False
        
        #left, right, fast fall, rotate, instant drop or swap
        if move_type not in move_types: 
            self.logger.error("{} is an invalid move type. Use one of these: {}".format(move_type, move_types))
            return False
        
        current_piece = self.piece_list[self.current_piece_index]
        
        new_coordinates = current_piece.move_piece(move_type)
        if not new_coordinates: 
            self.logger.debug("Unable to move piece.  current_piece.move_piece({}) returned {}.".format(move_type, new_coordinates))
            return False
        self.logger.debug("Moving {}-{} to the {}.".format(current_piece.shape(), self.current_piece_index, "left" if move_type == "T_LEFT" else "right"))
        i = 0
        #Validate the new coordinates
        for (x, y) in new_coordinates:
            i = i + 1
            self.logger.debug(" Checking {} coordinate: {}, {}".format(get_placement_str(i), x, y))
            
            if (x, y) in current_piece.get_coordinates(): continue
            if self.not_empty((x, y)): 
                self.logger.debug("Unable to move {}-{}. {} coordinate would have been occupied by {}".format(current_piece.shape(), self.current_piece_index, get_placement_str(i), self.at((x, y))))
                return False
            continue
        #Update the board
        for position in combine_unique(current_piece.get_coordinates(), new_coordinates):
            if position not in new_coordinates: self.set(position, None)
            else: self.set(position, current_piece.shape())

        
        #Update new coordinates on current piece
        self.piece_list[self.current_piece_index].set_coordinates(new_coordinates)
        
        #Update the pieces rotation counter
        if move_type in ["T_ROT_RIGHT", "T_ROT_LEFT"]: self.piece_list[self.current_piece_index].increment_rotation(move_type)
        
        
        return True
                    
    def apply_gravity(self):     
        #Verify only one piece is falling
        if len(self.piece_list) == 0:
            self.logger.debug("No tetris pieces on the board.  Nothing is going to fall")
            return
        if self.multi_fall:
            self.logger.debug("Multi falling is enabled but has not yet been implemented. Exiting...")
            return
        current_piece = self.piece_list[self.current_piece_index]
        
        new_coordinates = []

        if not current_piece.is_falling:#if len(self.falling_pieces) == 0: 
            self.logger.debug("Nothing is falling. multifall is {}".format("Enabled" if self.multi_fall else "Disabled"))
            return
        coordinates = current_piece.get_coordinates()
        self.logger.debug("Applying gravity to {}-{}.\nCUR COORDINATES: {}".format(current_piece.shape(), self.current_piece_index, coordinates))
        if len(coordinates) != 4: self.logger.error("{} has {} coordinates: {}".format(current_piece.shape(), len(coordinates), coordinates))
        #Loop through the coordinates of each segment of the tetris piece
        for (x,y) in coordinates:
            if x <= 0 or x >= self.num_columns or y <= 0 or y >= self.num_rows: 
                self.logger.error("Cannot apply gravity to {} at {}.  It is out of bounds".format(current_piece.shape(), (x, y)))
                return
            temp_loc = (x, y-1)
            if self.not_empty(temp_loc) and temp_loc not in coordinates:
                self.logger.debug("{} has stopped falling since it has reached {} which is populated by {}".format(shape, temp_loc, self.at(temp_loc)))
                return 
            new_coordinates.append(temp_loc)
        if len(new_coordinates) != 4: self.logger.debug("{} shape has an invalid number of new coordinates: {}".format(shape, new_coordinates))
        #loop through all unique positions and apply the movement to the board
        for position in combine_unique(coordinates, new_coordinates):
            if position not in new_coordinates: self.set(position, None) 
            else: 
                #This location is now occurpied
                self.set(position, current_piece.get_shape())
                x, y = position
                if y == 0: current_piece.grounded()
        #Commit new locations to the current piece
        self.logger.debug("Setting coordinates for {}-{}:\nNEW COORDINATES: {}\n".format(current_piece.shape(), self.current_piece_index, coordinates, new_coordinates))
        current_piece.set_coordinates(new_coordinates)            
    #Is a location populated with a block?
    def not_empty(self, coordinates):
        return True if self.coordinates[coordinates] is not None else False
    
    #Is a location populated with a block?
    def empty(self, coordinates):
        return False if self.coordinates[coordinates] is not None else True

    #Set a single block
    def set(self, coordinates, shape):
        if shape is not None and shape not in block_types: 
            self.logger.error("Not a valid shape")
            return False
            
        self.coordinates[coordinates] = shape
        return True
    
    #What type of block is here?
    def at(self, coordinates):
        (x, y) = coordinates
        if x < 0 or x >= self.num_columns or y < 0 or y >= self.num_rows:
            self.logger.error("Invalid coordinates provided to GamerBoard.at() function. x={}, y={}".format(x, y))
            return False
            
        return self.coordinates[coordinates]
     
    #Display a textual version of the game board
    def display_board(self, rows_to_display = 0, coordinates_only = False):
        print("##########")
        for y in range(rows_to_display-1, -1, -1):
            print("\r")
            line = ""
            for x in range(self.num_columns): 
                if coordinates_only: line += "({},{})".format(x, y)
                elif self.not_empty((x,y)): line += "X"
                else: line += "_"
            print(line)
        print("##########")
     
    def get_board(self):
        return self.coordinates
        
if __name__ == "__main__":
    #logger = Logger("./log/GameBoard __main__.log")
    #Perform tests and learn the syntax
    config = Config("CLASSIC_TETRIS")
    
    num_rows = config.num_rows 
    num_cols = config.num_columns
    num_rows_display = config.num_rows_display
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
    
    #Place a block at the starting location
    start_loc = test_game_board.DropSpot()
    test_game_board.place_block("SQUARE", start_loc)
    
    """
    #Display the coordinates [hide columns count, coordinates only]
    test_game_board.display_board(0, True)
    """
    
    """
    Testing Gravity
    """
    test_game_board.display_board(num_rows_display)

    #self.logger.debug("After falling:")
    for i in range(40):
        if i + num_rows_display >= num_rows: test_game_board.display_board(num_rows_display)
        if i == 37: test_game_board.move_piece("T_LEFT")
        test_game_board.apply_gravity()            