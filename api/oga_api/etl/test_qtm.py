import unittest
import oga_api.etl.qtm as qtm
class TestQTM(unittest.TestCase):

    def test_frame_walk1(self):
        self.content = qtm.readQTMFile('oga_api/etl/Walk1.mat')
        self.assertEqual(self.content['frame_rate'], 315.0)
        self.assertEqual(self.content['trajectories'].shape, (88, 4, 1491))
        self.assertEqual(self.content['frames'], 1491)
        self.assertEqual(self.content['number_markers'], 88)

    def test_frame_walk1(self):
        self.content = qtm.readQTMFile('oga_api/etl/Walk2.mat')
        self.assertEqual(self.content['frame_rate'], 315.0)
        self.assertEqual(self.content['trajectories'].shape, (49, 4, 1321))
        self.assertEqual(self.content['frames'], 1321)
        self.assertEqual(self.content['number_markers'], 49)
