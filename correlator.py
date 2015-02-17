import numpy as np

class Correlator:
    """A correlator is probably a poor name.
    It's more like a distance calculator between two n-dimensional points"""
    def __init__(self, reference, array):
        self.reference = reference
        self.array = array

    def single_direction(self, phi):
        """Returns the distance between the reference point and the point
        created by rotating the array by phi degrees"""
        phases_at_angle = self.array.each_pair_phase_difference_at_angle(phi)
        phase_differences = np.arctan2(np.sin(phases_at_angle - self.reference), np.cos(phases_at_angle - self.reference))
        # phase_differences in an n-dimensional vector of the phase differences between
        # the reference vector and the rotated vector. We want the length of 'phase_differences'
        # to know how far away these vector are from each other.
        return np.linalg.norm(phase_differences)

    def all_directions(self, points):
        result = {}
        for phi in np.linspace(-np.pi, np.pi, points):
            result[phi] = self.single_direction(phi)
        return result
