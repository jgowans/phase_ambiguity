import numpy as np
from antenna import Antenna

class Array:
    def __init__(self, d):
        self.antennas = []
        self.antennas.append(Antenna(d, 0))
        self.antennas.append(Antenna(-np.sqrt(d*d/2), +np.sqrt(d*d/2)))
        self.antennas.append(Antenna(-np.sqrt(d*d/2), -np.sqrt(d*d/2)))

    def phase_at_angle(self, th):
        phase_of_elements = np.array([])
        for antenna in self:
            phase_of_elements = np.append(phase_of_elements, antenna.phase_at_angle(th))
        return phase_of_elements

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.antennas):
            raise StopIteration
        self.current += 1
        return self.antennas[self.current - 1]

