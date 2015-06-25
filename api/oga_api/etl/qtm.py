import scipy.io as sio

def readQTMFile(qtmFile):
    content = sio.loadmat(qtmFile)
    
    index = 0
    mat_var_index = 0
    for key in content.keys(): 
        index = key.find('__') #the variable in the matlab file is the first key that don't have this chars
        if index == -1:
            break
        mat_var_index += 1

    if index != -1:
        raise ValueError("File format wrong. Don't have the initial variable")

    root_var = content[content.keys()[mat_var_index]][0,0] 
    trajectories = root_var['Trajectories'][0,0]['Unidentified'][0,0]['Data']
    new_content = {
            'frame_rate': root_var['FrameRate'][0,0], 
            'trajectories': trajectories,
            'frames': root_var['Frames'][0,0],
            'number_markers': trajectories.shape[0] 
            }
    
    return new_content
