from . import main_blueprint
from oga_api import get_db_connection
from flask import current_app, request
from flask.json import jsonify
from pymongo import MongoClient
from bson import json_util

def get_db():
    connection = MongoClient(current_app.config['DB_URI'])
    db = connection[current_app.config['DB_NAME']]
    return db




@main_blueprint.route('/patients/<id>')
def get_patient(id):
    db = get_db()
    patient = db.patients.find_one({'_id':id})
    if patient:
        return json_util.dumps(patient), 200
    else:
        return jsonify({'error': 'not found'}), 404 

@main_blueprint.route('/patients', methods=['POST'])
def new_patient():
    db = get_db()
    patient = request.json
    patient_id = db.patients.insert_one(patient).inserted_id
    patient = db.patients.find_one({'_id': patient_id})
    return json_util.dumps(patient), 201
