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

@main_blueprint.route('/gait_sample/upload/<patient_id>/<gait_sample_index>/', methods=["POST", "GET"])
def gait_sample_upload(patient_id, gait_sample_index):
    gait_sample_index = int(gait_sample_index)
    db = get_db()
    patient = db.patients.find_one({'_id': ObjectId(patient_id)})
    if not patient:
        return jsonify({'error': 'Patient not found. Oid: %s' % patient_id}), 404 
    if  'gait_samples' not in patient.keys() or gait_sample_index >= len(patient['gait_samples'] ):
        return jsonify({'error': 'Gait sample index %s for  Oid %s not found.' % (patient_id, str(gait_sample_index))}), 404 
    qtm_matlab_file = request.files['file']
    import oga_api.etl.qtm as qtm
    data = qtm.readQTMFile(qtm_matlab_file.stream)
    positional_data = {}
    positional_data['patient_id'] = ObjectId(patient_id)
    positional_data['gait_sample_index'] = gait_sample_index
    positional_data['frame_rate'] = data['frame_rate']
    positional_data['frames'] = data['frames']
    positional_data['number_markers'] = data['number_markers']
    positional_data['original_filename'] = qtm_matlab_file.filename
    markers = [];
    for i in range(data['number_markers']):
            markers.append('')
    positional_data['markers'] = markers
    positional_data['trajectories'] = data['trajectories'].tolist()
    db.positionals_data.replace_one({'patient_id': ObjectId(patient_id), 'gait_sample_index': gait_sample_index}, positional_data, True)
    pos = db.positionals_data.find_one({'patient_id': ObjectId(patient_id), 'gait_sample_index': gait_sample_index})
    del pos['trajectories']
    return json_util.dumps(pos, allow_nan=False), 200

@main_blueprint.route('/gait_sample/positional_data/<id_patient>/<gait_sample_index>/', methods=["GET"])
def get_positional_data(id_patient, gait_sample_index):
    gait_sample_index = int( gait_sample_index)
    db = get_db()
    pos = db.positionals_data.find_one({'patient_id': ObjectId(id_patient), 'gait_sample_index': gait_sample_index})
    if pos:
        if 'trajectories' in pos.keys():
            del pos['trajectories']
        return json_util.dumps(pos), 200
    else:
        return jsonify({'error': 'not found'}), 404 

@main_blueprint.route('/gait_sample/positionals_data/', methods=['PUT'])
def update_positional_data():
    db = get_db()
    pos = json_util.loads(request.data)
    positional = db.positionals_data.find_one({'_id': pos['_id']})
    if not positional:
        return jsonify({'error': 'not found'}), 404
    pos['trajectories'] = positional['trajectories']
    db.positionals_data.replace_one({'_id': pos['_id']}, pos)
    return json_util.dumps({"return": "Saved"}), 200
 
@main_blueprint.route('/concept/graph')
def get_graph():
    import matplotlib.pyplot as plt, mpld3
    fig = plt.figure()
    x= y= z = np.arange(10)
    plt.plot(x)
    html_str = mpld3.fig_to_html(fig)
    return html_str

@main_blueprint.route('/gait_sample/<id_positionals_data>/<marker_index>/', methods=['GET'])
def plot_marker(id_positionals_data, marker_index):
    id_positionals_data = id_positionals_data
    marker_index = int(marker_index)
    db = get_db()

    pos = db.positionals_data.find_one({'_id': ObjectId(id_positionals_data)})
    if not pos:
        return jsonify({'error': 'Positionals data not found. Oid:' + id_positionals_data}), 404 
    if marker_index >= pos['number_markers']:
        return jsonify({'error' : 'Marker index invalid'}), 404 

    x =  pos['trajectories'][marker_index][0]
    y =  pos['trajectories'][marker_index][1]
    z =  pos['trajectories'][marker_index][2]

    import matplotlib.pyplot as plt, mpld3

    fig = plt.figure()
    plt.plot(x, 'r')
    plt.plot(y, 'b')
    plt.plot(z, 'g')
    html_str = mpld3.fig_to_html(fig)
    return html_str, 200
