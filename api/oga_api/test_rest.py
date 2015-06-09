import unittest
import requests
from . import get_db_connection
from bson import json_util

base_url = 'http://localhost:5000/api/v0.0'

class TestRest(unittest.TestCase):
    db = None
    def setUp(self):
        self.db = get_db_connection('testing')
        self.db.patients.drop()

    def tearDown(self): 
        if self.db:
            self.db.patients.drop()

    def test_check_connection(self):
	obj = self.db['patients'].insert_one({'name': 'testing'})
	obj = self.db.patients.find_one({'name': 'testing'})
	self.assertTrue(obj['name'] == 'testing')

    def test_get_patient(self):
	patient_id = self.db.patients.insert_one({'name': 'roberto'}).inserted_id
	r = requests.get(base_url + "/patients/%s" % patient_id)
	print "***********************"
	print r.json
	#patient = json_util.loads(r.json)
	#self.assertEqual(patient['name'], 'roberto')

    def test_add_patient(self):
	payload = {'name': 'Mary Jane'}
	r = requests.post(base_url + '/patients', data = payload)
	patient = r.json
	#self.assertEqual(patient['name'], 'Mary Jane')
