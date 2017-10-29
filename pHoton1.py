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
    ACTION_ARRAY = [Actions.DO_NOTHING, Actions.EVAL, Actions.DO_NOTHING, Actions.SORT]
    action_index = 0
    current_action = ACTION_ARRAY[action_index]
    raw_array = []
    last_attack_time = datetime.datetime.now()
    last_attack_cell = ()

    # Defense variables
    border_cells = []

    # Instantiate a Game object.
    g = colorfight.Game()
    # You need to join the game using JoinGame(). 'MyAI' is the name of your
    # AI, you can change that to anything you want. This function will generate
    # a token file in the folder which preserves your identity so that you can
    # stop your AI and continue from the last time you quit.
    # If there's a token and the token is valid, JoinGame() will continue. If
    # not, you will join as a new player.
    g.JoinGame('pHoton_0')
    # Put you logic in a while True loop so it will run forever until you
    # manually stop the game

    def eval_all_cells():
        return "stub"

    def sort_all_eval():
        return "stub"

    while True:
        # This is the step to evaluate all the cell status for a global view
        if current_action == Actions.EVAL:
            eval_all_cells()

        # This is the step to sort from high to low the value of cells
        elif current_action == Actions.SORT:
            sortAll()

        # Now carry out the attack
        # Go through the array of cells, evaluate, and search for a highest value
        # that is adjacent to my cells
        # If found a value of 3, stop searching
        # (since this is highest value possible)
        highest_val = float('-inf')
        highest_val_coor = (0, 0)
        cur_x = 0
        cur_y = 0
        direct_dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        diagonal_dirs = [[1, 1], [1, -1], [-1, -1], [-1, 1]]

        while (cur_x < g.width and cur_y < g.height):
            is_adjacent = False
            this_cell = g.GetCell(cur_x, cur_y)
            this_cell_val = (4 / this_cell.takeTime)
            if this_cell.owner == 0:
                this_cell_val += 1
            else:
                this_cell_val -= this_cell.takeTime / 3

            if not this_cell.owner == g.uid:
                neighbors = set()
                for i in direct_dirs:
                    # Directly adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    if not sur_c == None:
                        if sur_c.owner == g.uid:
                            is_adjacent = True
                            this_cell_val += ((g.currTime - sur_c.occupyTime) / 30)
                        elif sur_c.owner == 0:
                            this_cell_val += 2
                        else:
                            if sur_c.owner in neighbors:
                                this_cell_val += (2 / sur_c.takeTime)
                            this_cell_val += (4 / sur_c.takeTime)
                            neighbors.add(sur_c.owner)
                    else:
                        this_cell_val += 3.3

                for i in diagonal_dirs:
                    # Diagonally adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    if not sur_c == None:
                        if sur_c.owner == 0:
                            this_cell_val += 1
                        elif sur_c.owner == g.uid:
                            this_cell_val += 3
                        else:
                            if sur_c.owner in neighbors:
                                this_cell_val += (2 / sur_c.takeTime)
                            this_cell_val += (3 / sur_c.takeTime)
                            neighbors.add(sur_c.owner)
                    else:
                        this_cell_val += 3.3
                else:
                    this_cell_val -= (this_cell.takeTime * 3)

            if this_cell_val > highest_val and is_adjacent and not this_cell.owner == g.uid:
                highest_val = this_cell_val
                highest_val_coor = (cur_x, cur_y)

            # Update coordinate
            temp_x = cur_x
            cur_x = (temp_x + 1) % g.width
            cur_y = cur_y + (temp_x + 1) // g.width

        now = datetime.datetime.now()
        timedelta = (now - last_attack_time).total_seconds()
        if (now - last_attack_time).total_seconds() > 2.0 and (highest_val_coor) != last_attack_cell:
                print(g.AttackCell(highest_val_coor[0], highest_val_coor[1]), "x-value", highest_val_coor[0], "y-value", highest_val_coor[1])
                last_attack_time = datetime.datetime.now()
                print("highest val", highest_val)
                last_attack_cell = (highest_val_coor[0], highest_val_coor[1])

        action_index = (action_index + 1) % 2
        current_action = ACTION_ARRAY[action_index]

        g.Refresh()
