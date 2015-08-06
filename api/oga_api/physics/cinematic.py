import numpy as np

def calc_angular_velocities(origins, components_a, components_b, time):
    angles = get_angles(origins, components_a, components_b)
    final = angles[1: len(angles)]
    initial = angles[0: len(angles) -1]
    return (final - initial) / time

def get_angles(origins, components_a, components_b):
    trans_a = components_a - origins
    trans_b = components_b - origins
    angles = np.arccos(np.sum(trans_a * trans_b, axis = 1)/(np.sqrt(np.sum(trans_a ** 2, axis = 1)) * np.sqrt(np.sum(trans_b ** 2, axis = 1))))
    return angles
