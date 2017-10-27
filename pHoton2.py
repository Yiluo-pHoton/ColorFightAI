# You need to import colorfight for all the APIs
import colorfight
import random
import datetime

class Actions:
    DO_NOTHING = 0
    EVAL = 1
    SORT = 2


class CellStatus:
    MY_CELL = 0
    EMPTY = 2
    OCCUPIED_LOW = 1
    OCCUPIED_HIGH = -1


if __name__ == '__main__':
    ACTION_ARRAY = [Actions.DO_NOTHING, Actions.DO_NOTHING]
    action_index = 0
    current_action = ACTION_ARRAY[action_index]
    raw_array = []
    last_attack_time = datetime.datetime.now() 

    # Instantiate a Game object.
    g = colorfight.Game()
    # You need to join the game using JoinGame(). 'MyAI' is the name of your
    # AI, you can change that to anything you want. This function will generate
    # a token file in the folder which preserves your identity so that you can
    # stop your AI and continue from the last time you quit. 
    # If there's a token and the token is valid, JoinGame() will continue. If
    # not, you will join as a new player.
    g.JoinGame('pHoton2')
    # Put you logic in a while True loop so it will run forever until you 
    # manually stop the game
    while True:
        
        # This is the step to evaluate all the cell status
        if current_action == Actions.EVAL:
            "stub"
        #    # Use a nested for loop to iterate through the cells on the map
        #    for x in range(g.width):
        #        raw_row = []
        #        for y in range(g.height):
        #            # Get a cell
        #            c = g.GetCell(x,y)
        #            # Assume this cell is empty
        #            this_cell = CellStatus.EMPTY
        #            # If the cell I got is mine
        #            if c.owner == g.uid:
        #                this_cell = CellStatus.MY_CELL
        #            elif not c.owner == 0:
        #                this_cell = CellStatus.OCCUPIED_HIGH
        #            raw_row += [this_cell]
        #        raw_array.append(raw_row)
        
        # This is the step to sort from high to low the value of cells
        elif current_action == Actions.SORT:
            "stub"
        
        # Now carry out the attack
        # Go through the array of cells, evaluate, and search for a highest value 
        # that is adjacent to my cells
        # If found a value of 3, stop searching 
        # (since this is highest value possible)
        highest_val = float('-inf')
        highest_val_coor = (0, 0)
        cur_x = 0
        cur_y = 0
        have_attacked = False
        direct_dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        diagonal_dirs = [[1, 1], [1, -1], [-1, -1], [-1, 1]]

        while not have_attacked and (cur_x < g.width and cur_y < g.height):
            is_adjacent = False
            this_cell = g.GetCell(cur_x, cur_y)
            this_cell_val = 0
            
            if this_cell.owner == 0:
                for i in direct_dirs:
                    # Directly adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    if not sur_c == None:
                        if sur_c.owner == g.uid:
                            is_adjacent = True
                        elif sur_c.owner == 0:
                            this_cell_val += 1
                        else:
                            this_cell_val -= 2
                for i in diagonal_dirs:
                    # Diagonally adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    if not sur_c == None:
                        if sur_c.owner == 0:
                            this_cell_val += 1
                        elif not sur_c.owner == g.uid:
                            this_cell_val -= 1
                
                now = datetime.datetime.now()
                timedelta = (now - last_attack_time).total_seconds()
                # If this cell is adjacent to my cell and all surrounding cells are empty
                if (is_adjacent and this_cell_val == 8) and (now - last_attack_time).total_seconds() > 2.0:
                    print(g.AttackCell(cur_x, cur_y), "x-value:", cur_x, "y-value:", cur_y)
                    last_attack_time = datetime.datetime.now()
                    print(last_attack_time)
                    print(timedelta)
                    have_attacked = True
            else:
                this_cell_val = -1

            if this_cell_val > highest_val and is_adjacent and not this_cell.owner == g.uid:
                highest_val = this_cell_val
                highest_val_coor = (cur_x, cur_y)

            # Update coordinate
            temp_x = cur_x
            cur_x = (temp_x + 1) % g.width
            cur_y = cur_y + (temp_x + 1) // g.width
        
        now = datetime.datetime.now()
        timedelta = (now - last_attack_time).total_seconds()
        if not have_attacked and (now - last_attack_time).total_seconds() > 2.0:
            if not g.GetCell(highest_val_coor[0], highest_val_coor[1]).owner == g.uid:
                print(g.AttackCell(highest_val_coor[0], highest_val_coor[1]), "x-value", highest_val_coor, "y-value", highest_val_coor[1])
                last_attack_time = datetime.datetime.now()
                print (last_attack_time)
                print(timedelta)

        action_index = (action_index + 1) % 2
        current_action = ACTION_ARRAY[action_index]
        
        g.Refresh()
