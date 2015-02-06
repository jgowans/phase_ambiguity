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

    def phase_at_angle(self, th):
        new_location = self.rotate(th)
        phase = new_location[0,0]
        # force phase to range from -pi to pi
        normalised_phase = np.arctan2(np.sin(phase), np.cos(phase))
        return normalised_phase

