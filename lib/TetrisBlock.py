from logger import *
from utilities import add_coordinates

#Predefine the shapes here
#Add ability to assign a tetris block as a part of a shape

block_types = [
"SQUARE",
"Z-PIECE",
"S-PIECE",
"L-PIECE",
"J-PIECE",
"T-PIECE",
"LINE"
]

num_rotations = {
"SQUARE" : 0,
"Z-PIECE": 1,
"S-PIECE": 1,
"L-PIECE": 3,
"J-PIECE": 3,
"T-PIECE": 3,
"LINE": 1
}

def relative_position(shape, block_num, rotation):
    #lookup relative position for any block of any shape
    lookup_relative_position = {            # (x, y)
        #SQUARE
        #Base position : 0
        ("SQUARE", 0, 0)            :    (0,0),        #    [01-]
        ("SQUARE", 1, 0)            :    (1,0),        #    [23-]
        ("SQUARE", 2, 0)            :    (0,-1),        #    
        ("SQUARE", 3, 0)            :    (1,-1),        #    
        
        #Z-PIECE
        #Base position : 0
        ("Z-PIECE", 0, 0)            :    (0,0),        #    [01-]
        ("Z-PIECE", 1, 0)            :    (1,0),        #    [-23]
        ("Z-PIECE", 2, 0)            :    (1,-1),        #    
        ("Z-PIECE", 3, 0)            :    (2,-1),        #    
        
        #First Rotation : 1
        ("Z-PIECE", 0, 1)            :    (1,0),        #    [-0]
        ("Z-PIECE", 1, 1)            :    (0,-1),       #    [12]
        ("Z-PIECE", 2, 1)            :    (1,-1),       #    [3-]
        ("Z-PIECE", 3, 1)            :    (0,-2),       #    
        
        #S-PIECE
        #Base position : 0
        ("S-PIECE", 0, 0)            :    (1,0),        #    [-01]
        ("S-PIECE", 1, 0)            :    (2,0),        #    [23-]
        ("S-PIECE", 2, 0)            :    (0,-1),        #    
        ("S-PIECE", 3, 0)            :    (1,-1),        #    

        #Base position : 1
        ("S-PIECE", 0, 1)            :    (0,0),        #    [0-]
        ("S-PIECE", 1, 1)            :    (0,-1),        #    [12]
        ("S-PIECE", 2, 1)            :    (1,-1),       #    [-3]
        ("S-PIECE", 3, 1)            :    (1,-2),       #    
        
        #J-PIECE        
        #Base position : 0
        ("J-PIECE", 0, 0)    :    (1,0),    #    [-0]
        ("J-PIECE", 1, 0)    :    (1,-1),    #    [-1]
        ("J-PIECE", 2, 0)    :    (0,-2),    #    [23]
        ("J-PIECE", 3, 0)    :    (1,-2),    #
        
        #First rotation
        ("J-PIECE", 0, 1)    :    (0,0),    #    [0--]
        ("J-PIECE", 1, 1)    :    (0,-1),   #    [123]
        ("J-PIECE", 2, 1)    :    (1,-1),   #
        ("J-PIECE", 3, 1)    :    (2,-1),   #
            
        #Second rotation
        ("J-PIECE", 0, 2)    :    (0,0),    #    [01]
        ("J-PIECE", 1, 2)    :    (1,0),   #    [2-]
        ("J-PIECE", 2, 2)    :    (0,-1),   #    [3-]
        ("J-PIECE", 3, 2)    :    (0,-2),   #
        
        #Third rotation
        ("J-PIECE", 0, 3)    :    (0,0),    #    [012]
        ("J-PIECE", 1, 3)    :    (1,0),   #    [--3]
        ("J-PIECE", 2, 3)    :    (2,0),   #
        ("J-PIECE", 3, 3)    :    (2,-1),   #
        
        #L-PIECE  
        #Base position
        ("L-PIECE", 0, 1)    :    (0,0),        #    [0-]
        ("L-PIECE", 1, 1)    :    (0,-1),       #    [1-]
        ("L-PIECE", 2, 1)    :    (0,-2),       #    [23]
        ("L-PIECE", 3, 1)    :    (1,-2),       #    
        
        #First Rotation : 1
        ("L-PIECE", 0, 1)    :    (0,0),        #    [012]
        ("L-PIECE", 1, 1)    :    (1,0),        #    [3]
        ("L-PIECE", 2, 1)    :    (2,0),        #    
        ("L-PIECE", 3, 1)    :    (0,-1),       #    
        
        #Second Rotation: 2
        ("L-PIECE", 0, 2)    :    (0,0),        #    [01]
        ("L-PIECE", 1, 2)    :    (1,0),        #    [-2]
        ("L-PIECE", 2, 2)    :    (1,-1),       #    [-3]
        ("L-PIECE", 3, 2)    :    (1,-2),       #    
        
        #Third Rotation: 3
        ("L-PIECE", 0, 3)    :    (2,0),        #    [--0]
        ("L-PIECE", 1, 3)    :    (0,-1),        #    [123]
        ("L-PIECE", 2, 3)    :    (1,-1),       #    
        ("L-PIECE", 3, 3)    :    (2,-1),       #    
        
        #T-PIECE
        #Base position : 0
        ("T-PIECE", 0, 0)    :    (1,0),    #    [-0-]
        ("T-PIECE", 1, 0)    :    (0,-1),   #    [123]
        ("T-PIECE", 2, 0)    :    (1,-1),    #    
        ("T-PIECE", 3, 0)    :    (2,-1),    #
        
        #First Rotation : 1
        ("T-PIECE", 0, 1)    :    (0,0),    #    [0-]
        ("T-PIECE", 1, 1)    :    (0,-1),   #    [12]
        ("T-PIECE", 2, 1)    :    (1,-1),   #    [3-]
        ("T-PIECE", 3, 1)    :    (0,-2),   #
        
        #Second Rotation : 2
        ("T-PIECE", 0, 2)    :    (0,0),    #    [012]
        ("T-PIECE", 1, 2)    :    (1,0),    #    [-3-]
        ("T-PIECE", 2, 2)    :    (2,0),    #    
        ("T-PIECE", 3, 2)    :    (1,-1),   #
        
        #Third Rotation : 3
        ("T-PIECE", 0, 3)    :    (1,0),    #    [-0]
        ("T-PIECE", 1, 3)    :    (0,-1),    #    [12]
        ("T-PIECE", 2, 3)    :    (1,-1),    #    [-3]
        ("T-PIECE", 3, 3)    :    (1,-2),   #
        
        #Base position : 0
        ("LINE", 0, 0)                :    (0,0),        #    [0]
        ("LINE", 1, 0)                :    (0,-1),        #    [1]
        ("LINE", 2, 0)                :    (0,-2),        #    [2]
        ("LINE", 3, 0)                :    (0,-3),        #    [3]
        
        #First Rotation: 1
        ("LINE", 0, 1)                :    (0,0),        #    [0123]
        ("LINE", 1, 1)                :    (1,0),       #    
        ("LINE", 2, 1)                :    (2,0),       #    
        ("LINE", 3, 1)                :    (3,0)        #    
    }
    return lookup_relative_position.get((shape, block_num, rotation), False)

    
