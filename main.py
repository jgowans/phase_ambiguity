#!/usr/bin/env python

import antenna_array
import correlator
import plotter
import numpy as np

POINTS = 200

x_domain = np.linspace(0.2, 7, 300)
Z = np.zeros((len(x_domain), POINTS))

for x_idx, x_val in enumerate(x_domain):
    arr = antenna_array.Array(x_val*np.pi)
    ref = arr.each_pair_phase_difference_at_angle(0)
    corr = correlator.Correlator(ref, arr)
    response = corr.many_directions(-np.pi, np.pi, POINTS)
    y = response.keys()
    y.sort()
    for i_idx, i_val in enumerate(y):
        Z[x_idx,i_idx] = response[i_val]

plotter.Plotter(x_domain, y, Z).colourmap()
#plotter.Plotter(x_domain, y, Z).surface()
