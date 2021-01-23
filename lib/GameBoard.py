from lib.TetrisBlock import *
from lib.logger import *
from lib.Config import *
from lib.utilities import combine_unique

"""
Game board
"""
    
class GameBoard(object):
    def __init__(self, rows, columns):
        self.num_rows        =    rows
        self.num_columns    =    columns
        self.index = 0
        self.coordinates = {}
        
        self.line_count = 0
        self.score = 0
    
        for x in range(self.num_rows):
            for y in range(self.num_columns):
                self.coordinates[(x,y)] = None
                
        self.calculate_start_location()
        
        #All pieces currently on the board
        self.piece_list = []
        
        #Tetris piece which is currently being controlled"
        self.current_piece_index = 0
        
        #Flag for when multiple blocks will be falling (Instead of just the current piece)
        self.multi_fall = False
                
    #Place a tetris piece    
    def calculate_start_location(self):
        start_x = int(self.num_rows/ 2) - 1
        start_y = self.num_columns - 1
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
            
            newTetrisPiece.set_ID(self.index)
            self.index += 1
            
            self.piece_list.append(newTetrisPiece)
            self.current_piece_index = len(self.piece_list) - 1
            if not frozen: self.piece_list[self.current_piece_index].falling()
            return True
        else: return False
     
    def falling(self):
        curr = self.curr_piece()
        if curr == False: return False
        return self.curr_piece().is_falling
        
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
            if x < 0 or x >= self.num_rows or y < 0 or y >= self.num_columns: 
                log_error("Cannot apply gravity to {} at {}.  It is out of bounds".format(shape, (x, y)))
                return
            temp_loc = (x, y-1)
            if self.not_empty(temp_loc) and temp_loc not in curr_block_locations:
                log_error("{} has stopped falling since it has reached {} which is populated by {}".format(shape, temp_loc, self.at(temp_loc)), "DEBUG")
                done_falling = True
            if y-1 == 0: done_falling = True
            new_block_locations.append(temp_loc)
        if done_falling:
            log_error("Piece is done falling", "DEBUG")
            current_piece.grounded()
            return
        #loop through all unique positions and apply the movement to the board
        for position in combine_unique(curr_block_locations, new_block_locations):
            if position not in new_block_locations: self.set(position, None) 
            else: self.set(position, shape)
        #Commit new locations to the current piece
        current_piece.set_coordinates(new_block_locations)
        current_piece.descend()
        log_error("Gravity Applied to {}:".format(shape), "DEBUG")
        if logger_level == "DEBUG": self.about_current_piece()
        
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
        return True if x < 0 or x >= self.num_rows or y < 0 or y >= self.num_columns else False

        
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
        
    def curr_piece(self):
        if len(self.piece_list) <= 0: 
            log_error("No pieces yet","DEBUG")
            return False            
        return self.piece_list[self.current_piece_index]

    """
    Find a way to combine these two functions
    
    move_lateral
    rotate
    """
   #Move current piece left or right - arbitrarily right by default
    def move_lateral(self, move_right = True):
        if not type(move_right) is bool:
            log_error("Parameter 'move_right' should be a boolean. move_right = {}".format(move_right))
        move_str = "right" if move_right else "left"
        current_piece = self.curr_piece()
        x_adjust = 1 if move_right else -1
        log_error("Move right = {}, x adjust = {}, ".format(move_right, x_adjust), "DEBUG")
        shape = current_piece.shape()
        current_coordinates = current_piece.get_coordinates()
        new_coordinates = current_piece.transform_coordinates(0,x_adjust)


        diff_coordinates = []
        empty_coordinates = []

        for position in combine_unique(current_coordinates, new_coordinates):
            if position not in current_coordinates:
                if self.is_coordinate_out_of_bounds(position):
                    log_error("Cannot move {} {}. {} is out of bounds.".format(shape, move_str , position), "DEBUG")
                    return False
                elif self.not_empty(position):
                    log_error("Cannot move {} {}. {} is occupied by {}.".format(shape, move_str, position, self.at(position)), "DEBUG")
                    return False
                else: diff_coordinates.append(position)
            elif position not in new_coordinates: empty_coordinates.append(position)
            else: pass

        for position in empty_coordinates: self.set(position, None)#if self.set(position, None): print("Success.  Position {} is {}".format(position, "empty" if self.empty(position) else "not empty"))     
        for position in diff_coordinates: self.set(position, shape)

        current_piece.set_coordinates(new_coordinates)
        current_piece.lateral(x_adjust)
        log_error("Moving {} {}:\n".format(shape, "right" if move_right else "left"), "DEBUG")
        if logger_level == "DEBUG": self.about_current_piece()
        return True#Only return true if the move is committed
    
    def rotate(self, clockwise = True):
        if not type(clockwise) is bool:
            log_error("Parameter 'clockwise' should be a boolean. clockwise= {}".format(clockwise))
        move_type_str = "clockwise" if clockwise else "counter-clockwise"

        current_piece = self.curr_piece()
        shape = current_piece.shape()
        log_error("Moving {} {}".format(shape, move_type_str), "DEBUG")

        current_coordinates = current_piece.get_coordinates()
        new_coordinates = current_piece.transform_coordinates(1 if clockwise else -1,0)
        diff_coordinates = []
        empty_coordinates = []

        for position in combine_unique(current_coordinates, new_coordinates):
            if position not in current_coordinates:
                if self.is_coordinate_out_of_bounds(position):
                    log_error("Cannot move {} {}. {} is out of bounds.".format(shape, move_type_str, position), "DEBUG")
                    return False
                elif self.not_empty(position):
                    log_error("Cannot move {} {}. {} is occupied by {}.".format(shape, move_type_str, self.at(position)), "DEBUG")
                    return False
                else: diff_coordinates.append(position)
            elif position not in new_coordinates: empty_coordinates.append(position)
            else: pass

        for position in empty_coordinates: self.set(position, None)#if self.set(position, None): print("Success.  Position {} is {}".format(position, "empty" if self.empty(position) else "not empty"))     
        for position in diff_coordinates: self.set(position, shape)

        current_piece.make_rotation(1 if clockwise else -1)
        current_piece.set_coordinates(new_coordinates)
        log_error("Rotated {} {}:".format(shape, move_type_str ))
        if logger_level == "DEBUG": self.about_current_piece()
        return True#Only return true if the move is committed
        
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
    
    #Modify score based on the number of lines cleared
    def update_stats(self, num_lines):
        if num_lines not in range(1, 4):
            log_error("ERROR: Invalid number of lines have been removed.")
            return
        self.line_count += num_lines
        print("Adding {} lines for {} points".format(num_lines, score_calc[num_lines-1]))
        self.score += score_calc[num_lines-1]
        
    def about_current_piece(self):
        print("--------------------------------------------------")
        print("   ~~~ Piece number {} ~~~   ".format(self.current_piece_index))
        self.curr_piece().about_piece()
        
    #Display a textual version of the game board
    def display_board(self, hide_column_count = 0, coordinates_only = False):
        print("Lines: {0:>3} Score: {1:>6}".format(self.line_count, self.score))
        for y in range(self.num_columns-1-hide_column_count, 0, -1):
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
            if i + display_cols >= num_cols: 
                test_game_board.display_board(display_cols)
                """
                #Test moving left or right
                dir = input("Press Enter to continue. Try moving a piece with l or r"
                right = True
                left = False
                if dir == "l": test_game_board.move_lateral(left)
                elif dir == "r": test_game_board.move_lateral(right)
                """
                """
                #Test rotation
                """
                dir = input("Press Enter to continue. Try rotating a piece with l or r")
                clockwise = True
                counterclockwise = False
                if dir == "l": test_game_board.rotate(counterclockwise)
                elif dir == "r": test_game_board.rotate(clockwise)
                print("\r\n\r\n")
            test_game_board.apply_gravity()


    