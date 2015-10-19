from . import main_blueprint
from oga_api import get_db_connection
from oga_api.physics import cinematic
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
    positional_data['initial_frame'] = 0
    positional_data['final_frame'] = data['frames'] - 1
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

@main_blueprint.route('/gait_sample/positional_data/<id_positionals>/trajectories/', methods=["GET"])
def get_trajectories(id_positionals):
    db = get_db()
    pos = db.positionals_data.find_one({'_id': ObjectId(id_positionals)})
    if pos and 'trajectories' in pos.keys():
        trajectories = [[[trajectorie if not np.isnan(trajectorie) else 0 for trajectorie in column] for column in line] for line in pos['trajectories']]
        return json_util.dumps(trajectories, allow_nan=False), 200
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

@main_blueprint.route('/gait_sample/positionals_data/<pos_id>/', methods=['DELETE'])
def delete_positional_data(pos_id):
    db = get_db()
    result = db.positionals_data.delete_one({'_id': ObjectId(pos_id)})
    if (result.deleted_count == 1):
    	return "", 200
    else:
	return "", 412

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

    if pos['markers'][marker_index] =="":
        title = 'Marker %s' % str(marker_index)
    else:
        title = pos['markers'][marker_index]

    trajectories = cut_trajectories(pos) 
    x_img =  trajectories[marker_index, 0, :]
    x_dom = 100 * np.arange(0, len(x_img))/np.float(len(x_img))
    y_img =  trajectories[marker_index, 1, :]
    y_dom = 100 * np.arange(0, len(y_img))/np.float(len(y_img))
    z_img =  trajectories[marker_index, 2, :]
    z_dom =  100 * np.arange(0, len(z_img))/np.float(len(z_img))

    lr_i = 0
    lr_f = x_dom.max() * 0.12 
    mst_i = lr_f
    mst_f = x_dom.max() * 0.31
    tst_i = mst_f
    tst_f = x_dom.max() * 0.50
    psw_i = tst_f
    psw_f = x_dom.max() * 0.62
    isw_i = psw_f
    isw_f = x_dom.max() * 0.75
    msw_i = isw_f
    msw_f = x_dom.max() * 0.87
    tsw_i = msw_f
    tsw_f = x_dom.max() * 1

    import matplotlib.pyplot as plt
    fig = plt.figure(1)

    plt.subplot(3,1,1)
    plt.title(title)
    plt.ylabel ("Spacial Data")
    plt.xlabel ("Percentual Gait Cycle")
    plt.axis([0, x_dom.max(), x_img.min(), x_img.max()])
    curve_x, = plt.plot(x_dom, x_img, 'r')
    plt.legend([curve_x], ['x' ], loc='best')
    plt.axvspan(xmin = lr_i, xmax=lr_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('LR', xy=(lr_i + 5, x_img.max() * 0.95))  
    plt.axvspan(xmin = mst_i, xmax=mst_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('MSt', xy=(mst_i + 5, x_img.max() * 0.95))  
    plt.axvspan(xmin = tst_i, xmax=tst_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('TSt', xy=(tst_i + 5, x_img.max() * 0.95))  
    plt.axvspan(xmin = psw_i, xmax=psw_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('PSw', xy=(psw_i + 5, x_img.max() * 0.95))  
    plt.axvspan(xmin = isw_i, xmax=isw_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('ISw', xy=(isw_i + 5, x_img.max() * 0.95))  
    plt.axvspan(xmin = msw_i, xmax=msw_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('MSw', xy=(msw_i + 5, x_img.max() * 0.95))  
    plt.axvspan(xmin = tsw_i, xmax=tsw_f, ymin =0, ymax=1, alpha = 0.6, color='y')
    plt.annotate('TSw', xy=(tsw_i + 5, x_img.max() * 0.95))  

    plt.subplot(3,1,2)
    plt.ylabel ("Spacial Data")
    plt.xlabel ("Percentual Gait Cycle")
    plt.axis([0, y_dom.max(), y_img.min(), y_img.max()])
    curve_y, = plt.plot(y_dom, y_img, 'b')
    plt.legend([curve_y], ['y' ], loc='best')
    plt.axvspan(xmin = lr_i, xmax=lr_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.axvspan(xmin = mst_i, xmax=mst_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.axvspan(xmin = tst_i, xmax=tst_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.axvspan(xmin = psw_i, xmax=psw_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.axvspan(xmin = isw_i, xmax=isw_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.axvspan(xmin = msw_i, xmax=msw_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.axvspan(xmin = tsw_i, xmax=tsw_f, ymin =0, ymax=1, alpha = 0.6, color='y')
 
    plt.subplot(3,1,3)
    plt.ylabel ("Spacial Data")
    plt.xlabel ("Percentual Gait Cycle")
    plt.axis([0, z_dom.max(), z_img.min(), z_img.max()])
    curve_z, = plt.plot(z_dom, z_img, 'g')
    plt.legend([curve_z], ['z' ], loc='best')
    plt.axvspan(xmin = lr_i, xmax=lr_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.axvspan(xmin = mst_i, xmax=mst_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.axvspan(xmin = tst_i, xmax=tst_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.axvspan(xmin = psw_i, xmax=psw_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.axvspan(xmin = isw_i, xmax=isw_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.axvspan(xmin = msw_i, xmax=msw_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.axvspan(xmin = tsw_i, xmax=tsw_f, ymin =0, ymax=1, alpha = 0.6, color='y')

    import cStringIO
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)

    html_str = """<html><body>
    <img src="data:image/png;base64,%s"/>
    </body></html>""" % sio.getvalue().encode("base64").strip()

    plt.close()
    return html_str, 200

@main_blueprint.route('/gait_sample/<id_positionals_data>/<angle_index>/angular_velocity/', methods=['GET'])
def plot_angular_velocity(id_positionals_data, angle_index):
    id_positionals_data = id_positionals_data
    angle_index = int(angle_index)
    db = get_db()
    pos = db.positionals_data.find_one({'_id': ObjectId(id_positionals_data)})
    if not pos:
        return jsonify({'error': 'Positionals data not found. Oid:' + id_positionals_data}), 404 
    if not 'angles' in pos:
        return jsonify({'error' : 'Positionals data doesn\'t contains angles.'}), 404

    angles = pos['angles']
    if angle_index < 0 or angle_index >= len(angles):
        return jsonify({'error' : 'Marker index invalid'}), 404 
    angle = angles[angle_index]
    
    t = cut_trajectories(pos).tolist()

    origin = t[int(angle['origin'])][0:3][:]
    component_a = t[int(angle['component_a'])][0:3][:]
    component_b = t[int(angle['component_b'])][0:3][:]
    av = cinematic.calc_angular_velocities(np.array(origin).T, np.array(component_a).T, np.array(component_b).T, 1/float(pos['frame_rate']))  

    av_img = av 
    av_dom = 100 * np.arange(0, len(av_img))/np.float(len(av_img))
    lr_i = 0
    lr_f = av_dom.max() * 0.12 
    mst_i = lr_f
    mst_f = av_dom.max() * 0.31
    tst_i = mst_f
    tst_f = av_dom.max() * 0.50
    psw_i = tst_f
    psw_f = av_dom.max() * 0.62
    isw_i = psw_f
    isw_f = av_dom.max() * 0.75
    msw_i = isw_f
    msw_f = av_dom.max() * 0.87
    tsw_i = msw_f
    tsw_f = av_dom.max() * 1

    import matplotlib.pyplot as plt
    fig = plt.figure(1)

    plt.subplot(1,1,1)
    plt.title("Angular Velociteis for %s" % angle['description'])
    plt.ylabel ("Degrees/Seconds")
    plt.xlabel ("Percentual Gait Cycle")
    plt.axis([0, av_dom.max(), av_img.min(), av_img.max()])
    curve_av, = plt.plot(av_dom, av_img, 'r')
    plt.axvspan(xmin = lr_i, xmax=lr_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('LR', xy=(lr_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = mst_i, xmax=mst_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('MSt', xy=(mst_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = tst_i, xmax=tst_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('TSt', xy=(tst_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = psw_i, xmax=psw_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('PSw', xy=(psw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = isw_i, xmax=isw_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('ISw', xy=(isw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = msw_i, xmax=msw_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('MSw', xy=(msw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = tsw_i, xmax=tsw_f, ymin =0, ymax=1, alpha = 0.6, color='y')
    plt.annotate('TSw', xy=(tsw_i + 5, av_img.max() * 0.90))  
 

    import cStringIO
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)

    html_str = """<html><body>
    <img src="data:image/png;base64,%s"/>
    </body></html>""" % sio.getvalue().encode("base64").strip()

    plt.close()
    return html_str, 200

@main_blueprint.route('/gait_sample/<id_positionals_data>/<angle_index>/angles/', methods=['GET'])
def plot_angles(id_positionals_data, angle_index):
    id_positionals_data = id_positionals_data
    angle_index = int(angle_index)
    db = get_db()
    pos = db.positionals_data.find_one({'_id': ObjectId(id_positionals_data)})
    if not pos:
        return jsonify({'error': 'Positionals data not found. Oid:' + id_positionals_data}), 404 
    if not 'angles' in pos:
        return jsonify({'error' : 'Positionals data doesn\'t contains angles.'}), 404
    angles = pos['angles']
    if angle_index < 0 or angle_index >= len(angles):
        return jsonify({'error' : 'Marker index invalid'}), 404 
    angle = angles[angle_index]
    t = cut_trajectories(pos).tolist()
    origin = t[int(angle['origin'])][0:3][:]
    component_a = t[int(angle['component_a'])][0:3][:]
    component_b = t[int(angle['component_b'])][0:3][:]
    a = cinematic.get_angles(np.array(origin).T, np.array(component_a).T, np.array(component_b).T)  

    a_img = a 
    a_dom = 100 * np.arange(0, len(a_img))/np.float(len(a_img))
    lr_i = 0
    lr_f = a_dom.max() * 0.12 
    mst_i = lr_f
    mst_f = a_dom.max() * 0.31
    tst_i = mst_f
    tst_f = a_dom.max() * 0.50
    psw_i = tst_f
    psw_f = a_dom.max() * 0.62
    isw_i = psw_f
    isw_f = a_dom.max() * 0.75
    msw_i = isw_f
    msw_f = a_dom.max() * 0.87
    tsw_i = msw_f
    tsw_f = a_dom.max() * 1

    import matplotlib.pyplot as plt
    fig = plt.figure(1)

    plt.subplot(1,1,1)
    plt.title("Angles for %s" % angle['description'])
    plt.ylabel ("Degrees")
    plt.xlabel ("Percentual Gait Cycle")
    plt.axis([0, a_dom.max(), a_img.min(), a_img.max()])
    curve_a, = plt.plot(a_dom, a_img, 'r')
    plt.axvspan(xmin = lr_i, xmax=lr_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('LR', xy=(lr_i + 5, a_img.max() * 0.90))  
    plt.axvspan(xmin = mst_i, xmax=mst_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('MSt', xy=(mst_i + 5, a_img.max() * 0.90))  
    plt.axvspan(xmin = tst_i, xmax=tst_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('TSt', xy=(tst_i + 5, a_img.max() * 0.90))  
    plt.axvspan(xmin = psw_i, xmax=psw_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('PSw', xy=(psw_i + 5, a_img.max() * 0.90))  
    plt.axvspan(xmin = isw_i, xmax=isw_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('ISw', xy=(isw_i + 5, a_img.max() * 0.90))  
    plt.axvspan(xmin = msw_i, xmax=msw_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('MSw', xy=(msw_i + 5, a_img.max() * 0.90))  
    plt.axvspan(xmin = tsw_i, xmax=tsw_f, ymin =0, ymax=1, alpha = 0.6, color='y')
    plt.annotate('TSw', xy=(tsw_i + 5, a_img.max() * 0.90))  
 

    import cStringIO
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)

    html_str = """<html><body>
    <img src="data:image/png;base64,%s"/>
    </body></html>""" % sio.getvalue().encode("base64").strip()

    plt.close()
    return html_str, 200


@main_blueprint.route('/simulation/cmac/training/', methods=['POST'])
def run_cmac_training():
    cmacConfig = json_util.loads(request.data)
    error = ""
    if not 'idPatient' in cmacConfig:
        error = error + " Don't contains idPatient"
    if not 'idGaitSample' in cmacConfig:
        error = error + " Don't contains idGaitSample"
    if not 'activationsNumber' in cmacConfig:
        error = error + " Don't contains activationsNumber"
    if not 'iterationsNumber' in cmacConfig:
        error = error + " Don't contains iterationsNumber"
    if not 'output' in cmacConfig:
        error = error + " Don't contains output"
    if not ('markers' in cmacConfig or 'angles' in cmacConfig):
        error = error + " Don't contains markers neither angles"
    if error != "":
        return jsonify({'error': error}), 500
    db = get_db()
    #patient = db.patients.find_one({'_id': ObjectId(cmacConfig['idPatient'])})
    pos = db.positionals_data.find_one({'_id': ObjectId(cmacConfig['idGaitSample'])})
    import oga_api.ml.basic_cmac as basic_cmac
    #import pdb; pdb.set_trace()
    b_cmac = basic_cmac.BasicCMAC(cut_trajectories(pos), pos['angles'], 1.0/float(pos['frames']), cmacConfig['markers'], cmacConfig['angles'], cmacConfig['activationsNumber'], cmacConfig['output'], cmacConfig['iterationsNumber'])
    try:
	    b_cmac.train()
    except basic_cmac.ParameterInvalid as invalid:
        return jsonify({'error': invalid.description}), 500

    result = b_cmac.fire_test()
    #basic = bc.BasicCMAC(self._trajectories, self._pos_angles, 1.0/315.0, self._cmacConfig['markers'], self._cmacConfig['angles'], self._cmacConfig['activationsNumber'], self._cmacConfig['output'], self._cmacConfig['iterationsNumber']) 
    av_img = result 
    av_dom = 100 * np.arange(0, len(av_img))/np.float(len(av_img))
    lr_i = 0
    lr_f = av_dom.max() * 0.12 
    mst_i = lr_f
    mst_f = av_dom.max() * 0.31
    tst_i = mst_f
    tst_f = av_dom.max() * 0.50
    psw_i = tst_f
    psw_f = av_dom.max() * 0.62
    isw_i = psw_f
    isw_f = av_dom.max() * 0.75
    msw_i = isw_f
    msw_f = av_dom.max() * 0.87
    tsw_i = msw_f
    tsw_f = av_dom.max() * 1

    import matplotlib.pyplot as plt
    fig = plt.figure(1)
    fig.set_size_inches(20, 6)

    plt.subplot(1,2,1)
    plt.title("Right Knee Angular Velocities")
    plt.ylabel ("Degrees / Seconds")
    plt.xlabel ("Percentual Gait Cycle")
    plt.axis([0, av_dom.max(), av_img.min(), av_img.max()])
    plt.axvspan(xmin = lr_i, xmax=lr_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('LR', xy=(lr_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = mst_i, xmax=mst_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('MSt', xy=(mst_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = tst_i, xmax=tst_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('TSt', xy=(tst_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = psw_i, xmax=psw_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('PSw', xy=(psw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = isw_i, xmax=isw_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('ISw', xy=(isw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = msw_i, xmax=msw_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('MSw', xy=(msw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = tsw_i, xmax=tsw_f, ymin =0, ymax=1, alpha = 0.6, color='y')
    plt.annotate('TSw', xy=(tsw_i + 5, av_img.max() * 0.90))  
    curve_aproximation, = plt.plot(av_dom, av_img, 'r')
    curve_real, = plt.plot(av_dom, b_cmac.data_out_test, 'b')
    plt.legend([curve_aproximation, curve_real], ['Aproximation', 'Real' ], loc='best')

    plt.subplot(1, 2, 2)
    plt.xlabel('Iterations', fontsize=15)
    plt.ylabel('Mean Squared Error', fontsize=15)
    plt.plot(b_cmac.t.E)


    import cStringIO
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)

    html_str = """<html><body>
    <img src="data:image/png;base64,%s"/>
    </body></html>""" % sio.getvalue().encode("base64").strip()

    plt.close()
    return html_str, 200



def cut_trajectories(pos):
    trajectories = np.array(pos['trajectories'])
    if 'initial_frame' in pos and 'final_frame' in pos and 'frames' in pos:
        initial = pos['initial_frame'] 
        final = pos['final_frame']
        frames = pos['frames'] 
        if initial >0 and initial < final and final < frames:
            trajectories = trajectories[:,:, initial:final]
    return trajectories




@main_blueprint.route('/gait_sample/<id_positionals_data>/<angle_index>/angular_accelerations/', methods=['GET'])
def plot_angular_acceleration(id_positionals_data, angle_index):
    id_positionals_data = id_positionals_data
    angle_index = int(angle_index)
    db = get_db()
    pos = db.positionals_data.find_one({'_id': ObjectId(id_positionals_data)})
    if not pos:
        return jsonify({'error': 'Positionals data not found. Oid:' + id_positionals_data}), 404 
    if not 'angles' in pos:
        return jsonify({'error' : 'Positionals data doesn\'t contains angles.'}), 404

    angles = pos['angles']
    if angle_index < 0 or angle_index >= len(angles):
        return jsonify({'error' : 'Marker index invalid'}), 404 
    angle = angles[angle_index]
    
    t = cut_trajectories(pos).tolist()

    origin = t[int(angle['origin'])][0:3][:]
    component_a = t[int(angle['component_a'])][0:3][:]
    component_b = t[int(angle['component_b'])][0:3][:]
    av = cinematic.calc_angular_velocities(np.array(origin).T, np.array(component_a).T, np.array(component_b).T, 1/float(pos['frame_rate']))  
    aa = cinematic.calc_angular_accelerations(av, 1/float(pos['frame_rate']))

    av_img = aa 
    av_dom = 100 * np.arange(0, len(av_img))/np.float(len(av_img))
    lr_i = 0
    lr_f = av_dom.max() * 0.12 
    mst_i = lr_f
    mst_f = av_dom.max() * 0.31
    tst_i = mst_f
    tst_f = av_dom.max() * 0.50
    psw_i = tst_f
    psw_f = av_dom.max() * 0.62
    isw_i = psw_f
    isw_f = av_dom.max() * 0.75
    msw_i = isw_f
    msw_f = av_dom.max() * 0.87
    tsw_i = msw_f
    tsw_f = av_dom.max() * 1

    import matplotlib.pyplot as plt
    fig = plt.figure(1)

    plt.subplot(1,1,1)
    plt.title("Angular Accelerations for %s" % angle['description'])
    plt.ylabel ("Degrees/Seconds^2")
    plt.xlabel ("Percentual Gait Cycle")
    plt.axis([0, av_dom.max(), av_img.min(), av_img.max()])
    curve_av, = plt.plot(av_dom, av_img, 'r')
    plt.axvspan(xmin = lr_i, xmax=lr_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('LR', xy=(lr_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = mst_i, xmax=mst_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('MSt', xy=(mst_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = tst_i, xmax=tst_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('TSt', xy=(tst_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = psw_i, xmax=psw_f, ymin =0, ymax=1, alpha = 0.2, color='b')
    plt.annotate('PSw', xy=(psw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = isw_i, xmax=isw_f, ymin =0, ymax=1, alpha = 0.2, color='y')
    plt.annotate('ISw', xy=(isw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = msw_i, xmax=msw_f, ymin =0, ymax=1, alpha = 0.4, color='y')
    plt.annotate('MSw', xy=(msw_i + 5, av_img.max() * 0.90))  
    plt.axvspan(xmin = tsw_i, xmax=tsw_f, ymin =0, ymax=1, alpha = 0.6, color='y')
    plt.annotate('TSw', xy=(tsw_i + 5, av_img.max() * 0.90))  
 

    import cStringIO
    format = "png"
    sio = cStringIO.StringIO()
    plt.savefig(sio, format=format)

    html_str = """<html><body>
    <img src="data:image/png;base64,%s"/>
    </body></html>""" % sio.getvalue().encode("base64").strip()

    plt.close()
    return html_str, 200


