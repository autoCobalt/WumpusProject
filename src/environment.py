import random

class World:
    # 0 = safe spot
    # 1 = bottomless pit
    # 2 = wumpus creature
    # 3 = pot of gold
    # 7 = starting square

    #initial difficulty will be from 1 to 3
    def __init__(self, difficulty):
        self.__size_limit = 8
        self.__directions = ['n', 'e', 's', 'w']
        self.__current_position = ()
        self.current_sense = ()
        self.__facing_direction = None


        if difficulty == 1:
            self.__easy_difficulty()
        elif difficulty == 2:
            self.__medium_difficulty()
        else:
            self.__hard_difficulty()


        self.__tornado_landing()


    def __tornado_landing(self):
        self.__current_position = random.choice(self.__starting_positions)
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

    # left_or_right = either 'l' or 'r'
    def rotate_direction(self, left_or_right):
        if left_or_right == 'l':
            self.__facing_direction = self.__directions[(self.__directions.index(self.__facing_direction) - 1 + len(self.__directions)) % len(self.__directions)]
        else:
            self.__facing_direction = self.__directions[(self.__directions.index(self.__facing_direction) + 1) % len(self.__directions)]

    # forward_or_back = either 'f' or 'b'
    # returns True if movement successful, false if it failed
    def move_direction(self, forward_or_back):
        (forwardable, backwardable) = self.__available_movement()

        result = False
        adjustments = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        if forward_or_back == 'f' and forwardable:
            result = True
            (a, b) = adjustments[self.__directions.index(self.__facing_direction)]
            (x, y) = self.__current_position
            self.__current_position = (x+a, y+b)
            self.current_sense = self.__sensory_world[x+a][y+b]
        elif forward_or_back == 'b' and backwardable:
            result = True
            (a, b) = adjustments[self.__directions.index(self.__facing_direction)]
            (x, y) = self.__current_position
            self.__current_position = (x - a, y - b)
            self.current_sense = self.__sensory_world[x - a][y - b]

        return result


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


if __name__ == '__main__':
    w = World(1)

    for v in w.mapped_world:
        print(v)

