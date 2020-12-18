from lib.TetrisBlock import *


class Textrix(object):
	def __init__(self, **kwargs):
		pygame.init()
		
		self.init_logo()
		
		self.GameBoard = GameBoard(kwargs.get("board_width", 10), kwargs.get("board_height", 10))
		
		
	#Create the game board with all empty spaces

	if __name__ == "__main__":
		Textrix()