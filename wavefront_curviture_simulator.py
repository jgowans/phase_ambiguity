#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants

def get_phase_difference(r0, r1, freq_hz):
    wavelength = scipy.constants.c / freq_hz
    phase_0 = 2*np.pi * r0 / wavelength
    phase_1 = 2*np.pi * r1 / wavelength
    return phase_1 - phase_0

def simulate():
    freq = 250e6
    points = 300
    x = np.ndarray((points), dtype=np.float64)
    y = np.ndarray((points), dtype=np.float64)
    for idx, r in enumerate(np.linspace(5, 50, 300)):
        r0 = r
        r1 = np.sqrt(0.6**2 + r**2)
        x[idx] = r
        y[idx] = get_phase_difference(r0, r1, freq)
    percentage = 100 * y / np.pi 
    fig, ax0 = plt.subplots()
    ax0.plot(x, percentage, linewidth = 2)
    ax0.set_ylabel("Phase error (percentage)")
    ax0.axhline(y = 1, color='r')
    ax0.axhline(y = 2, color='orange')
    fig.gca().set_title("Curved wavefront error for a 0.6 m 2-element array")
    fig.gca().set_xlabel("Tx to Rx distance (meters)")
    ax1 = ax0.twinx()
    ax1.plot(x, y)
    ax1.set_ylabel("Phase error (radians)")
    ax1.set_ylim(
        bottom = np.pi * ax0.get_ylim()[0] / 100,
        top = np.pi * ax0.get_ylim()[1] / 100
    )
    plt.show()

if __name__ == '__main__':
    simulate()
