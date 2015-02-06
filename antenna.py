import numpy as np

class Antenna:
    def __init__(self, x, y):
        self.location = np.matrix([
            [x, y]
        ])

    def rotate(self, th):
        rotation_matrix = np.matrix([
                [np.cos(th), -np.sin(th)],
                [np.sin(th), np.cos(th)]
        ])
        return self.location * rotation_matrix

    def get_phase_difference(self, th):
        new_location = self.rotate(th)
        return new_location[0,0]