"""
Tetris Pieces

"""

class TetrisPiece(object):
    
    def __init__(self, block_type = None, anchor_position = None, rotation = 0):
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
        return self.coordinates
    
    #Transformations only return coordinates, commit of new coordinates is implementation specific
    def transform_coordinates(self, rotate=0, adjust_x=0):
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
        
        if new_rotation == 0 and adjust_x == 0:
            log_error("No change to coordinates.")
            return False
            
        new_coordinates = []
        log_error("Transforming coordinates with New rotation = {} and Adjust_X = {} \n".format(new_rotation, adjust_x), "DEBUG")
        log_error("New Coordinates:", "DEBUG")
        for i in range(4): 
            rotation_modifier = relative_position(self.block_type, i, new_rotation)
            if rotation_modifier == False:
                log_error("Unable to rotate {} from position {} to position {} (Failed on i = {})".format(self.block_type, self.rotation, new_rotation, i))
                return False
            
            adjustment = add_coordinates(rotation_modifier, (adjust_x, 0))
       
            new_coordinates.append(add_coordinates(self.anchor_position, adjustment))
            log_error(new_coordinates[i], "DEBUG")
            
           
        return new_coordinates
        

    #Set new coordinates for each part of the piece
    def set_coordinates(self, new_coordinates):
        self.coordinates = new_coordinates
        return
    
    #What type of shape is this?
    def get_shape(self):
        return self.block_type
        
    def shape(self):
        return self.block_type
        
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