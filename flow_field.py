class FlowField:
    def __init__(self, width, height, blocked=None, costs=None):
        self.width = width
        self.height = height
        self.blocked = set(blocked or ())
        self.costs = dict(costs or {})
        self.goal = None

    def set_goal(self, goal):
        return None

    def compute(self):
        return None

    def distance(self, x, y):
        return None

    def direction(self, x, y):
        return None

    def path(self, start):
        return None
