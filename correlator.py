import numpy as np

class Correlator:
    def __init__(self, reference, array):
        self.reference = reference
        self.array = array

    def single_direction(self, th):
        phase_at_angle = self.array.phase_at_angle(th)
        phase_difference = np.arctan2(np.sin(phase_at_angle - self.reference), np.cos(phase_at_angle - self.reference))
        return np.linalg.norm(phase_difference)

    def all_directions(self, points):
        result = {}
        for th in np.linspace(-np.pi, np.pi, points):
            result[th] = self.single_direction(th)
        return result
