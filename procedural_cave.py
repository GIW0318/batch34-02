class CaveMap:
    def __init__(self, width, height, seed=0, fill=0.45):
        self.width = width
        self.height = height
        self.seed = seed
        self.fill = fill

    @classmethod
    def from_rows(cls, rows):
        return None

    def generate(self, steps=4, birth=5, death=4):
        return None

    def connected(self):
        return None

    def components(self):
        return None

    def repair(self):
        return None

    def state(self):
        return {}
