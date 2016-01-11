#!/usr/bin/env python

from directionFinder_backend.antenna_array import AntennaArray
from directionFinder_backend.direction_finder import DirectionFinder
import numpy as np
from colorlog import ColoredFormatter
import matplotlib.pyplot as plt
import logging
import argparse

if __name__ == '__main__':
    # setup root logger. Shouldn't be used much but will catch unexpected messages
    colored_formatter = ColoredFormatter("%(log_color)s%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(colored_formatter)
    handler.setLevel(logging.DEBUG)

    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.INFO)

    logger = logging.getLogger('main')
    logger.propagate = False
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description = "Run RMS error simulations")
    parser.add_argument('--freq', default=250e6, type=float)
    parser.add_argument('--phi_min', default=-np.pi, type=float)
    parser.add_argument('--phi_max', default=np.pi, type=float)
    parser.add_argument('--phi_points', default=1000, type=int)
    parser.add_argument('--elements', default=4, type=int)
    parser.add_argument('--array_geometry_file', default=None)
    parser.add_argument('--with_ref_element', type=bool, default=False)
    parser.add_argument('--radius', type=float, default=0.5)
    parser.add_argument('--rmserr', type=float, default=0.1)
    args = parser.parse_args()

    phi_domain = np.linspace(args.phi_min, args.phi_max, args.phi_points)

    if args.array_geometry_file:
        arr = AntennaArray.mk_from_config(args.array_geometry_file)
    else:
        if args.with_ref_element == True:
            arr = AntennaArray.mk_circular_with_ref(args.radius, args.elements)
        else:
            arr = AntennaArray.mk_circular(args.radius, args.elements)

    df = DirectionFinder(None, arr, args.freq, logger.getChild('df'))
    
    x = []
    y = []


    df_errors = []
    for phi in phi_domain:
        array_response = arr.each_pair_phase_difference_at_angle(phi, args.freq)
        visibility_errors = np.random.normal(0, args.rmserr, array_response.shape)
        array_response += visibility_errors
        angle_out = df.find_closest_point(array_response)
        angular_error = np.arctan2(
            np.sin(phi - angle_out),
            np.cos(phi - angle_out)
        )
        df_errors.append(angular_error)
        x.append(phi)
        y.append(angle_out)

    rmserror = np.sqrt(np.sum(np.square(df_errors)) / len(df_errors))
    print("Angular RMS error: {}".format(rmserror))
    #y = np.unwrap(y)
    plt.plot(x,y, linestyle='', marker='.')
    plt.show()
