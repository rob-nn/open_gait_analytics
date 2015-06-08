import unittest
import requests

class TestRest(unittest.TestCase):
    def setUp(self):
	db.patients.drop()

    def tearDown(self): 
        db.patients.drop()

    def test_check_connection(self):
	db.patients.insert({'name': 'testing'})
	obj = db.patients.find_on({'name': 'testing'})
	self.assertTrue(obj.name == 'testing')
