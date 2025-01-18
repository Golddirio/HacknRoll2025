import numpy as np

class Pair():
    def __init__(self, index: int, xs: np.ndarray):
        self.index = index
        self.xs = xs
        
    def __str__(self):
        return f"[{self.index}, {self.xs}]"