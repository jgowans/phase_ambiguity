import numpy as np
from antenna import Antenna
import itertools

class Array:
    def __init__(self, d):
        self.antennas = []
        self.antennas.append(Antenna(0, 0))
        self.antennas.append(Antenna(d, 0))
        self.antennas.append(Antenna(-np.sqrt(d*d/2), +np.sqrt(d*d/2)))
        self.antennas.append(Antenna(-np.sqrt(d*d/2), -np.sqrt(d*d/2)))

    def phases_at_angle(self, th):
        phases_of_elements = np.array([])
        for antenna in self:
            phases_of_elements = np.append(phases_of_elements, antenna.phase_at_angle(th))
        return phases_of_elements

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.antennas):
            raise StopIteration
        self.current += 1
        return self.antennas[self.current - 1]

    def each_pair(self):
        pairs = itertools.combinations(self.antennas, 2)
        for pair in pairs:
            yield pair

    def each_pair_phase_difference_at_angle(self, phi):
        for pair in self.each_pair():
            phase_difference_between_two_antennas(pair[0], pair[1])

    def phase_difference_between_two_antennas_at_angle(antA, antB, phi):
        """Implements antB.phase - antA.phase"""
        antA_distance = antA.rotated(phi).x
        antB_distance = antB.rotated(phi).x
        delta_x = antB_distance - antB_distance
        # force phase to range from -pi to pi. I sort of know how phiis works...
        normalised_phase = np.arctan2(np.sin(delta_x), np.cos(delta_x))

