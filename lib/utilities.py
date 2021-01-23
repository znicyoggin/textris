from random import randrange

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

score_calc = [100, 250, 500, 1000]

def random_shape():
    return block_types[randrange(len(block_types))]
    
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
        ("L-PIECE", 0, 0)    :    (0,0),        #    [0-]
        ("L-PIECE", 1, 0)    :    (0,-1),       #    [1-]
        ("L-PIECE", 2, 0)    :    (0,-2),       #    [23]
        ("L-PIECE", 3, 0)    :    (1,-2),       #    
        
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

def combine_unique(list_1, list_2):
    list_3 = list_1.copy()
    for element in list_2:
        if element in list_1: continue
        else: list_3.append(element)
    return list_3
    
def add_coordinates(coord_1, coord_2):
    x1, y1 = coord_1
    x2, y2 = coord_2
    return (x1+x2, y1+y2)
    