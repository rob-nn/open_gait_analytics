import unittest
from . import create_app, get_db_connection
from bson import json_util
from flask import current_app, url_for
import numpy as np

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

    def test_update_patient(self):
	patient = {'name': 'Roberto'}
	patient_id = self.db.patients.insert_one(patient).inserted_id
	patient = self.db.patients.find_one({'_id': patient_id})	
	patient['name'] = 'Roberto A. Lima'
	r = self.client.put(url_for('oga_api_0_0.patients'), headers={'Content-Type': 'application/json'}, data = json_util.dumps(patient))
        self.assertEqual(r.status_code, 200)
	patient = self.db.patients.find_one({'_id': patient_id})
	self.assertEqual(patient['name'], 'Roberto A. Lima')

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
	''' 
	    def test_gait_sample_upload(self):
		qtm_file = open('oga_api/etl/Walk1.mat')
		url = url_for('oga_api_0_0.gait_sample_upload')
		r = self.client.post(url, data = {'file': (qtm_file, 'Walk1.mat'),})
		self.assertEqual(r.status_code, 200)
		qtm_data = json_util.loads(r.data.decode('utf-8')) 
		self.assertEqual(qtm_data['frames'], 1491)
		self.assertEqual(qtm_data['frame_rate'], 315)
		self.assertEqual(qtm_data['number_markers'], 88)
		self.assertEqual(qtm_data['original_filename'], 'Walk1.mat')
		self.assertEqual(len(qtm_data['markers']), 88)
		for marker in qtm_data['markers']:
			self.assertEqual(marker, '')
		#import numpy as np
		#print np.array(qtm_data['trajectories']).shape
		print r.data[:79]
	'''
    def test_plot_marker_invalid(self) :
	patient_id = self.db.patients.insert_one({'name': 'roberto'}).inserted_id
	url = url_for('oga_api_0_0.plot_marker', id = patient_id, sample_index = 0, marker_index =0)
	r = self.client.get(url)
	self.assertEqual(r.status_code, 404)

    def test_plot_marker_invalid_index(self) :
	trajectories = np.arange(27).reshape((3,3,3))
	gait_sample = {'data': {'trajectories': trajectories}}
	patient = {'name': 'roberto', 'gait_samples': [sample]}
	patient_id = self.db.patients.insert_one(patient).inserted_id
	url = url_for('oga_api_0_0.plot_marker', id = patient_id, sample_index = 1, marker_index =0)
	r = self.client.get(url)
	self.assertEqual(r.status_code, 404)
