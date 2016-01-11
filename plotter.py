import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LogNorm
from matplotlib.colors import PowerNorm

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
        fig, ax = plt.subplots()
        #mesh = plt.pcolormesh(self.X, self.Y, self.Z, linewidth=0,rasterized=True, vmin=0, vmax=4, axes=ax)
        mesh = plt.pcolormesh(self.X, self.Y, self.Z, linewidth=0,rasterized=True, axes=ax)
        bar = plt.colorbar()
        #bar.set_label("Difference (RMS radians)")
        #ax.set_title("Ambiguity for N antenna circular array with R m radius")
        #ax.set_xlabel("Frequency (MHz)")
        #ax.set_ylabel("Comparison angle (radians)")
        #ax.set_ylim(top=3.2, bottom=-3.2)
        #ax.set_xlim(left=30)
        plt.show()


