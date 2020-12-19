import random
from os import system
import time

# By Walter Alcazar
# Wumpus World.
# Goal of the game is to reach the pot of gold and get back to the starting square.
class World:
    # 0 = safe spot
    # 1 = bottomless pit
    # 2 = wumpus creature
    # 3 = pot of gold
    # 7 = starting square

    # initial difficulty will be from 1 to 3
    def __init__(self, difficulty):
        self.__size_limit = 8
        self.__directions = ['n', 'e', 's', 'w']
        self.__current_position = ()
        self.current_sense = ()
        self.__facing_direction = None
        self.__gold_recovered = False
        self.__cycle_action = 0
        self.__wumpus_face = [[" z|^) ", "Zz|^) ", "Z |^) ", "  |^) "], ["> :^( ", " >:^( ", " >=^( ", " >:^O "]]

        self.__blank_row = "|" + "      |" * self.__size_limit + "\n"
        self.__blank_border = "|" + "------|" * self.__size_limit + "\n"
        self.__top_bot = "-" + "-------" * self.__size_limit + "\n"

        if difficulty == 1:
            self.__easy_difficulty()
        elif difficulty == 2:
            self.__medium_difficulty()
        else:
            self.__hard_difficulty()

        self.__tornado_landing()

    def __tornado_landing(self):
        self.__current_position = random.choice(self.__starting_positions)
        self.__original_position = self.__current_position
        self.__facing_direction = random.choice(self.__directions)
        (x, y) = self.__current_position

        self.current_sense = self.__sensory_world[x][y]

    # return result is tuple boolean (can_move_forward, can_move_backward)
    def __available_movement(self):
        (x, y) = self.__current_position
        # movement restrictions are forwards and backwards options
        result = (False, False)
        if self.__facing_direction == 'n':
            result = (True if y + 1 < self.__size_limit else False, True if y - 1 >= 0 else False)
        if self.__facing_direction == 'e':
            result = (True if x + 1 < self.__size_limit else False, True if x - 1 >= 0 else False)
        if self.__facing_direction == 's':
            result = (True if y - 1 >= 0 else False, True if y + 1 < self.__size_limit else False)
        if self.__facing_direction == 'w':
            result = (True if x - 1 >= 0 else False, True if x + 1 < self.__size_limit else False)

        return result

    def make_a_move(self, movement):
        self.__cycle_action = (self.__cycle_action + 1) % 4
        if self.__gold_recovered and self.__cycle_action == 3:
            self.__wumpus_movement()
        result = True
        if movement == 'l' or movement == 'r':
            self.__rotate_direction(movement)
        else:
            result = self.__move_direction(movement)

        return result

    def __wumpus_movement(self):
        (x, y) = self.__current_position
        wumpus_list = []
        for j in range(len(self.__mapped_world)):
            for i in range(len(self.__mapped_world[j])):
                if self.__mapped_world[i][j] == 2:
                    wumpus_list.append((i, j))

        for i, j in wumpus_list:
            i_greater = abs(i-x) > abs(j-y)
            movement_made = False
            if i_greater and i < x and self.__mapped_world[i+1][j] != 1 and self.__mapped_world[i+1][j] != 2:
                self.__mapped_world[i+1][j] = 2
                movement_made = True
            elif i_greater and i > x and self.__mapped_world[i-1][j] != 1 and self.__mapped_world[i+1][j] != 2:
                self.__mapped_world[i-1][j] = 2
                movement_made = True
            elif not i_greater and j < y and self.__mapped_world[i][j+1] != 1 and self.__mapped_world[i+1][j] != 2:
                self.__mapped_world[i][j+1] = 2
                movement_made = True
            elif not i_greater and j > y and self.__mapped_world[i][j-1] != 1 and self.__mapped_world[i+1][j] != 2:
                self.__mapped_world[i][j-1] = 2
                movement_made = True

            if movement_made:
                self.__mapped_world[i][j] = 0

    # left_or_right = either 'l' or 'r'
    def __rotate_direction(self, left_or_right):
        if left_or_right == 'l':
            self.__facing_direction = self.__directions[(self.__directions.index(self.__facing_direction) - 1 + len(self.__directions)) % len(self.__directions)]
        else:
            self.__facing_direction = self.__directions[(self.__directions.index(self.__facing_direction) + 1) % len(self.__directions)]

    # forward_or_back = either 'f' or 'b'
    # returns True if movement successful, false if it failed
    def __move_direction(self, forward_or_back):
        (forwardable, backwardable) = self.__available_movement()

        result = False
        adjustments = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        if forward_or_back == 'f' and forwardable:
            result = True
            (a, b) = adjustments[self.__directions.index(self.__facing_direction)]
            (x, y) = self.__current_position
            self.__current_position = (x+a, y+b)
            self.current_sense = self.__sensory_world[x+a][y+b]
            self.__check_for_gold()
        elif forward_or_back == 'b' and backwardable:
            result = True
            (a, b) = adjustments[self.__directions.index(self.__facing_direction)]
            (x, y) = self.__current_position
            self.__current_position = (x - a, y - b)
            self.current_sense = self.__sensory_world[x - a][y - b]
            self.__check_for_gold()

        return result

    def __check_for_gold(self):
        (x, y) = self.__current_position
        if self.__mapped_world[x][y] == 3:
            self.__gold_recovered = True
            self.__mapped_world[x][y] = 0
            self.__cycle_action = 0

    def __generate_map(self, pit_list, wumpus_list, gold_list, starting_spots):
        self.__mapped_world = [[0 for x in range(self.__size_limit)] for y in range(self.__size_limit)]

        # sensory tuple = ( Windy?, Smelly?, Shiny?)
        self.__sensory_world = [[(False, False, False) for x in range(self.__size_limit)] for y in range(self.__size_limit)]

        for x, y in pit_list:
            self.__mapped_world[x][y] = 1
            (q, r, s) = self.__sensory_world[x][y]
            self.__sensory_world[x][y] = (True, r, s)

            if x-1 >= 0:
                (a, b, c) = self.__sensory_world[x-1][y]
                self.__sensory_world[x-1][y] = (True, b, c)
            if x+1 < self.__size_limit:
                (a, b, c) = self.__sensory_world[x+1][y]
                self.__sensory_world[x+1][y] = (True, b, c)
            if y-1 >= 0:
                (a, b, c) = self.__sensory_world[x][y-1]
                self.__sensory_world[x][y-1] = (True, b, c)
            if y+1 < self.__size_limit:
                (a, b, c) = self.__sensory_world[x][y+1]
                self.__sensory_world[x][y+1] = (True, b, c)

        for x, y in wumpus_list:
            self.__mapped_world[x][y] = 2
            (q, r, s) = self.__sensory_world[x][y]
            self.__sensory_world[x][y] = (q, True, s)

            if x - 1 >= 0:
                (a, b, c) = self.__sensory_world[x - 1][y]
                self.__sensory_world[x - 1][y] = (a, True, c)
            if x + 1 < self.__size_limit:
                (a, b, c) = self.__sensory_world[x + 1][y]
                self.__sensory_world[x + 1][y] = (a, True, c)
            if y - 1 >= 0:
                (a, b, c) = self.__sensory_world[x][y - 1]
                self.__sensory_world[x][y - 1] = (a, True, c)
            if y + 1 < self.__size_limit:
                (a, b, c) = self.__sensory_world[x][y + 1]
                self.__sensory_world[x][y + 1] = (a, True, c)

        for x, y in gold_list:
            self.__mapped_world[x][y] = 3
            (q, r, s) = self.__sensory_world[x][y]
            self.__sensory_world[x][y] = (q, r, True)

            if x - 1 >= 0:
                (a, b, c) = self.__sensory_world[x - 1][y]
                self.__sensory_world[x - 1][y] = (a, b, True)
            if x + 1 < self.__size_limit:
                (a, b, c) = self.__sensory_world[x + 1][y]
                self.__sensory_world[x + 1][y] = (a, b, True)
            if y - 1 >= 0:
                (a, b, c) = self.__sensory_world[x][y - 1]
                self.__sensory_world[x][y - 1] = (a, b, True)
            if y + 1 < self.__size_limit:
                (a, b, c) = self.__sensory_world[x][y + 1]
                self.__sensory_world[x][y + 1] = (a, b, True)

        self.__starting_positions = starting_spots

    def __easy_difficulty(self):
        """  0 1 2 3 4 5 6 7
        
        0    0 0 0 2 0 0 0 0
        1    0 3 0 0 0 0 1 0
        2    0 0 0 0 0 0 0 0
        3    1 2 0 0 0 0 0 0
        4    0 0 0 0 0 1 0 7
        5    7 0 0 0 0 0 0 0
        6    0 0 0 0 0 0 0 0
        7    0 0 0 0 7 0 0 1
        """
        pit_list = [(1, 6), (3, 0), (4, 5), (7, 7)]
        wumpus_list = [(0, 3), (3, 1)]
        gold_list = [(1, 1)]
        starting_spots = [(4, 7), (5, 0), (7, 4)]

        self.__generate_map(pit_list, wumpus_list, gold_list, starting_spots)

    def __medium_difficulty(self):
        """  0 1 2 3 4 5 6 7

        0    3 0 0 2 0 0 0 0
        1    1 0 0 0 0 0 1 0
        2    0 0 0 0 0 0 0 0
        3    1 2 0 1 0 0 0 0
        4    0 0 0 0 0 1 0 7
        5    1 0 0 0 0 0 0 0
        6    0 0 0 0 0 0 0 0
        7    7 0 0 0 7 0 0 1
        """
        pit_list = [(1, 0), (1, 6), (3, 0), (3, 3), (4, 5), (5, 0), (7, 7)]
        wumpus_list = [(0, 3), (3, 1)]
        gold_list = [(0, 0)]
        starting_spots = [(4, 7), (7, 0), (7, 4)]

        self.__generate_map(pit_list, wumpus_list, gold_list, starting_spots)

    def __hard_difficulty(self):
        """  0 1 2 3 4 5 6 7

        0    7 0 0 2 0 0 0 0
        1    0 0 0 0 0 0 1 0
        2    0 0 0 0 1 0 0 0
        3    1 0 0 0 2 0 0 0
        4    0 0 0 0 1 0 0 0
        5    7 0 0 1 0 0 0 0
        6    0 0 0 1 0 0 1 0
        7    0 0 0 1 0 0 0 3
        """
        pit_list = [(1, 6), (2, 4), (3, 0), (4, 4), (5, 3), (6, 3), (6, 6), (7, 3)]
        wumpus_list = [(0, 3), (3, 4)]
        gold_list = [(7, 7)]
        starting_spots = [(0, 0), (5, 0)]

        self.__generate_map(pit_list, wumpus_list, gold_list, starting_spots)

    # "O" bottomless pit
    # "W" wumpus
    # "$" pot of gold!
    # "<-- --> -^- -v-" direction of
    def map_visual(self):
        (x,y) = self.__current_position
        result = "(" + str(x) + ", " + str(y) + ") " + self.__facing_direction + "\n"
        result += self.__top_bot

        for j in range(len(self.__mapped_world)):
            result += self.__blank_row + "|"
            for i in range(len(self.__mapped_world[j])):
                block_type = self.__mapped_world[i][j]
                if self.__current_position[0] == i and self.__current_position[1] == j:
                    if self.__facing_direction == 'n':
                        result += " =^^= "
                    elif self.__facing_direction == 'e':
                        result += " ===> "
                    elif self.__facing_direction == 's':
                        result += " =vv= "
                    else:
                        result += " <=== "
                elif block_type == 0:
                    result += "      "
                elif block_type == 1:
                    result += " \__/ "
                elif block_type == 2:
                    result += self.__wumpus_face[1 if self.__gold_recovered else 0][self.__cycle_action]
                elif block_type == 3:
                    result += " $$$$ "
                result += "|"
            result += "\n"
            result += self.__blank_row + self.__top_bot

        lines = result.split("\n")
        s = len(lines)
        result = "\n\n\n"
        for i in range(s):
            result += lines[s-i-1] + "\n"
        result += "\n\n\n"

        return result

    def game_won(self):
        return self.__gold_recovered and self.__current_position == self.__original_position

    def death_check(self):
        (x, y) = self.__current_position
        result = True
        message = ""
        if self.__mapped_world[x][y] == 1:
            message = "You fell in a bottomless pit! you died..."
            result = False
        elif self.__mapped_world[x][y] == 2:
            message = "You've been eaten by the Wumpus! Oh no..."
            result = False

        return result, message


if __name__ == '__main__':
    w = World(2)
    acceptable_moves = ['f', 'b', 'l', 'r']
    system('clear')

    start_time = time.time()
    while not w.game_won() and w.death_check()[0]:
        print(w.map_visual())
        user_move = raw_input("Enter next move (f = forward, b = back, l = left turn, r = right turn) ")
        system('clear')
        if user_move in acceptable_moves:
            valid_move = w.make_a_move(user_move)

            if not valid_move:
                print("Failed to move... you hit a wall!")
        else:
            print("not a valid move!")


    if w.game_won():
        print(w.map_visual())
        print("CONGRATS!!! YOU WON THE GAME in {:.2f} seconds!!!!!!".format((time.time() - start_time)))
    else:
        _, message = w.death_check()
        print(message)