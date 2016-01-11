#!/usr/bin/env python

from directionFinder_backend import antenna_array
from correlator import Correlator
from plotter import Plotter
import numpy as np
import argparse

parser = argparse.ArgumentParser(description = "Run phase ambiguity simulations")
parser.add_argument('--freq', default=250e6, type=float)
parser.add_argument('--phi_min', default=-np.pi, type=float)
parser.add_argument('--phi_max', default=np.pi, type=float)
parser.add_argument('--phi_points', default=300, type=int)
parser.add_argument('--elements', default=4, type=int)
parser.add_argument('--array_geometry_file', default=None)
parser.add_argument('--surface_plot', action='store_true')
parser.add_argument('--with_ref_element', type=bool, default=False)
parser.add_argument('--radius', type=float, default=0.5)
args = parser.parse_args()

print(args)

# wavelengths seperation between elements and reference
phi_domain = np.linspace(args.phi_min, args.phi_max, args.phi_points)
Z = np.zeros((args.phi_points, args.phi_points))

if args.array_geometry_file:
    arr = antenna_array.AntennaArray.mk_from_config(args.array_geometry_file)
else:
    if args.with_ref_element == True:
        arr = antenna_array.AntennaArray.mk_circular_with_ref(args.radius, args.elements)
    else:
        arr = antenna_array.AntennaArray.mk_circular(args.radius, args.elements)
for antenna in arr.antennas:
    print("{x}, {y}".format(x =antenna.x, y = antenna.y))

for phi_idx, phi_val in enumerate(phi_domain):
    ref = arr.each_pair_phase_difference_at_angle(phi_val, args.freq)
    corr = Correlator(ref, arr)
    response = corr.many_directions(args.phi_min, args.phi_max, args.phi_points, args.freq)
    y = response.keys()
    y.sort()
    for i_idx, i_val in enumerate(y):
        Z[phi_idx,i_idx] = response[i_val]

Plotter(phi_domain, y, Z).colourmap()
#plotter.Plotter(x_domain, y, Z).surface()
