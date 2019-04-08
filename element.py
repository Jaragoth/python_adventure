from enum import Enum


class ElementType(Enum):
    item = 1
    adventurer = 2
    friend = 3
    monster = 4


class Base:
    def __init__(self):
        self.health = 0
        self.maxHealth = 0
        self.name = ''
        self.x = 0
        self.y = 0
        self.z = 0
        self.value = 0
        self.type = ElementType.item

    def my_location(self):
        return (self.x, self.y, self.z)

class Living(Base):
    def __init__(self):
        super().__init__()
        self.sight = 0
        self.speed = 0
