import numpy as np

class Correlator:
    """A correlator is probably a poor name.
    It's more like a distance calculator between two n-dimensional points"""
    def __init__(self, reference, array):
        self.reference = reference
        self.array = array

    def single_direction(self, th):
        """Returns the distance between the reference point and the point
        created by rotating the array by theta degrees"""
        phases_at_angle = self.array.phases_at_angle(th)
        phase_differences = np.arctan2(np.sin(phases_at_angle - self.reference), np.cos(phases_at_angle - self.reference))
        distance = 0
        for phase_difference in phase_differences:
            distance += phase_difference**2
        return np.linalg.norm(phase_differences)

    def all_directions(self, points):
        result = {}
        for th in np.linspace(-np.pi, np.pi, points):
            result[th] = self.single_direction(th)
        return result
