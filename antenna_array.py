from antenna import Antenna

class Array:
    def __init__(self, d):
        self.antennas = []
        self.antennas.append(Antenna(d, 0))
        self.antennas.append(Antenna(0, d))
        self.antennas.append(Antenna(d, d))

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.antennas):
            raise StopIteration
        self.current += 1
        return self.antennas[self.current - 1]

