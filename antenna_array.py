import numpy as np
from antenna import Antenna
import itertools

class AntennaArray:
    def __init__(self, d):
        self.antennas = []
        # "Circular" around a reference element
        self.antennas.append(Antenna(0, 0))
        self.antennas.append(Antenna(d, 0))
#        self.antennas.append(Antenna(0, d))
#        self.antennas.append(Antenna(-d, 0))
#        self.antennas.append(Antenna(0, -d))
        self.antennas.append(Antenna(-np.sqrt(d**2/2), +np.sqrt(d**2/2)))
        self.antennas.append(Antenna(-np.sqrt(d**2/2), -np.sqrt(d**2/2)))
#        self.antennas.append(Antenna(np.sqrt(d**2/2), np.sqrt(d**2/2)))
#        self.antennas.append(Antenna(np.sqrt(d**2/2), -np.sqrt(d**2/2)))

    def phases_at_angle(self, phi):
        phases_of_elements = np.array([])
        for antenna in self:
            phases_of_elements = np.append(phases_of_elements, antenna.phase_at_angle(phi))
        return phases_of_elements

    def __iter__(self):
        self.current = 0
        return self

    def __len__(self):
        return len(self.antennas)

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
        phases_of_pairs = np.array([])
        for ant0, ant1 in self.each_pair():
            phases_of_pairs = np.append(
                phases_of_pairs,
                self.phase_difference_between_two_antennas_at_angle(
                    ant0, 
                    ant1, 
                    phi
                )
            )
        return phases_of_pairs

    def phase_difference_between_two_antennas_at_angle(self, antA, antB, phi):
        """Implements antB.phase - antA.phase"""
        antA_distance = antA.rotated(phi).x
        antB_distance = antB.rotated(phi).x
        delta_x = antB_distance - antA_distance
        # force phase to range from -pi to pi. I sort of know how phiis works...
        normalised_phase = np.arctan2(np.sin(delta_x), np.cos(delta_x))
        return normalised_phase

