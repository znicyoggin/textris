from lib.logger import *
from lib.utilities import *

"""
Tetris Pieces

"""
class TetrisPiece(object):
    
    def __init__(self, block_type = None, anchor_position = None, rotation = 0):
        self.ID = ""
        self.block_type= block_type
        self.anchor_position= anchor_position
        self.rotation= rotation
        
        #Validate Block type
        
        if self.ValidateBlockType() == False: return
        
        if self.anchor_position is None:
            log_error("Anchor Position not provided")
            return
        if not type(anchor_position) is tuple:
            log_error("Anchor position {} is not valid.".format(self.anchor_position))
            return
        self.coordinates = []
        
        self.is_falling = False
        
        #Determine coordinates for all blocks in the shape
        log_error("Displaying initial coordinates for {}".format(self.block_type), "DEBUG")
        for i in range(4):
            rotation_modifier = relative_position(self.block_type, i, self.rotation)
            if rotation_modifier == False:
                log_error("Unable to rotate {} {} {}".format(self.block_type, self.rotation, "time" if rotation == 1 else "times"))
                return
            self.coordinates.append(tuple(map(lambda i, j: i + j, self.anchor_position, rotation_modifier)))
            log_error("{}: {}".format(i, self.coordinates[i]), "DEBUG")
    
    def set_ID(self, ID):
        self.ID = ID
        return self.ID
    
    def get_ID(self):
        return self.ID
        
    def is_falling(self):
        if self.is_falling:
            return True
        else: return False

    def falling(self):
        self.is_falling = True

    def grounded(self):
        self.is_falling = False

    #Current coordinates for each part of this piece
    def get_coordinates(self):
        if len(self.coordinates) > 4: log_error("Error: Too many coordinates")
        return self.coordinates
    
    #Transformations only return coordinates, commit of new coordinates is implementation specific
    def transform_coordinates(self, rotate=0, adjust_x=0):
        log_error("transform_coordinates called with rotate={}, adjust_x={}\n".format(rotate, adjust_x),"DEBUG")
        #Validate parameters
        if rotate not in (-1, 0, 1):            
            log_error("Invalid Rotation Passed: {}".format(rotate))
            return False
        
        if adjust_x not in (-1, 0, 1):
            log_error("Invalid X Adjustment Passed: {}".format(adjust_x))
            return False
        new_rotation = self.rotation
        if abs(rotate) != 0: 
            new_rotation = (self.rotation + rotate) % (num_rotations[self.block_type] + 1)
        """
        if new_rotation == 0 and adjust_x == 0:
            log_error("No change to coordinates.")
            return False
        """    
        new_coordinates = []
        #log_error("New Coordinates:", "DEBUG")
        for i in range(4): 
            rotation_modifier = relative_position(self.block_type, i, new_rotation)
            if rotation_modifier == False:
                log_error("Unable to rotate {} from position {} to position {} (Failed on i = {})".format(self.block_type, self.rotation, new_rotation, i))
                return False
            
            adjustment = add_coordinates(rotation_modifier, (adjust_x, 0))
       
            new_coordinates.append(add_coordinates(self.anchor_position, adjustment))
            #log_error(new_coordinates[i], "DEBUG")
            
           
        return new_coordinates
        
    def about_piece(self):
        print("--------------------------------------------------")
        print("The {} is on rotation #{} of {}".format(self.block_type, self.rotation, num_rotations[self.block_type]))
        print("It is anchored at {}".format(self.anchor_position))
        print("Coordinates:{}".format(self.coordinates))
        print("Piece is{} falling".format(" not" if not self.is_falling else ""))
        print("Identifier is {}".format(self.ID))
        print("--------------------------------------------------")
        
    #Set new coordinates for each part of the piece
    def set_coordinates(self, new_coordinates):
        if len(new_coordinates) > 4: log_error("Error: too many blocks")
        self.coordinates = new_coordinates
        return
    
    #What type of shape is this?
    def get_shape(self):
        return self.block_type
        
    def shape(self):
        return self.block_type
    
    def get_anchor(self):
        return self.anchor_position
    
    def set_anchor(self, position):
        self.anchor_position = position
        return
    
    def descend(self):
        (x, y) =  self.anchor_position
        self.anchor_position = (x, y-1)
        return
        
    def lateral(self, x_adjust):
        (x, y) = self.anchor_position
        self.anchor_position = (x + x_adjust, y)
        return
    
    def make_rotation(self, modifier):
        new_rotation = (self.rotation + modifier) % (num_rotations[self.block_type]+1)
        log_error("Moving {} from rotation #{} to rotation #{}".format(self.block_type, self.rotation, new_rotation), "DEBUG")
        log_error("new_rotation = {} = ({} + {}) % {}".format( new_rotation, self.rotation, modifier, num_rotations[self.block_type]), "DEBUG")
        self.rotation = new_rotation
        return self.rotation
        
     #Is this a valid type of block?
    def ValidateBlockType(self):
            valid_block_type = True
            if self.block_type is None:
                log_error("No block type provided")
                return not valid_block_type
            if not type(self.block_type) is str:
                log_error("block type is not a string")
                return not valid_block_type
            if self.block_type not in block_types:
                log_error("{} is not a block type".format(self.block_type))
                return not valid_block_type
            return valid_block_type
        
        
if __name__ == "__main__":
    """
    #Run basic tests of functionality
    test_square     = TetrisPiece("SQUARE", (0,0), 0)
    test_zpiece        = TetrisPiece("Z-PIECE", (11,32), 0)
    test_circle        = TetrisPiece("CIRCLE", (0,0), 0)
    test_nowhere    = TetrisPiece("SQUARE")
    test_bad_loc    = TetrisPiece("SQUARE", 22)
    test_rotate_1     = TetrisPiece("LINE", (0,0), 1)    
    test_rotate_2     = TetrisPiece("S-PIECE", (22,11), 3)
    """
    
    """
    #Test Transformations
    """
    #Initialize a square
    test_square = TetrisPiece("J-PIECE", (5,5))
    #Rotate clockwise
    test_square.transform_coordinates(1, -1)
    

    #Rotate counter-clockwise
    #test_square.transform_coordinates(-1, 0)