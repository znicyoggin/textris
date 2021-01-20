from lib.logger import *

class Config(object):
    def __init__(self, designation):
        self.game = None
        self.game_mode = None
        
        if designation == "CLASSIC_TETRIS":
            self.game = "Tetrix"
            self.game_mode = "Classic Tetris"
            self.num_rows = 10
            self.num_columns = 40
            self.hide_column_count = int(self.num_columns/ 2)
            
        else:
            log_error("Invalid Designation")
        