class Base:
    def __init__(self):
        self.health = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.sight = 0

    def my_location(self):
        return [self.x, self.y, self.z]
