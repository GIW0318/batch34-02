class FabrikChain:
    def __init__(self, lengths, base=(0.0, 0.0)):
        self.lengths = list(lengths)
        self.base = tuple(base)
        self.last_iterations = 0

    @property
    def reach(self):
        return 0.0

    def solve(self, target, tolerance=1e-3, max_iterations=10):
        return None
