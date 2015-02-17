#!/usr/bin/env python

import antenna_array
import correlator
import numpy as np
import matplotlib.pyplot as plt

BASELINE_LENGTH = 2.55

arr = antenna_array.AntennaArray(BASELINE_LENGTH*2*np.pi)
ref = arr.each_pair_phase_difference_at_angle(0)
corr = correlator.Correlator(ref, arr)
response = corr.many_directions(-np.pi, np.pi, 900)
x = response.keys()
x.sort()
y=[]
for i_idx, i_val in enumerate(x):
    y.append(response[i_val])

plt.plot(x,y)
plt.show()
    
