from TetrisBlock import *
from logger import *
from Config import *

"""

Game board

"""
	
class GameBoard(object):
	def __init__(self, rows, columns):
		self.num_rows		=	rows
		self.num_columns	=	columns
	
		self.coordinates = {}
	
		for x in range(self.num_rows):
			for y in range(self.num_columns):
				self.coordinates[(x,y)] = None
				
		
		
	def set(self, coordinate, shape):
		if shape not in block_types: 
			log_error("Not a valid shape")
			return False
			
		self.coordinates[coordinate] = shape
		return True
	
	def at(self, coordinate):
		(x, y) = coordinates
		if x < 0 or x >= self.num_rows or y < 0 or y >= self.num_columns:
			log_error("invalid coordinates")
			return False
			
		return self.coordinates[coordinate]
		
if __name__ == "__main__":
	config = Config("CLASSIC_TETRIS")
	
	num_rows = config.num_rows 
	num_cols = config.num_columns
	test_game_board = GameBoard(num_rows, num_cols)
	
	test_coordinates = (4, 2)
	test_game_board.set(test_coordinates, "LINE")
	print(test_game_board.at(test_coordinates))
	
				
	