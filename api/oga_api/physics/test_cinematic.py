import unittest
import numpy as np
import oga_api.physics.cinematic as c

class TestCinematic(unittest.TestCase):
    def test_get_angles(self):
        a0 = np.array([0, 0, 0])
        a1 = np.array([1, 0, 0])
        a2 = np.array([0, 1, 0])
        r = np.array([np.round(np.pi/2, 4)])

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
        results = np.append(results, np.array([np.round(np.pi* 3/4, 4)]))
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

        #rotate pi/2
        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, np.array([-1, 0, 0])).reshape(len(p2) + 1, 3)
        results = np.append(results, [np.round(np.pi/2, 4)]); 
        av = c.calc_angular_velocities(o, p1, p2, 1)
        self.assertTrue((np.round(av, 4) == results).all())

        #rotate -pi/2
        o = np.append(o, a0).reshape(len(o) + 1, 3)
        p1 = np.append(p1, a1).reshape(len(p1) + 1, 3)
        p2 = np.append(p2, np.array([0, 1, 0])).reshape(len(p2) + 1, 3)
        results = np.append(results, [np.round(-1 * np.pi/2, 4)]); 
        av = c.calc_angular_velocities(o, p1, p2, 1)
        self.assertTrue((np.round(av, 4) == results).all())


if __name__ == '__main__':
    unittest.main()
