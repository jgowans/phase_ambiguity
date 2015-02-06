#!/usr/bin/env python

import antenna_array
import correlator
import numpy as np
import matplotlib.pyplot as plt
arr = antenna_array.Array(3*np.pi)
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





