from . import main_blueprint
from oga_api import get_db_connection
from flask import current_app, request
from flask.json import jsonify
from pymongo import MongoClient
from bson import json_util, ObjectId
from flask.ext.cors import cross_origin
import numpy as np

def get_db():
    connection = MongoClient(current_app.config['DB_URI'])
    db = connection[current_app.config['DB_NAME']]
    return db

@main_blueprint.route('/patients/<id>/')
def get_patient(id):
    db = get_db()
    patient = db.patients.find_one({'_id': ObjectId(id)})
    if patient:
        return json_util.dumps(patient), 200
    else:
        return jsonify({'error': 'not found'}), 404 

@main_blueprint.route('/patients/', methods=['GET', 'POST', 'PUT'])
def patients():
    if request.method == 'GET':
	db = get_db()
	patients = list(db.patients.find({}))
	return json_util.dumps(patients), 200
    else:
    	db = get_db()
	patient = json_util.loads(request.data)
	if request.method == 'POST':
		patient_id = db.patients.insert_one(patient).inserted_id
		patient = db.patients.find_one({'_id': ObjectId(patient_id)})
		return json_util.dumps(patient), 201
	elif request.method == 'PUT':
		#import pdb; pdb.set_trace()
		db.patients.replace_one({'_id': patient['_id']}, patient)
		return json_util.dumps({"return": "Saved"}), 200

@main_blueprint.route('/gait_sample/upload/', methods=["POST", "GET"])
def gait_sample_upload():
        qtm_matlab_file = request.files['file']
        import oga_api.etl.qtm as qtm
        data = qtm.readQTMFile(qtm_matlab_file.stream)
        data['trajectories'] = np.nan_to_num(data['trajectories'])
	data['original_filename'] = qtm_matlab_file.filename
	markers = [];
	for i in range(data['number_markers']):
		markers.append('')
	data['markers'] = markers
	return json_util.dumps(data, allow_nan=False), 200
