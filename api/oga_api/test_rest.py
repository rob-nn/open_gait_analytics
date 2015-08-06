import unittest
from . import create_app, get_db_connection
from bson import json_util, ObjectId
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
	self.db.positionals_data.drop()
	self.client = self.app.test_client(use_cookies=True)	

    def tearDown(self): 
        if self.db:
            self.db.patients.drop()
	    self.db.positionals_data.drop()
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
	 
    def test_plot_marker_invalid(self) :
	url = url_for('oga_api_0_0.plot_marker', id_positionals_data = u'000000000000000000000000', marker_index = 0)
	r = self.client.get(url)
	self.assertEqual(r.status_code, 404)

    def test_plot_marker_invalid_index(self) :
	if True: return;
	trajectories = np.arange(27).reshape((3,3,3))
	gait_sample = {'data': {'trajectories': trajectories}}
	patient = {'name': 'roberto', 'gait_samples': [gait_sample]}
	patient_id = self.db.patients.insert_one(patient).inserted_id
	url = url_for('oga_api_0_0.plot_marker', id = patient_id, sample_index = 1, marker_index =0)
	r = self.client.get(url)
	self.assertEqual(r.status_code, 404)

    def test_plot_marker(self):
	patient = {'name': 'Roberto', 'gait_samples' : [{'description': 'walk'}]}
	patient_id = self.db.patients.insert_one(patient).inserted_id
	patient = self.db.patients.find_one({'_id': patient_id})
	qtm_file = open('oga_api/etl/Walk5.mat')
	url = url_for('oga_api_0_0.gait_sample_upload', patient_id=patient_id, gait_sample_index=0)
	r = self.client.post(url, data = {'file': (qtm_file, 'Walk5.mat'),})
	self.assertEqual(r.status_code, 200)
	pos = self.db.positionals_data.find_one({'patient_id': patient_id, 'gait_sample_index': 0})
	url = url_for('oga_api_0_0.plot_marker', id_positionals_data = pos['_id'], sample_index = 1, marker_index =0)

    def test_gait_sample_upload_add(self):
	patient = {'name': 'Roberto', 'gait_samples' : [{'description': 'walk '}]}
	patient_id = self.db.patients.insert_one(patient).inserted_id
	patient = self.db.patients.find_one({'_id': patient_id})	
	qtm_file = open('oga_api/etl/Walk1.mat')
	url = url_for('oga_api_0_0.gait_sample_upload', patient_id=patient_id, gait_sample_index=0)
	r = self.client.post(url, data = {'file': (qtm_file, 'Walk1.mat'),})
	self.assertEqual(r.status_code, 200)
	positional_data = json_util.loads(r.data.decode('utf-8')) 
	self.assertEqual(positional_data['frames'], 1491)
	self.assertEqual(positional_data['frame_rate'], 315)
	self.assertEqual(positional_data['number_markers'], 88)
	self.assertEqual(positional_data['original_filename'], 'Walk1.mat')
	self.assertEqual(len(positional_data['markers']), 88)
	self.assertEqual(positional_data['patient_id'], ObjectId(patient_id))
	self.assertEqual(positional_data['gait_sample_index'], 0)
	for marker in positional_data['markers']:
		self.assertEqual(marker, '')

        #test angular velocities





    def test_gait_sample_upload_update_and_get_trajectories(self):
        patient = {'name': 'Roberto', 'gait_samples' : [{'description': 'walk 1'}, {'description': 'walk 2'}]}
	patient_id = self.db.patients.insert_one(patient).inserted_id
	patient = self.db.patients.find_one({'_id': patient_id})	
	qtm_file = open('oga_api/etl/Walk2.mat')
	url = url_for('oga_api_0_0.gait_sample_upload', patient_id=patient_id, gait_sample_index=0)
	r = self.client.post(url, data = {'file': (qtm_file, 'Walk2.mat'),})
        qtm_file.close()
        count = self.db.positionals_data.count({'patient_id': ObjectId(patient_id), 'gait_sample_index': 0})
        self.assertEqual(count, 1)
        count = self.db.positionals_data.count({'patient_id': ObjectId(patient_id)})
        self.assertEqual(count, 1)
        #check get trajectories
        pos = self.db.positionals_data.find_one({'patient_id': ObjectId(patient_id), 'gait_sample_index': 0})
        url = url_for('oga_api_0_0.get_trajectories', id_positionals = pos['_id'])
        r = self.client.get(url)
	trajectories = json_util.loads(r.data.decode('utf-8')) 
        self.assertTrue(type(trajectories) is list)

    def test_gait_sample_upload_two_times(self):
        patient = {'name': 'Roberto', 'gait_samples' : [{'description': 'walk 1'}, {'description': 'walk 2'}]}
	patient_id = self.db.patients.insert_one(patient).inserted_id
	patient = self.db.patients.find_one({'_id': patient_id})	
	qtm_file = open('oga_api/etl/Walk2.mat')
	url = url_for('oga_api_0_0.gait_sample_upload', patient_id=patient_id, gait_sample_index=0)
	r = self.client.post(url, data = {'file': (qtm_file, 'Walk2.mat'),})
        qtm_file.close()
	qtm_file = open('oga_api/etl/Walk2.mat')
	self.assertEqual(r.status_code, 200)
        url = url_for('oga_api_0_0.gait_sample_upload', patient_id=patient_id, gait_sample_index=1)
	r = self.client.post(url, data = {'file': (qtm_file, 'Walk2.mat'),})
        qtm_file.close()
        count = self.db.positionals_data.count({'patient_id': ObjectId(patient_id), 'gait_sample_index': 0})
        self.assertEqual(count, 1)
        count = self.db.positionals_data.count({'patient_id': ObjectId(patient_id), 'gait_sample_index': 1})
        self.assertEqual(count, 1)
        count = self.db.positionals_data.count({'patient_id': ObjectId(patient_id)})
        self.assertEqual(count, 2)

    def test_get_positional_data(self):
	positional_data = {'patient_id': ObjectId(u'000000000000000000000000'), 'gait_sample_index':0}
	pos_id = self.db.positionals_data.insert_one(positional_data).inserted_id
	url = url_for('oga_api_0_0.get_positional_data', id_patient = u'000000000000000000000000', gait_sample_index = 0)
	r = self.client.get(url)
	pos = json_util.loads(r.data.decode('utf-8'))
	self.assertEqual(r.status_code, 200)
	self.assertEqual(pos['gait_sample_index'], 0)

    def test_get_positional_data(self):
	url = url_for('oga_api_0_0.get_positional_data', id_patient = u'000000000000000000000000', gait_sample_index = 0)
	r = self.client.get(url)
	self.assertEqual(r.status_code, 404)

    def test_update_positional_data(self):
        trajectories = [[0, 0, 0]]
        positional_data = {'patient_id': ObjectId(u'000000000000000000000000'), 'gait_sample_index':0, 'initial_frame':0, 'trajectories': trajectories}
	pos_id = self.db.positionals_data.insert_one(positional_data).inserted_id
	positional_data = self.db.positionals_data.find_one({'_id': ObjectId(pos_id)})
	positional_data['initial_frame'] = 1
	url = url_for('oga_api_0_0.update_positional_data')
	r = self.client.put(url,  headers={'Content-Type': 'application/json'}, data = json_util.dumps(positional_data))
	self.assertEqual(r.status_code, 200)
	pos_updated = self.db.positionals_data.find_one({'_id': ObjectId(pos_id)})
	self.assertEqual(pos_updated['initial_frame'], 1)
	self.assertEqual(pos_updated['trajectories'][0], trajectories[0])

    def test_update_positional_data_two_times(self):
        trajectories = [[0, 0, 0]]
        positional_data = {'patient_id': ObjectId(u'000000000000000000000000'), 'gait_sample_index':0, 'initial_frame':0, 'trajectories': trajectories}
	pos_id = self.db.positionals_data.insert_one(positional_data).inserted_id
        del positional_data['trajectories']
        positional_data['initial_frame'] = 5
	url = url_for('oga_api_0_0.update_positional_data')
	r = self.client.put(url,  headers={'Content-Type': 'application/json'}, data = json_util.dumps(positional_data))
	self.assertEqual(r.status_code, 200)
	pos_updated = self.db.positionals_data.find_one({'_id': ObjectId(pos_id)})
        self.assertEqual(pos_updated['initial_frame'], 5)
	self.assertEqual(pos_updated['trajectories'][0], trajectories[0])

    def test_update_positional_data_position_not_found(self):
	positional_data = {'_id': ObjectId(u'000000000000000000000000'), 'patient_id': ObjectId(u'000000000000000000000000'), 'gait_sample_index':0, 'initial_frame':0}
	url = url_for('oga_api_0_0.update_positional_data')
	r = self.client.put(url,  headers={'Content-Type': 'application/json'}, data = json_util.dumps(positional_data))
	self.assertEqual(r.status_code, 404)


    def test_delete_positional_data(self):
        trajectories = [[0, 0, 0]]
        positional_data = {'patient_id': ObjectId(u'000000000000000000000000'), 'gait_sample_index':0, 'initial_frame':0, 'trajectories': trajectories}
	pos_id = self.db.positionals_data.insert_one(positional_data).inserted_id
	url = url_for('oga_api_0_0.delete_positional_data', pos_id = pos_id)
	r = self.client.delete(url,  headers={'Content-Type': 'application/json'})
	self.assertEqual(r.status_code, 200)
	pos_data = self.db.positionals_data.find_one({'_id': ObjectId(pos_id)})
        self.assertEqual(pos_data, None)

    def test_delete_unexistent_positional_data(self):
	url = url_for('oga_api_0_0.delete_positional_data', pos_id = ObjectId(u'000000000000000000000000'))
        r = self.client.delete(url)
        self.assertEqual(r.status_code, 412)
