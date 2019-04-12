from enum import Enum
from random import shuffle, randrange
import os
import element


class Floor(Enum):
    Basic = 1
    Ladder = 2
    Slope = 3
    EndOfMaze = 4


class Maze:
    """ A maze is a collection of spaces arrange in a way where there is one way through them to a goal."""

    def __init__(self, x, y, z, view_size=10):
        self.spaces = dict()
        self.x = x
        self.y = y
        self.z = z
        self.view = view_size
        self.end_of_maze = [x, y, z]
        self.vis = []
        for x in range(self.z):
            self.vis.append([[0] * self.x + [1] for _ in range(self.y)] + [[1] * (self.x + 1)])
        self.vis.append(
            [[1] * self.x + [1] for _ in range(self.y)] + [[1] * (self.x + 1)]
        )
        self.make_maze()
        self.draw_maze()

    def lookup_or_make_space(self, x, y, z):
        k = (x, y, z)
        if k in self.spaces.keys():
            return self.spaces[k]
        else:
            self.spaces[k] = Space(x, y, z)
            return self.spaces[k]

    def make_maze(self):

        def walk(x, y, z):
            self.vis[z][y][x] = 1

            current_space = self.lookup_or_make_space(x, y, z)
            directions = current_space.adjoining_spaces()
            shuffle(directions)
            for (xx, yy, zz) in directions:
                if self.vis[zz][yy][xx] > 0:  # Have we been here before?
                    continue
                new_space = self.lookup_or_make_space(xx, yy, zz)
                if xx == x and yy == y:  # we went up or down.
                    current_space.floorType = Floor.Ladder
                    new_space.floorType = Floor.Ladder
                    self.vis[z][y][x] = 2
                    self.vis[zz][yy][xx] = 2
                elif xx == x:  # Did we move North or South?
                    # hor[max(y, yy)][x] = "+  "
                    if y > yy:
                        # we moved North
                        current_space.wall_north = 0
                        new_space.wall_south = 0
                    else:
                        # we moved We moved South
                        current_space.wall_south = 0
                        new_space.wall_north = 0
                elif yy == y:  # Did we move East or West?
                    # ver[y][max(x, xx)] = "   "
                    if x > xx:
                        # we moved West
                        current_space.wall_west = 0
                        new_space.wall_east = 0
                    else:
                        current_space.wall_east = 0
                        new_space.wall_west = 0

                self.spaces[new_space.id] = new_space
                walk(xx, yy, zz)
            self.spaces[current_space.id] = current_space

        walk(randrange(self.x), randrange(self.z), randrange(self.z))

    def update_visable_path(self, adventurer=element.Adventurer):
        """we should be able to see x number of square down the dark hall"""

    def draw_maze(self, adventurer=element.Adventurer()):
        """ given an adventurer, lets draw the map around them. """
        # TODO: Make a function to draw the map.
        loc = adventurer.my_location()
        lb = max(loc[0] - self.view / 2, 0)
        ub = max(loc[1] - self.view / 2, 0)
        z = loc[2]
        rb = min(lb + self.view, self.x)
        db = min(ub + self.view, self.y)

        for x in range(lb, rb):
            for y in range(ub, db):
                s = self.spaces[(x, y, z)]

        self.clear_screen()
        print('||--------- Python Adventure ---------||')

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')


class Space:
    """ A space is an object that has four walls and a floor. In addition you can track if a space has been visited."""

    def __init__(self, x, y, z=1):
        self.floorType = Floor.Basic  # maybe have slopes or ladders some time.
        self.visible = 0
        self.wall_north = 1
        self.wall_east = 1
        self.wall_south = 1
        self.wall_west = 1
        self.x = x
        self.y = y
        self.z = z
        self.id = (x, y, z)

    def adjoining_spaces(self):
        return [(self.x - 1, self.y, self.z), (self.x, self.y + 1, self.z),
                (self.x + 1, self.y, self.z), (self.x, self.y - 1, self.z),
                (self.x, self.y, self.z + 1), (self.x, self.y, self.z - 1)]
