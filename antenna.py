import numpy as np

class Antenna:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = np.array([
            [x],
            [y]
        ])

    def rotated(self, phi):
        rotation_matrix = np.array([
                [np.cos(phi), -np.sin(phi)],
                [np.sin(phi), np.cos(phi)]
        ])
        new_location = rotation_matrix.dot(self.location)
        return Antenna(new_location[0,0], new_location[1,0])

    def rotated_distance(phi):
        return self.rotated(phi).x

    def phase_at_angle(self, phi):
        new_phase = self.rotated(phi).x
        # force phase to range from -pi to pi. I sort of know how phiis works...
        normalised_phase = np.arctan2(np.sin(new_phase), np.cos(new_phase))
        return normalised_phase


