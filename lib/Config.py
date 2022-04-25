class Config(object):
    def __init__(self, designation):
        self.game = None
        self.game_mode = None
        
        if designation == "CLASSIC_TETRIS":
            #Basics
            self.game = "Tetrix"
            self.game_mode = "Classic Tetris"
            self.num_rows = 40 #Total height of the game board
            self.num_columns = 10 #Number of columns in the tetris board
            self.num_rows_display = int(self.num_rows/ 2) #Viewable region of the game board

            #Logger
            self.logger_level = "DEBUG"
            self.log_file_location = ".\\logs\\textris.log"
            
            #Display 
            self.pixels_x = 1024
            self.pixels_y = 768
            self.aspect_ratio = self.pixels_x / self.pixels_y
            
        else:
            log_error("Invalid Designation")
        