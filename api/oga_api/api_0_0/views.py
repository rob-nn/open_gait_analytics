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

@main_blueprint.route('/concept/graph')
def get_graph():
    import matplotlib.pyplot as plt, mpld3
    from mpl_toolkits.mplot3d import axes3d

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x= y= z = np.arange(10)
    ax.plot_wireframe(x,y,z)
    mpld3.show()
    html_str = mpld3.fig_to_html(fig)
    return html_str

@main_blueprint.route('/gait_sample/<id>/<sample_index>/<marker_index>')
def plot_marker(id, sample_index, marker_index):
    sample_index = int(sample_index)
    db = get_db()
    patient = db.patients.find_one({'_id': ObjectId(id)})
    if not patient:
        return jsonify({'error': 'Patient not found. Oid:' + id}), 404 
    if  'gait_samples' not in patient.keys() or sample_index >= len(patient['gait_samples'] ):
        return jsonify({'error': 'Gait sample index ' + str(sample_index) + ' for  Oid:' + id + ' not found.'}), 404 
  
    import matplotlib.pyplot as plt, mpld3

    gait_sample = patient['gait_samples'][sample_index]
    x =  gait_sample['data']['trajectories'][maker_index, 0, :]
    y =  gait_sample['data']['trajectories'][maker_index, 1, :]
    z =  gait_sample['data']['trajectories'][maker_index, 2, :]
 
    fig = plt.figure()
    plt.plot(x, y, z)
    plt.show()
    html_string= mpld3.fig_to_html(fig)

    return html_string
