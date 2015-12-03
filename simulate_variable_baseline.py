#!/usr/bin/env python

from directionFinder_backend import antenna_array
from correlator import Correlator
from plotter import Plotter
import numpy as np
import argparse

parser = argparse.ArgumentParser(description = "Run phase ambiguity simulations")
parser.add_argument('--f_min', default=100e6, type=float)
parser.add_argument('--f_max', default=500e6, type=float)
parser.add_argument('--f_points', default=300, type=int)
parser.add_argument('--phi_min', default=-np.pi, type=float)
parser.add_argument('--phi_max', default=np.pi, type=float)
parser.add_argument('--phi_points', default=300, type=int)
parser.add_argument('--ref-angle', default=0, type=int)
parser.add_argument('--elements', default=4, type=int)
parser.add_argument('--array_geometry_file', default=None)
parser.add_argument('--surface_plot', action='store_true')
parser.add_argument('--with_ref_element', type=bool, default=False)
parser.add_argument('--radius', type=float, default=1.0)
args = parser.parse_args()

print(args)

# wavelengths seperation between elements and reference
f_domain = np.linspace(args.f_min, args.f_max, args.f_points)
Z = np.zeros((len(f_domain), args.phi_points))

if args.array_geometry_file:
    arr = antenna_array.AntennaArray.mk_from_config(args.array_geometry_file)
else:
    if args.with_ref_element == True:
        arr = antenna_array.AntennaArray.mk_circular_with_ref(args.radius, args.elements)
    else:
        arr = antenna_array.AntennaArray.mk_circular(args.radius, args.elements)

for f_idx, f_val in enumerate(f_domain):
    ref = arr.each_pair_phase_difference_at_angle(args.ref_angle, f_val)
    corr = Correlator(ref, arr)
    response = corr.many_directions(args.phi_min, args.phi_max, args.phi_points, f_val)
    y = response.keys()
    y.sort()
    for i_idx, i_val in enumerate(y):
        Z[f_idx,i_idx] = response[i_val]

Plotter(f_domain, y, Z).colourmap()
#plotter.Plotter(x_domain, y, Z).surface()
