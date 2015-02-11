#!/usr/bin/env python

import antenna_array
import correlator
import numpy as np
import matplotlib.pyplot as plt

distances = np.linspace(0.5*np.pi, 5*np.pi, 30)

for d in distances:
    arr = antenna_array.Array(d)
    ref = arr.phase_at_angle(0)
    corr = correlator.Correlator(ref, arr)

response = corr.all_directions(500)

x = response.keys()
x.sort()
y = []
for i in x:
    y.append(response[i])

plt.plot(x,y)
plt.show(block=True)





