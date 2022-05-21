from utilities import combine_unique
from logger import *
from lib.Config import *
from lib.TetrisPiece import *


"""

Game board

"""
    
class GameBoard(object):
    def __init__(self, rows, columns, max_rows):
        self.logger = Logger(".\logs\GameBoard.log", "DEBUG")
        self.num_rows = rows
        self.num_columns = columns
        self.max_rows = max_rows
            
        self.coordinates = {}
    
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                self.coordinates[(x,y)] = None
                
        self.calculate_start_location()
        
        #All pieces currently on the board
        self.piece_list = []
        self.completed_lines = []
        
        #Tetris piece which is currently being controlled"
        self.current_piece_index = None
        
        #Flag for when multiple blocks will be falling (Instead of just the current piece)
        self.multi_fall = False

        self.game_over = False
        
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
        self.logger.debug("Moving {}-{}.  Move type is {}.  On {} rotation.".format(current_piece.shape(), self.current_piece_index, move_type, current_piece.rotation))
        i = 0
        need_to_ground_piece = False
        #Validate the new coordinates
        for coordinate in new_coordinates:
            i = i + 1
            self.logger.debug(" Checking {} coordinate: {}".format(get_placement_str(i), coordinate))
            
            if coordinate in current_piece.get_coordinates(): continue
            if self.out_of_bounds(coordinate):
                self.logger.debug("Unable to move {}-{}. {} coordinate would have been out of bounds".format(current_piece.shape(), self.current_piece_index, get_placement_str(i)))
                return False
            if self.not_empty(coordinate): 
                self.logger.debug("Unable to move {}-{}. {} coordinate would have been occupied by {}".format(current_piece.shape(), self.current_piece_index, get_placement_str(i), self.at((coordinate))))
                return False
            if coordinate[1] == 0: need_to_ground_piece = True
            continue
        #Update the board
        for position in combine_unique(current_piece.get_coordinates(), new_coordinates):
            if position not in new_coordinates: self.set(position, None)
            else: self.set(position, current_piece.shape())

        
        #Update new coordinates on current piece
        current_piece.set_coordinates(new_coordinates)
        if need_to_ground_piece: current_piece.grounded()
        
        #Update the pieces rotation counter
        if move_type in ["T_ROT_RIGHT", "T_ROT_LEFT"]: 
            current_piece.increment_rotation(move_type)
                
        current_piece.update_anchor_position(move_type)
        
        return True
        
    def out_of_bounds(self, coordinate):
        x, y = coordinate
        if x >= self.num_columns or x < 0 or y >= self.num_rows or y < 0: return True
        if x >= self.num_columns or x < 0 or y >= self.num_rows or y < 0: return True
        else: return False
     
    def check_for_lines(self):
        num_lines_consecutive = 0
        completed_lines = []
        last_row_line = None

        for y in range(self.num_rows):
            is_complete = True
            for x in range(self.num_columns):
                if self.empty((x, y)) : is_complete = False
            if is_complete:
                if last_row_line == x-1: num_lines_consecutive += 1
                last_row_line = x
        if last_row_line is None: return 0
        
        self.completed_lines = completed_lines
        print("Checking for completed lines. {}, {}".format(self.completed_lines, num_lines_consecutive))
        return num_lines_consecutive
    
    def get_completed_lines(self):
        return self.completed_lines
        
    def cleanup_lines(self):
        for x in self.completed_lines:
            for y in self.num_cols:
                self.set((x,y), None)
     
    def is_game_over(self):
        return self.game_over
        
    def game_is_over(self):
        self.game_over = True
        return
    
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
            if self.out_of_bounds((x,y)): 
                self.logger.error("Cannot apply gravity to {} at {}.  It is out of bounds".format(current_piece.shape(), (x, y)))
                return
            temp_loc = (x, y-1)
            if temp_loc[1] < 0: return
            if self.not_empty(temp_loc) and temp_loc not in coordinates:
                self.logger.debug("{}-{} has stopped falling since it has reached {} which is populated by {}".format(current_piece.shape(), self.current_piece_index, temp_loc, self.at(temp_loc)))
                current_piece.grounded()
                if y >= self.max_rows: self.game_is_over() 
                return 
            new_coordinates.append(temp_loc)
        if len(new_coordinates) != 4: self.logger.debug("{} shape has an invalid number of new coordinates: {}".format(shape, new_coordinates))
        #loop through all unique positions and apply the movement to the board
        for position in combine_unique(coordinates, new_coordinates):
            if position not in new_coordinates: self.set(position, None) 
            else: 
                #This location is now occupied
                self.set(position, current_piece.get_shape())
                x, y = position
                if y == 0: current_piece.grounded()#Is this where we add the logic to check for "On top of a piece?"
        #Commit new locations to the current piece
        self.logger.debug("Setting coordinates for {}-{}:\nNEW COORDINATES: {}\n".format(current_piece.shape(), self.current_piece_index, coordinates, new_coordinates))
        current_piece.set_coordinates(new_coordinates)

        #Shortcut to move the anchor down by one space
        current_piece.update_anchor_position("T_FAST")
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