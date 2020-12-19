from logger import *

class Config(object):
	def __init__(self, designation):
		self.game = None
		self.game_mode = None
		
		if designation == "CLASSIC_TETRIS":
			self.game = "Tetrix"
			self.game_mode = "Classic Tetris"
			self.num_rows = 10
			self.num_columns = 20
			
		else:
			log_error("Invalid Designation")
		