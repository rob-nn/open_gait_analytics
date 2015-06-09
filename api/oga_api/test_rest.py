import unittest
from . import create_app, get_db_connection
from bson import json_util
from flask import current_app, url_for

class TestRest(unittest.TestCase):
    db = None
    def setUp(self):
	self.app = create_app('testing')
	self.app_context = self.app.app_context()
	self.app_context.push()
        self.db = get_db_connection('testing')
        self.db.patients.drop()
	self.client = self.app.test_client(use_cookies=True)	

    def tearDown(self): 
        if self.db:
            self.db.patients.drop()
	self.app_context.pop()

    def test_app_exists(self):
	self.assertFalse(current_app is None)

    def test_app_is_testing(self):
	self.assertTrue(current_app.config['TESTING'])

    def test_check_connection(self):
	obj = self.db['patients'].insert_one({'name': 'testing'})
	obj = self.db.patients.find_one({'name': 'testing'})
	self.assertTrue(obj['name'] == 'testing')

    def test_get_patient(self):
	patient_id = self.db.patients.insert_one({'name': 'roberto'}).inserted_id
	url = url_for('oga_api_0_0.get_patient', id = patient_id)
	r = self.client.get(url)
	patient = json_util.loads(r.data.decode('utf-8'))
	self.assertEqual(r.status_code, 200)
	self.assertEqual(patient['name'], 'roberto')
    
    def test_get_patient_404(self):
	url = url_for('oga_api_0_0.get_patient', id = u'000000000000000000000000')
	r = self.client.get(url)
	self.assertEqual(r.status_code, 404)

    def test_add_patient(self):
	payload = json_util.dumps({'name': 'Mary Jane'})
	r = self.client.post(url_for('oga_api_0_0.patients'), headers={'Content-Type': 'application/json'}, data = payload)
	self.assertEqual(r.status_code, 201)
	patient = json_util.loads(r.data.decode('utf-8')) 
	self.assertEqual(patient['name'], 'Mary Jane')

    def test_get_patients(self):
        url = url_for('oga_api_0_0.patients')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        patients = json_util.loads(r.data.decode('utf-8'))
        self.assertEqual(len(patients), 0)
        self.db.patients.insert_one({'name': 'roberto'})
        self.db.patients.insert_one({'name': 'Mary Jane'})
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        patients = json_util.loads(r.data.decode('utf-8'))
        self.assertEqual(len(patients), 2)
