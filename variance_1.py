# You need to import colorfight for all the APIs
import colorfight
import random
import datetime
import math

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
    ACTION_ARRAY = [Actions.EVAL, Actions.SORT,
                    Actions.DO_NOTHING, Actions.DO_NOTHING, Actions.DO_NOTHING, Actions.DO_NOTHING,
                    Actions.DO_NOTHING, Actions.DO_NOTHING, Actions.DO_NOTHING, Actions.DO_NOTHING]
    action_index = 0
    current_action = ACTION_ARRAY[action_index]
    evaled_cells = {}
    sorted_cells = []
    pre_dist_to_global_high = 60
    cur_dist_to_global_high = 60

    # Last attacked cell information
    last_attack_time = datetime.datetime.now()
    last_attack_cell = ()

    # Defense variables
    border_cells = []
    my_coor = []

    # Instantiate a Game object.
    g = colorfight.Game()
    # You need to join the game using JoinGame(). 'MyAI' is the name of your
    # AI, you can change that to anything you want. This function will generate
    # a token file in the folder which preserves your identity so that you can
    # stop your AI and continue from the last time you quit.
    # If there's a token and the token is valid, JoinGame() will continue. If
    # not, you will join as a new player.
    g.JoinGame('bubo_4_enemy')
    # Put you logic in a while True loop so it will run forever until you
    # manually stop the game

    def eval_this_cell_global(cur_x, cur_y):
        this_cell_global_val = 0
        for x in range(cur_x - 3, cur_x + 3):
            for y in range(cur_y - 3, cur_y + 3):
                this_cell = g.GetCell(x, y)
                neighbors = set()

                if this_cell != None:
                    if this_cell.owner != g.uid:
                        if this_cell.owner == 0:
                            this_cell_global_val -= 2
                        else:
                            if this_cell.owner in neighbors:
                                this_cell_global_val += 1
                            this_cell_global_val -= this_cell.takeTime
                    if this_cell.cellType == "gold":
                        this_cell_global_val += 6
                else:
                    this_cell_global_val += 4
        evaled_cells[(cur_x, cur_y)] = this_cell_global_val

    def sort_all_eval():
        sorted_cells = sorted(evaled_cells, key=evaled_cells.get, reverse=True)

    while True:
        # This is the step to sort from high to low the value of cells
        if current_action == Actions.SORT:
            sort_all_eval()

        # Now carry out the attack
        # Go through the array of cells, evaluate, and search for a highest value
        # that is adjacent to my cells
        # If found a value of 3, stop searching
        # (since this is highest value possible)
        highest_val = float('-inf')
        highest_val_coor = (0, 0)
        sec_highest_val = float('-inf')
        sec_highest_val_coor = (0, 0)
        cur_x = 0
        cur_y = 0
        direct_dirs = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        diagonal_dirs = [[1, 1], [1, -1], [-1, -1], [-1, 1]]

        while (cur_x < g.width and cur_y < g.height):
            if current_action == Actions.EVAL:
                eval_this_cell_global(cur_x, cur_y)
                my_coor = []

            is_adjacent = False
            this_cell = g.GetCell(cur_x, cur_y)
            this_cell_val = (4 / this_cell.takeTime)
            if this_cell.owner == 0:
                this_cell_val += 1
            else:
                this_cell_val -= this_cell.takeTime / 3
            if this_cell.cellType == "gold" and this_cell.takeTime < 12:
                this_cell_val += 10
            if not this_cell.owner == g.uid:
                neighbors = set()
                if current_action == Actions.DO_NOTHING:
                    for i in range(3):
                        dist = abs(sorted_cells[i][0] - cur_x) + abs(sorted_cells[i][1])
                        if  dist < pre_dist_to_global_high:
                            this_cell_val += 4 * math.e ** (- 0.1 * (dist - 8) ** 2)
                            pre_dist_to_global_high = dist
                for i in direct_dirs:
                    # Directly adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    # Number of my cells around
                    num_my_cell = 0

                    if not sur_c == None:
                        if sur_c.cellType == "gold" and this_cell.takeTime < 12:
                            this_cell_val += 8
                        if sur_c.owner == g.uid:
                            is_adjacent = True
                            this_cell_val += ((g.currTime - sur_c.occupyTime) / 40)
                            num_my_cell += 1
                        elif sur_c.owner == 0:
                            this_cell_val += 2
                        else:
                            if sur_c.owner in neighbors:
                                this_cell_val += (4 / sur_c.takeTime)
                            this_cell_val += (4 / sur_c.takeTime)
                            neighbors.add(sur_c.owner)
                    else:
                        this_cell_val += 2
                for i in diagonal_dirs:

                    # Diagonally adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    if not sur_c == None:
                        if sur_c.cellType == "gold" and this_cell.takeTime < 12:
                            this_cell_val += 6
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
                        this_cell_val += 2
                else:
                    this_cell_val -= (this_cell.takeTime * 3)
                    my_coor += [(cur_x, cur_y)]

            this_cell_val += num_my_cell
            
            if this_cell_val > highest_val and is_adjacent and not this_cell.owner == g.uid:
                highest_val = this_cell_val
                highest_val_coor = (cur_x, cur_y)
            elif this_cell_val < highest_val and this_cell_val > sec_highest_val and is_adjacent and not this_cell.owner == g.uid:
                sec_highest_val = this_cell_val
                sec_highest_val_coor = (cur_x, cur_y)

            # Update coordinate
            temp_x = cur_x
            cur_x = (temp_x + 1) % g.width
            cur_y = cur_y + (temp_x + 1) // g.width

        now = datetime.datetime.now()
        timedelta = (now - last_attack_time).total_seconds()
        if (now - last_attack_time).total_seconds() > 0.5 and (highest_val_coor) != last_attack_cell:
            if not g.GetCell(highest_val_coor[0], highest_val_coor[1]).isTaking:
                print(g.AttackCell(highest_val_coor[0], highest_val_coor[1]), "x-value", highest_val_coor[0], "y-value", highest_val_coor[1])
                last_attack_time = datetime.datetime.now()
                last_attack_cell = (highest_val_coor[0], highest_val_coor[1])
        elif (now - last_attack_time).total_seconds() > 0.5 and (sec_highest_val_coor) != last_attack_cell:
            if not g.GetCell(sec_highest_val_coor[0], sec_highest_val_coor[1]).isTaking:
                print(g.AttackCell(sec_highest_val_coor[0], sec_highest_val_coor[1]), "x-value", sec_highest_val_coor[0], "y-value", highest_val_coor[1])
                last_attack_time = datetime.datetime.now()
                last_attack_cell = (sec_highest_val_coor[0], sec_highest_val_coor[1])

        action_index = (action_index + 1) % 2
        current_action = ACTION_ARRAY[action_index]

        g.Refresh()
