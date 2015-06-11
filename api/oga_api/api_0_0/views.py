from . import main_blueprint
from oga_api import get_db_connection
from flask import current_app, request
from flask.json import jsonify
from pymongo import MongoClient
from bson import json_util, ObjectId
from flask.ext.cors import cross_origin

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

@main_blueprint.route('/patients/', methods=['GET', 'POST'])
def patients():
    if request.method == 'GET':
	db = get_db()
	patients = list(db.patients.find({}))
	return json_util.dumps(patients), 200
    else:
    	db = get_db()
	patient = request.json
	patient_id = db.patients.insert_one(patient).inserted_id
	patient = db.patients.find_one({'_id': ObjectId(patient_id)})
	return json_util.dumps(patient), 201

@main_blueprint.route('/gait_sample/upload/', methods=["POST", "GET"])
def gait_sample_upload():
	print 'hi'
	stream = request.files['file'].stream
	#for line in stream:
	#	print line
	#import pdb; pdb.set_trace()
	return json_util.dumps({'data':'ok'}), 200

