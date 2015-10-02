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

    return (np.pi -  angles) * (180/np.pi)

def get_vectorial_velocities(vector, time):
        final_position = vector[1: len(vector)]
        initial_position = vector[0: len(vector) - 1]
        return (final_position - initial_position) / time

def get_3d_velocities(vector_x, vector_y, vector_z, time):
        return (get_vectorial_velocities(vector_x, time), get_vectorial_velocities(vector_y, time), get_vectorial_velocities(vector_z, time))
