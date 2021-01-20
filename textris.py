from lib.GameBoard import *


def main ():    
    #Load default tetris rules
    config = Config("CLASSIC_TETRIS")
    
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
    for j in range(40):
        #Generate a random new tetris block
        print("Falling" if textris.falling() else "Not falling")
        new_block_type = random_shape()
        textris.place_block(new_block_type, textris.DropSpot())
        
        for i in range(40):
            if i + display_cols >= num_cols: 
                print("{} is falling".format("Something" if textris.falling() else "Nothing"))
                textris.display_board(display_cols)
                #Move left / right
                dir = input("a=left, d=right, q=counter-clockwise, e=clockwise")

                if dir == "a": textris.move_lateral(left)
                elif dir == "d": textris.move_lateral(right)
                elif dir == "q": textris.rotate(counterclockwise)
                elif dir == "e": textris.rotate(clockwise)

                print("\r\n\r\n")
            textris.apply_gravity()
            
if __name__ == "__main__":
    main()

