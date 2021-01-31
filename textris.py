from lib.GameBoard import *
from lib.signal import *
import time


def main ():    
    #Load default tetris rules
    config = Config("CLASSIC_TETRIS")
    
    #Keep time
    
    
    #set defaults
    num_rows = config.num_rows 
    num_cols = config.num_columns
    display_cols = config.hide_column_count
    textris= GameBoard(num_rows, num_cols)
    
    right = True
    left = False
    clockwise = True
    counterclockwise = False
    
    #main loop
    time_threshold = 100000 #100 ms

    while(1):
        print("Beginning of while loop.  {} is falling".format("Something" if textris.falling() else "Nothing"))
        #Generate a random new tetris block
        new_block_type = random_shape()
        #print("Dropping {}".format(new_block_type))
        #textris.place_block(new_block_type, textris.DropSpot())
        textris.place_block("L-PIECE", textris.DropSpot())

        
        i = 0
        while textris.falling():
            
            if i + display_cols >= num_cols: 
                
                textris.display_board(display_cols)
                #Move left / right
                dir = input("a=left, d=right, q=counter-clockwise, e=clockwise")

                if dir == "a": textris.move_lateral(left)
                elif dir == "d": textris.move_lateral(right)
                elif dir == "q": textris.rotate(counterclockwise)
                elif dir == "e": textris.rotate(clockwise)

                print("\r\n\r\n")
                #When lines are eliminated, add to the score
                #textris.update_stats(3)
            textris.apply_gravity()
            textris.cleanup()
            i += 1
            
if __name__ == "__main__":
    main()

