from enum import Enum


class ElementType(Enum):
    item = 1
    adventurer = 2
    friend = 3
    monster = 4


class Base:
    def __init__(self):
        self.name = ''
        self.x = 0
        self.y = 0
        self.z = 0
        self.value = 0
        self.active = 0
        self.type = ElementType.item

    def my_location(self):
        return self.x, self.y, self.z


class Living(Base):
    def __init__(self):
        Base.__init__(self)
        self.health = 0
        self.maxHealth = 0
        self.sight = 0
        self.speed = 0


class Adventurer(Living):
    def __init__(self, health=10, sight=6, name='Michael', x=0, y=0, z=0, speed=4):
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

