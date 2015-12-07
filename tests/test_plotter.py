#!/usr/bin/env python

import unittest
import numpy as np
import sys
sys.path.append('..')
import plotter

class PlotterTester(unittest.TestCase):
    def setUp(self):
        x = np.arange(-5, 5, 0.2)
        y = np.arange(-3, 3, 0.2)
        Z = np.zeros((len(x),len(y)))
        for idx_x, val_x in enumerate(x):
            for idx_y, val_y in enumerate(y):
                Z[idx_x,idx_y] = val_x**2 + val_y**2
        self.plotter = plotter.Plotter(x,y,Z)

    def test_surface(self):
        self.plotter.surface()

    def test_colourmap(self):
        self.plotter.colourmap()

if __name__ == '__main__':
    unittest.main()
