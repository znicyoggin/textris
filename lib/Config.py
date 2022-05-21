class Config(object):
    def __init__(self, designation):
        self.game = None
        self.game_mode = None
        
        if designation == "CLASSIC_TETRIS":
            #Basics
            self.game = "Tetrix"
            self.game_mode = "Classic Tetris"
            self.num_rows = 24 #Total height of the game board
            self.num_columns = 10 #Number of columns in the tetris board
            self.num_rows_display = 20 #Viewable region of the game board

            #Game related parameters
            self.max_fps = 40
            #Logger
            self.logger_level = "DEBUG"
            self.log_file_location = ".\\logs\\textris.log"
            
            #Display 
            self.pixels_x = 500
            self.pixels_y = 1000
            self.aspect_ratio = self.pixels_x / self.pixels_y
            self.block_dimensions = (50, 40)
            #Image Locations
            self.image_location_blocks = ".//img//blocks"
            
            #Number of ticks that pass before the tetris piece falls again
            self.level_based_gravity = [1000, 800, 600, 400, 200, 100]
            
            #Number of ticks that must pass before you can move again
            self.move_time = 200
            
            #Move x times faster when you hold left/right button
            self.holding_button_move_multiplier = 2
            
            #Fall x times faster when you hold the fall button
            self.fast_fall_speed_multiplier = 2
            
        else:
            log_error("Invalid Designation")
        