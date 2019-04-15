from enum import Enum
from random import shuffle, randrange
import os
import element


class Floor(Enum):
    Basic = 1
    Ladder = 2
    Slope = 3
    EndOfMaze = 4
    LadderUp = 4
    LadderDown = 5


class Maze:
    """ A maze is a collection of spaces arrange in a way where there is one way through them to a goal."""

    def __init__(self, x=8, y=8, z=1, view_size=10):
        self.spaces = dict()
        self.elements = dict()
        self.x = x
        self.y = y
        self.z = z
        self.view = view_size
        self.add_element_to_maze(element.Place(x, y, z, "The End", 'O'))
        self.focus = None

        self.make_maze()
        # self.draw_maze()

    def lookup_or_make_space(self, x, y, z):
        k = (x, y, z)
        if k in self.spaces.keys():
            return self.spaces[k]
        else:
            self.spaces[k] = Space(x, y, z)
            return self.spaces[k]

    def make_maze(self):
        vis = []
        for _ in range(self.z):
            vis.append([[0] * self.x + [1] for _ in range(self.y)] + [[1] * (self.x + 1)])
        vis.append(
            [[1] * self.x + [1] for _ in range(self.y)] + [[1] * (self.x + 1)]
        )

        def walk(x, y, z):
            vis[z][y][x] = 1 if vis[z][y][x] == 0 else 2

            current_space = self.lookup_or_make_space(x, y, z)
            directions = current_space.adjoining_spaces()
            shuffle(directions)
            directions = directions + current_space.up_down()
            for (xx, yy, zz) in directions:
                if vis[zz][yy][xx] > 0:  # Have we been here before?
                    continue
                new_space = self.lookup_or_make_space(xx, yy, zz)
                if xx == x and yy == y:  # we went up or down.
                    if z > zz:
                        current_space.floorType = Floor.LadderDown if current_space.floorType == Floor.Basic else Floor.Ladder
                        new_space.floorType = Floor.LadderUp if new_space.floorType == Floor.Basic else Floor.Ladder
                    else:
                        current_space.floorType = Floor.LadderUp if current_space.floorType == Floor.Basic else Floor.Ladder
                        new_space.floorType = Floor.LadderDown if new_space.floorType == Floor.Basic else Floor.Ladder
                    vis[z][y][x] = 2
                    vis[zz][yy][xx] = 2
                elif xx == x:  # Did we move North or South?
                    if y > yy:
                        # we moved North
                        current_space.wall_north = 0
                        new_space.wall_south = 0
                    else:
                        # we moved We moved South
                        current_space.wall_south = 0
                        new_space.wall_north = 0
                elif yy == y:  # Did we move East or West?
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
        print('Maze Made!')

    def update_visable_path(self, adventurer=element.Adventurer):
        """we should be able to see x number of square down the dark hall"""

    def draw_maze(self):
        """ Lets draw the map. """
        if self.focus is None:
            loc = (0, 0, 0)
        else:
            loc = self.elements[self.focus].my_location()
        lb = max(loc[0] - int(self.view / 2), 0)
        ub = max(loc[1] - int(self.view / 2), 0)
        z = loc[2]
        rb = min(lb + self.view, self.x)
        db = min(ub + self.view, self.y)

        if ub == 0:
            rows = [["+--"] * (rb-lb)]
            if rb == self.x:
                rows[0].append('+')
        else:
            rows = []
        for y in range(ub, db):
            row1 = []
            row2 = []
            for x in range(lb, rb):
                s = self.spaces[(x, y, z)]
                val = ('|' if s.wall_west else ' ') + self.draw_element(x, y, z) + (
                    ' ' if s.floorType == Floor.Basic else '#')
                row1.append(val)
                row2.append('+--' if s.wall_south else '+  ')
            if rb == self.x:
                row1.append('|')
                row2.append('+')
            rows.append(row1)
            rows.append(row2)

        self.clear_screen()
        print('||--------- Python Adventure ---------||')
        print('Level: {}'.format(loc[2] + 1))
        for row in rows:
            print(''.join(row))

    def clear_screen(self):
        """ Windows or mac, clear the screen. """
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_element(self, x, y, z):

        elms = self.get_elements_by_location(x, y, z)
        if len(elms) == 1:
            val = elms[0].display
        elif len(elms) == 0:
            val = ' '
        else:
            val = next(elm.display for elm in elms for e in element.ElementType if elm.type == e)

        return val

    def add_element_to_maze(self, new_element=element.Base()):
        self.elements[new_element.id] = new_element
        if new_element.display == '@':
            self.focus = new_element.id
        """ This will take an element and add it to the maze dictionary. """

    def get_element_by_name(self, look_for, find_one=True, element_type=9999):
        """ This should take a string, and check for a element with that name and return it. """
        lst = [n for n in self.elements.values() if
               n.name == look_for and (element_type == 9999 or element_type == n.type)]
        if find_one:
            return lst[0]
        else:
            return lst

    def get_elements_by_location(self, x, y, z):
        """ Given a xyz location, will check for an element. """
        return [e for e in self.elements.values() if e.x == x and e.y == y and e.z == z]


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
                (self.x + 1, self.y, self.z), (self.x, self.y - 1, self.z)]

    def up_down(self):
        return [(self.x, self.y, self.z + 1), (self.x, self.y, self.z - 1)]

    def valid_moves(self):
        moves = dict()
        if not self.wall_north:
            moves['n'] = (self.x, self.y - 1, self.z)
        if not self.wall_south:
            moves['s'] = (self.x, self.y + 1, self.z)
        if not self.wall_east:
            moves['e'] = (self.x + 1, self.y, self.z)
        if not self.wall_west:
            moves['w'] = (self.x - 1, self.y, self.z)
        if self.floorType == Floor.Ladder or self.floorType == Floor.LadderUp:
            moves['u'] = (self.x, self.y, self.z + 1)
        if self.floorType == Floor.Ladder or self.floorType == Floor.LadderDown:
            moves['d'] = (self.x, self.y, self.z - 1)
        return moves
