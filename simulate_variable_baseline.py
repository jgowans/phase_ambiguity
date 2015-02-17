#!/usr/bin/env python

import antenna_array
import correlator
import plotter
import numpy as np
import argparse

parser = argparse.ArgumentParser(description = "Run phase ambiguity simulations")
parser.add_argument('--d_min', default=0.2, type=float)
parser.add_argument('--d_max', default=7, type=float)
parser.add_argument('--d_points', default=300, type=int)
parser.add_argument('--phi_min', default=-np.pi, type=float)
parser.add_argument('--phi_max', default=np.pi, type=float)
parser.add_argument('--phi_points', default=300, type=int)
parser.add_argument('--ref-angle', default=0, type=int)
parser.add_argument('--surface_plot', action='store_true')
args = parser.parse_args()

print(args)

# wavelengths seperation between elements and reference
x_domain = np.linspace(args.d_min, args.d_max, args.d_points)
Z = np.zeros((len(x_domain), args.phi_points))

for x_idx, x_val in enumerate(x_domain):
    arr = antenna_array.AntennaArray(x_val*np.pi)
    ref = arr.each_pair_phase_difference_at_angle(args.ref_angle)
    corr = correlator.Correlator(ref, arr)
    response = corr.many_directions(args.phi_min, args.phi_max, args.phi_points)
    y = response.keys()
    y.sort()
    for i_idx, i_val in enumerate(y):
        Z[x_idx,i_idx] = response[i_val]

plotter.Plotter(x_domain, y, Z).colourmap()
#plotter.Plotter(x_domain, y, Z).surface()
