# You need to import colorfight for all the APIs
import colorfight
import random
import datetime
import math
import copy

class Actions:
    DO_NOTHING = 0
    EVAL = 1
    SORT = 2


class CellStatus:
    MY_CELL = 0
    EMPTY = 2
    OCCUPIED_LOW = 1
    OCCUPIED_HIGH = -1


class Mode:
    NORMAL = 0
    ATTACK_BASE = 1
    BORDER_DEFENSE = 2
    BASE_DEFENSE = 3


class BaseDefense:
    BUILD = 0
    DEFEND = 1


class BaseValue:
    ATTACK = 20
    SURROUNDING = 10


class BaseStrategyValue:
    ATTACK = 10
    SURROUNDING_DIR = 40
    SURROUNDING_COR = 30

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

    log_highest_coor = []
    # Last attacked cell information
    last_attack_time = datetime.datetime.now()
    last_attack_cell = ()

    # Defense variables
    border_cells = []
    my_coor = []

    base_defense = None

    # My base
    my_base = []

    # mode
    mode = Mode.NORMAL

    # Instantiate a Game object.
    g = colorfight.Game()
    # You need to join the game using JoinGame(). 'MyAI' is the name of your
    # AI, you can change that to anything you want. This function will generate
    # a token file in the folder which preserves your identity so that you can
    # stop your AI and continue from the last time you quit.
    # If there's a token and the token is valid, JoinGame() will continue. If
    # not, you will join as a new player.
    g.JoinGame('geekowl')
    # Put you logic in a while True loop so it will run forever until you
    # manually stop the game


    def get_ranking(user_id):
        sorted_users = copy.deepcopy(g.users)
        sorted_users.sort(key=lambda x: x.cellNum)
        user_ranking = [u.id for u in sorted_users]
        return user_ranking.index(user_id) + 1

    def eval_this_cell_global(cur_x, cur_y):
        this_cell_global_val = 0

        for x in range(cur_x - 2, cur_x + 2):
            for y in range(cur_y - 2, cur_y + 2):
                this_cell = g.GetCell(x, y)

                if this_cell != None:
                    if this_cell.owner != g.uid:
                        if this_cell.owner == 0:
                            this_cell_global_val -= 1
                        else:
                            this_cell_global_val -= this_cell.takeTime
                            this_cell_global_val += (8 / get_ranking(this_cell.owner))
                    if this_cell.cellType == "gold":
                        this_cell_global_val += 6
                    if this_cell.cellType == "energy":
                        this_cell_global_val += 10
                else:
                    this_cell_global_val += 2
        evaled_cells[(cur_x, cur_y)] = this_cell_global_val

    def sort_all_eval():
        sorted_cells = sorted(evaled_cells, key=evaled_cells.get, reverse=True)

    def base_or_defend():
        # Decide if build new base or defend the old one
        "stub"

    def attack_base(x, y):
        # Check if the enemy base has all my cells around
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        if g.GetCell(x, y).owner == g.uid:
            return False
        for i in directions:
            if g.GetCell(x + i[0], y + i[1]) != None:
                if g.GetCell(x + i[0], y + i[1]).owner != g.uid:
                    return False
        return True

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
        thir_highest_val = float('-inf')
        thir_highest_val_coor = (0, 0)
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
            this_cell_val = (6 / this_cell.takeTime)
            if this_cell.owner == 0:
                this_cell_val += 1
            else:
                this_cell_val -= this_cell.takeTime / 3
            if this_cell.cellType == "gold" and this_cell.takeTime < 8:
                this_cell_val += 8
            if this_cell.cellType == "energy" and this_cell.takeTime < 8:
                this_cell_val += 10
            if this_cell.isBase:
                if attack_base(cur_x, cur_y):
                    print(g.AttackCell(cur_x, cur_y), "kill base")
                    last_attack_cell = (cur_x, cur_y)
                else:
                    this_cell_val += BaseValue.SURROUNDING
            if not this_cell.owner == g.uid:
                neighbors = set()
                if current_action == Actions.DO_NOTHING:
                    for i in range(3):
                        dist = abs(sorted_cells[i][0] - cur_x) + abs(sorted_cells[i][1])
                        if  dist < pre_dist_to_global_high:
                            this_cell_val += 10 * math.e ** (- 0.1 * (dist - 8) ** 2)
                            pre_dist_to_global_high = dist
                for i in direct_dirs:
                    # Directly adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    # Number of my cells around
                    num_my_cell = 0

                    if not sur_c == None:
                        if sur_c.cellType == "gold" and this_cell.takeTime < 8:
                            this_cell_val += 6
                        if sur_c.cellType == "energy" and this_cell.takeTime < 12:
                            this_cell_val += 10
                        if sur_c.owner == g.uid:
                            is_adjacent = True
                            this_cell_val += ((g.currTime - sur_c.occupyTime) / 40)
                            num_my_cell += 1
                            if sur_c.isBase and this_cell.owner == 0:
                                print(g.AttackCell(cur_x, cur_y), "Empty around base")
                                last_attack_cell = (cur_x, cur_y)
                        elif sur_c.owner == 0:
                            this_cell_val += 2
                        else:
                            if sur_c.owner in neighbors:
                                this_cell_val += (4 / sur_c.takeTime)
                            this_cell_val += (4 / sur_c.takeTime)
                            this_cell_val += (6 / get_ranking(sur_c.owner))
                            if sur_c.isBase:
                                this_cell_val += 35

                            neighbors.add(sur_c.owner)
                    else:
                        this_cell_val += 2
                for i in diagonal_dirs:
                    # Diagonally adjacent cells
                    sur_c = g.GetCell(cur_x + i[0], cur_y + i[1])
                    if not sur_c == None:
                        if sur_c.cellType == "gold" and this_cell.takeTime < 8:
                            this_cell_val += 4
                        if sur_c.cellType == "energy" and this_cell.takeTime < 12:
                            this_cell_val += 8
                        if sur_c.owner == 0:
                            this_cell_val += 1
                        elif sur_c.owner == g.uid:
                            this_cell_val += 3
                            num_my_cell += 0.5
                        else:
                            if sur_c.owner in neighbors:
                                this_cell_val += (4 / sur_c.takeTime)
                            this_cell_val += (4 / sur_c.takeTime)
                            this_cell_val += (6 / get_ranking(sur_c.owner))
                            if sur_c.isBase:
                                this_cell_val += 30
                            neighbors.add(sur_c.owner)
                    else:
                        this_cell_val += 4
                else:
                    this_cell_val -= (this_cell.takeTime * 2)
                    if this_cell.isBase:
                        my_base = (cur_x, cur_y)

            this_cell_val += ((2 / this_cell.takeTime) * num_my_cell ** 3)

            if this_cell_val > highest_val and is_adjacent and not this_cell.owner == g.uid:
                highest_val = this_cell_val
                highest_val_coor = (cur_x, cur_y)
            elif this_cell_val < highest_val and this_cell_val > sec_highest_val and is_adjacent and not this_cell.owner == g.uid:
                sec_highest_val = this_cell_val
                sec_highest_val_coor = (cur_x, cur_y)
            elif this_cell_val < sec_highest_val and this_cell_val > thir_highest_val and is_adjacent and not this_cell.owner == g.uid:
                thir_highest_val = this_cell_val
                thir_highest_val_coor = (cur_x, cur_y)

            # Update coordinate
            temp_x = cur_x
            cur_x = (temp_x + 1) % g.width
            cur_y = cur_y + (temp_x + 1) // g.width

        now = datetime.datetime.now()
        timedelta = (now - last_attack_time).total_seconds()
        if (highest_val_coor) != last_attack_cell:
            if not g.GetCell(highest_val_coor[0], highest_val_coor[1]).isTaking:
                print(g.AttackCell(highest_val_coor[0], highest_val_coor[1]), highest_val_coor[0], highest_val_coor[1], highest_val)
                last_attack_time = datetime.datetime.now()
                last_attack_cell = (highest_val_coor[0], highest_val_coor[1])
        elif (sec_highest_val_coor) != last_attack_cell:
            if not g.GetCell(sec_highest_val_coor[0], sec_highest_val_coor[1]).isTaking:
                print(g.AttackCell(sec_highest_val_coor[0], sec_highest_val_coor[1]), sec_highest_val_coor[0], sec_highest_val_coor[1], sec_highest_val)
                last_attack_time = datetime.datetime.now()
                last_attack_cell = (sec_highest_val_coor[0], sec_highest_val_coor[1])
        elif (thir_highest_val_coor) != last_attack_cell:
            if not g.GetCell(thir_highest_val_coor[0], thir_highest_val_coor[1]).isTaking:
                print(g.AttackCell(thir_highest_val_coor[0], thir_highest_val_coor[1]), thir_highest_val_coor[0], thir_highest_val_coor[1])
                last_attack_time = datetime.datetime.now()
                last_attack_cell = (thir_highest_val_coor[0], thir_highest_val_coor[1])

        action_index = (action_index + 1) % 2
        current_action = ACTION_ARRAY[action_index]

        g.Refresh()
