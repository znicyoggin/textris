#Predefine the shapes here
#Add ability to assign a tetris block as a part of a shape

block_types = [
"SQUARE",
"Z-PIECE",
"S-PIECE",
"L-PIECE",
"J-PIECE",
"T-PIECE"
"LINE"
]

def relative_position(shape, block_num, rotation):
	#lookup relative position for any block of any shape
	lookup_relative_position = {			# (x, y)
		#Base position : 0
		("SQUARE", 0, 0)			:	(0,0),		#	[01-]
		("SQUARE", 1, 0)			:	(1,0),		#	[23-]
		("SQUARE", 2, 0)			:	(0,1),		#	
		("SQUARE", 3, 0)			:	(1,1),		#	
		
		#Base position : 0
		("Z-PIECE", 0, 0)			:	(0,0),		#	[01-]
		("Z-PIECE", 1, 0)			:	(1,0),		#	[-23]
		("Z-PIECE", 2, 0)			:	(1,1),		#	
		("Z-PIECE", 3, 0)			:	(2,1),		#	
		
		#Base position : 0
		("S-PIECE", 0, 0)			:	(1,0),		#	[-01]
		("S-PIECE", 1, 0)			:	(2,0),		#	[23-]
		("S-PIECE", 2, 0)			:	(0,1),		#	
		("S-PIECE", 3, 0)			:	(1,1),		#	

		#Base position : 0
		("L-PIECE", 0, 0)	:	(0,0),		#	[0-]
		("L-PIECE", 1, 0)	:	(0,1),		#	[1-]
		("L-PIECE", 2, 0)	:	(0,2),		#	[23]
		("L-PIECE", 3, 0)	:	(1,2),		#	
		
		#Base position : 0
		("J-PIECE", 0, 0)	:	(1,0),	#	[-0]
		("J-PIECE", 1, 0)	:	(1,1),	#	[-1]
		("J-PIECE", 2, 0)	:	(0,2),	#	[23]
		("J-PIECE", 3, 0)	:	(1,2),	#
			
		#Base position : 0
		("T-PIECE", 0, 0)	:	(1,0),	#	[-0-]
		("T-PIECE", 1, 0)	:	(0,1),	#	[123]
		("T-PIECE", 2, 0)	:	(1,1),	#	
		("T-PIECE", 3, 0)	:	(2,1),	#
		
		#Base position : 0
		("LINE", 0, 0)				:	(0,0),		#	[0]
		("LINE", 1, 0)				:	(0,1),		#	[1]
		("LINE", 2, 0)				:	(0,2),		#	[2]
		("LINE", 3, 0)				:	(0,3)		#	[3]
	}
	return lookup_relative_position.get((shape, block_num, rotation), False)

logger_level = "DEBUG"
def log_map(level):
        lookup_log_map = {
                "DEBUG"	: 0,
                "INFO"		: 1,
                "ALERT"	: 2,
                "ERROR"	: 3
                }
        return lookup_log_map.get(level, 0)

def log_error(msg, msg_level = "ERROR"):
        curr_weight = log_map(logger_level)
        msg_weight = log_map(msg_level)
        
        if msg_weight >= curr_weight:
	        print(msg)

	
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
			
		#Determine coordinates for all blocks in the shape
		log_error("Displaying initial coordinates for {}".format(self.block_type), "DEBUG")
		for i in range(4):
			rotation_modifier = relative_position(self.block_type, i, self.rotation)
			if rotation_modifier == False:
				log_error("Unable to rotate {} {} {}".format(self.block_type, self.rotation, "time" if rotation == 1 else "times"))
				return
			self.coordinates.append(tuple(map(lambda i, j: i + j, self.anchor_position, rotation_modifier)))
			log_error(self.coordinates[i], "DEBUG")
                
				
	def get_coordinates(self):
		return self.coordinates
	
	def get_shape(self):
					return self.block_type
			
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
	
                
"""

Game board

"""
	
class GameBoard(object):
	def __init__(self, rows, columns):
		self.num_rows		=	rows
		self.num_columns	=	columns
	
		self.coordinates = {}
	
		for x in range(num_rows):
			for y in range(num_columns):
				self.coordinates[(x,y)] = None
				
		return True
		
	def set(self, coordinate, shape):
		if shape not in block_types: 
			log_error("Not a valid shape")
			return False
			
		self.coordinates[coordinate] = shape
		return True
	
	def at(coordinate):
		(x, y) = coordinates
		if x < 0 or x >= self.num_rows or y < 0 or y >= self.num_columns:
			log_error("invalid coordinates")
			return False
			
		return self.coordinates[coordinate]
				
				
		
if __name__ == "__main__":
	#Run basic tests of functionality
	test_square 	= TetrisPiece("SQUARE", (0,0), 0)
	test_zpiece		= TetrisPiece("Z-PIECE", (11,32), 0)
	test_circle		= TetrisPiece("CIRCLE", (0,0), 0)
	test_nowhere		= TetrisPiece("SQUARE")
	test_bad_loc		= TetrisPiece("SQUARE", 22)
	test_rotate_1 = TetrisPiece("LINE", (0,0), 1)	
	test_rotate_2 = TetrisPiece("S-PIECE", (22,11), 3)
