from enum import Enum
from random import shuffle, randrange


class Floor(Enum):
    Basic = 1
    Ladder = 2
    Slope = 3


class Maze:
    """ A maze is a collection of spaces arrange in a way where there is one way through them to a goal."""

    def __init__(self, x, y, z):
        self.spaces = dict()
        self.x = x
        self.y = y
        self.z = z
        self.end_of_maze = [x, y, z]
        self.vis = [
                       [[0] * self.x + [2] for _ in range(self.y)] + [[2] * (self.x + 1)]
                   ] * self.z + [
                       [2] * self.x + [2] for _ in range(self.y)
                   ] + [[2] * (self.x + 1)]
        self.make_maze()

    def lookup_or_make_space(self, x, y, z):
        k = (x, y, z)
        if k in self.spaces.keys():
            return self.spaces[k]
        else:
            self.spaces[k] = Space(x, y, z)
            return self.spaces[k]

    def make_maze(self):

        def walk(x, y, z):
            self.vis[x][y][z] = 1

            cs = self.lookup_or_make_space(x, y, z)
            d = cs.adjoining_spaces()
            shuffle(d)
            for (xx, yy, zz) in d:
                if self.vis[xx][yy][zz]:  # Have we been hear before?
                    continue
                ns = self.lookup_or_make_space(xx, yy, zz)
                if xx == x:  # Did we move North or South?
                    # hor[max(y, yy)][x] = "+  "
                    if y > yy:
                        # we moved North
                        cs.north = 0
                        ns.south = 0
                    else:
                        # we moved We moved South
                        cs.south = 0
                        ns.north = 0
                elif yy == y:  # Did we move East or West?
                    # ver[y][max(x, xx)] = "   "
                    if x > xx:
                        # we moved West
                        cs.west = 0
                        ns.east = 0
                    else:
                        cs.east = 0
                        ns.west = 0
                elif xx == x and yy == y:  # we went up or down.
                    cs.floorType = Floor.Ladder
                    ns.floorType = Floor.Ladder
                self.spaces[ns.name] = ns
                walk(xx, yy, zz)
            self.spaces[cs.name] = cs

        walk(randrange(self.x), randrange(self.z), randrange(self.z))

    def update_visable_path(self, adventurer):
        """we should be able to see x number of square down the dark hall"""

    def draw_maze(self, adventurer):
        """ given an adventurer, lets draw the map around them. """
        # TODO: Make a function to draw the map.

        pass


class Space:
    """ A space is an object that has four walls and a floor. In addition you can track if a space has been visited."""

    def __init__(self, x, y, z=1):
        self.floorType = Floor.Basic  # maybe have slopes or ladders some time.
        self.visible = 0
        self.north = 1
        self.east = 1
        self.south = 1
        self.west = 1
        self.x = x
        self.y = y
        self.z = z
        self.id = (x, y, z)

    def adjoining_spaces(self):
        return [([self.x - 1, self.y, self.z]), ([self.x, self.y + 1, self.z]),
                ([self.x + 1, self.y, self.z]), ([self.x, self.y - 1, self.z]),
                ([self.x, self.y, self.z + 1]), ([self.x, self.y, self.z - 1])]
