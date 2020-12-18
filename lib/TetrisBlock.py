#Predefine the shapes here
#Add ability to assign a tetris block as a part of a shape

block_types = [
"SQUARE",
"Z-PIECE",
"S-PIECE"
"LINE",
"FORWARDS-L",
"BACKWARDS-L"
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
		("LINE", 0, 0)				:	(0,0),		#	[0]
		("LINE", 1, 0)				:	(0,1),		#	[1]
		("LINE", 2, 0)				:	(0,2),		#	[2]
		("LINE", 3, 0)				:	(0,3),		#	[3]
		
		#Base position : 0
		("FORWARDS-L", 0, 0)	:	(0,0),		#	[0-]
		("FORWARDS-L", 1, 0)	:	(0,1),		#	[1-]
		("FORWARDS-L", 2, 0)	:	(0,2),		#	[23]
		("FORWARDS-L", 3, 0)	:	(1,2),		#	
		
		#Base position : 0
		("BACKWARDS-L", 0, 0)	:	(1,0),	#	[-0]
		("BACKWARDS-L", 1, 0)	:	(1,1),	#	[-1]
		("BACKWARDS-L", 2, 0)	:	(0,2),	#	[23]
		("BACKWARDS-L", 3, 0)	:	(1,2)	#	
	}
	return lookup_relative_position.get((shape, block_num), False)

logger_level = "DEBUG"
def log_map(level):
        lookup_log_map = {
                "DEBUG":0,
                "INFO":1,
                "ALERT":2,
                "ERROR":3
                }
        return lookup_log_map.get(level, 0)

def log_error(msg, msg_level = "ERROR"):
        #If level is DEBUG: always do
        #If level is INFO: only show when msg_level is
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

                #Validate Block type and position
                if self.block_type is not None:
                        if self.block_type not in block_types: 
                                log_error("Invalid block type")
				return false
			if self.anchor_position is None:
				log_error("Anchor Position not provided")
				return False

                        self.coordinates = []
			#Determine coordinates for all blocks in the shape
			for i in range(4):
                                self.coordinates[i] = self.anchor_position + relative_position(self.block_type, i, self.rotation)
                                log_error(self.coordinates[i], "DEBUG")
                                return False
                                
		def get_coordinates():
			return self.coordinates
		
		def get_shape():
			if shape not in block_types:
				log_error("not a valid block type")
				return False
				
			return self.block_type
                
"""

Game board

"""
	
class GameBoard(object):
	def __init__(rows, columns)
		self.num_rows		=	rows
		self.num_columns	=	columns
	
		self.coordinates = {}
	
		for x in range(num_rows):
			for y in range(num_columns):
				self.coordinates[(x,y)] = None
				
		return True
		
	def set(coordinate, shape):
		if shape not in block_types: 
			log_error("Not a valid shape")
			return False
			
		self.coordinates(coordinate) = shape
		return True
	
	def at(coordinate):
		(x, y) = coordinates
		if x < 0 or x >= self.num_rows or y < 0 or y >= self.num_columns:
			log_error("invalid coordinates")
			return False
			
		return self.coordinates[coordinate]
				
				
		
if __name__ == "__main__":
        #Run basic tests of functionality
        test_square = TetrisBlock("SQUARE", (0,0), 0)
