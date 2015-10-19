import unittest
import numpy as np
import oga_api.physics.cinematic as c

class TestCinematic(unittest.TestCase):
    def test_get_angles(self):
        a0 = np.array([0, 0, 0])
        a1 = np.array([1, 0, 0])
        a2 = np.array([0, 1, 0])
        r = np.array([np.round(90, 4)])

        o = a0.reshape(1, 3)
        p1 = a1.reshape(1, 3)
        p2 = a2.reshape(1, 3)
        results = r
        angles = c.get_angles(o, p1, p2)
        self.assertTrue((np.round(angles, 4) ==results).all())

        o = np.append(o, a0 + 3).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1 + 3).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, a2 + 3).reshape(len(p2) + 1, 3)
        results = np.append(results, r)
        angles = c.get_angles(o, p1, p2)
        self.assertTrue((np.round(angles, 4) ==results).all())

        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, np.array([-1, 1, 0])).reshape(len(p2) + 1, 3)
        results = np.append(results, np.array([np.round(45, 4)]))
        angles = c.get_angles(o, p1, p2)
        self.assertTrue((np.round(angles, 4) ==results).all())

        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, np.array([0,0,1])).reshape(len(p2) + 1, 3)
        results = np.append(results, r)
        angles = c.get_angles(o, p1, p2)
        self.assertTrue((np.round(angles, 4) ==results).all())

        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, np.array([0,0,-1])).reshape(len(p2) + 1, 3)
        results = np.append(results, r)
        angles = c.get_angles(o, p1, p2)
        self.assertTrue((np.round(angles, 4) ==results).all())


    def test_calc_angular_velocities(self):
        a0 = np.array([0, 0, 0])
        a1 = np.array([1, 0, 0])
        a2 = np.array([0, 1, 0])
        r = np.array([0], float)

        o = a0.reshape(1, 3)
        p1 = a1.reshape(1, 3)
        p2 = a2.reshape(1, 3)

	

        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, a2).reshape(len(p2) + 1, 3)
        results = r
        av = c.calc_angular_velocities(o, p1, p2, 1)
        self.assertTrue((np.round(av, 4) ==results).all())

        #rotate -90 degrees
        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, np.array([-1, 0, 0])).reshape(len(p2) + 1, 3)
        results = np.append(results, [np.round(-90, 4)]); 
        av = c.calc_angular_velocities(o, p1, p2, 1)
	#import pdb; pdb.set_trace()
        self.assertTrue((np.round(av, 4) == results).all())

        #rotate 90
        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, np.array([0, 1, 0])).reshape(len(p2) + 1, 3)
        results = np.append(results, [np.round(90, 4)]); 
        av = c.calc_angular_velocities(o, p1, p2, 1)
        self.assertTrue((np.round(av, 4) == results).all())
	
    def test_calc_angular_accelerations(self):
	v = np.array([0, 1, 3])
	aa = c.calc_angular_accelerations(v, 1)
	self.assertEqual(aa[0], 1)
	self.assertEqual(aa[1], 2)


    def test_get_vetorial_velocities(self):
        vec_1 = np.array([0, 1, 2, 3])
        time = 1
        vect_v = c.get_vectorial_velocities(vec_1, time)
        self.assertTrue((vect_v == np.array([1, 1, 1])).all())

    def test_get_vetorial_velocities_half_time(self):
        vec_1 = np.array([0, 1, 2, 3])
        time = 0.5 
        vect_v = c.get_vectorial_velocities(vec_1, time)
        self.assertTrue((vect_v == np.array([2, 2, 2])).all())

    def test_get_vetorial_velocities_with_acceleration(self):
        vec_1 = np.array([0, 1, 3, 6.55])
        time = 0.5 
        vect_v = c.get_vectorial_velocities(vec_1, time)
        self.assertTrue((vect_v == np.array([2, 4, 7.1])).all())

    def test_get_3d_velocities(self):
        vec_x = np.array([1, 2, 3])
        vec_y = np.array([1, 3, 5])
        vec_z = np.array([1, 4, 7])
        v_x, v_y, v_z = c.get_3d_velocities(vec_x, vec_y, vec_z, 1)
        self.assertTrue((v_x == np.array([1, 1])).all())
        self.assertTrue((v_y == np.array([2, 2])).all())
        self.assertTrue((v_z == np.array([3, 3])).all())

if __name__ == '__main__':
    unittest.main()
