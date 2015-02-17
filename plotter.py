import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D

class DimensionMismatch(Exception):
    pass

class Plotter:
    def __init__(self, x_domain, y_domain, z_grid):
        if z_grid.shape[0] != len(x_domain):
            raise DimensionMismatch("Z's 1st dimension is not equal to x's length")
        if z_grid.shape[1] != len(y_domain):
            raise DimensionMismatch("Z's 2nd dimension is not equal to y's length")
        self.X, self.Y = np.meshgrid(x_domain, y_domain, indexing="ij")
        self.Z = z_grid

    def surface(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        surface = ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1)
        plt.show()

    def colourmap(self):
#        plt.pcolormesh(self.X, self.Y, self.Z, norm=matplotlib.colors.LogNorm())
        plt.pcolormesh(self.X, self.Y, self.Z)
        plt.colorbar()
        plt.show()


