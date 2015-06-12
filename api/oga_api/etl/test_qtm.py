import unittest
import oga_api.etl.qtm as qtm
class TestQTM(unittest.TestCase):

    def setUp(self):
        self.content = qtm.readQTMFile('oga_api/etl/Walk1.mat')

    def test_frame_rate(self):
        self.assertEqual(self.content['frame_rate'], 315.0)

    def test_trajectories_shape(self):
        self.assertEqual(self.content['trajectories'].shape, (88, 4, 1491))

    def test_frames(self):
        self.assertEqual(self.content['frames'], 1491)

    def test_number_markers(self):
        self.assertEqual(self.content['number_markers'], 88)
