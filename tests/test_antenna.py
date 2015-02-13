#!/usr/bin/env python

import unittest
import numpy as np
import sys
sys.path.append('..')
import antenna

class AntennaTester(unittest.TestCase):
    def setUp(self):
        self.antenna = antenna.Antenna(12.34, 23.45) # some nasty number of wavelengths

    def test_coordinates(self):
        self.assertAlmostEqual(self.antenna.x, 12.34)
        self.assertAlmostEqual(self.antenna.y, 23.45)

    def test_rotated_pi(self):
        rotated = self.antenna.rotated(np.pi)
        self.assertAlmostEqual(rotated.x, -12.34)
        self.assertAlmostEqual(rotated.y, -23.45)

    def test_rotated_3_2_pi(self):
        rotated = self.antenna.rotated(3*np.pi/2)
        self.assertAlmostEqual(rotated.x, 23.45)
        self.assertAlmostEqual(rotated.y, -12.34)

if __name__ == '__main__':
    unittest.main()
