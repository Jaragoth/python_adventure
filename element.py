from enum import Enum
import game_map


class ElementType(Enum):
    adventurer = 1
    item = 2
    place = 3
    monster = 4


class Base:
    def __init__(self, name='', x=0, y=0, z=0, value=0, active=0, base_type=ElementType.item, display='`'):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.value = value
        self.active = active
        self.type = base_type
        self.display = display
        self.id = id(self)

    def my_location(self):
        return self.x, self.y, self.z

    def move(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Living(Base):
    def __init__(self):
        Base.__init__(self)
        self.health = 0
        self.maxHealth = 0
        self.sight = 0
        self.speed = 0

    def my_moves(self, the_map):
        return the_map.lookup_or_make_space(self.x, self.y, self.z).valid_moves()


class Place(Base):
    def __init__(self, x=0, y=0, z=0, name='', display=' '):
        Base.__init__(self, x=x, y=y, z=z, name=name, display=display)
        self.type = ElementType.place


class Adventurer(Living):
    def __init__(self, health=10, sight=6, name='Michael', x=0, y=0, z=0, speed=4, active=1):
        Living.__init__(self)
        self.inventory = dict()
        self.type = ElementType.adventurer
        self.health = health
        self.sight = sight
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.speed = speed
        self.active = active
        self.display = '@'

