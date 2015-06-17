import scipy.io as sio

def readQTMFile(qtmFile):
    content = sio.loadmat(qtmFile)
    root_var = content[content.keys()[0]][0,0] 
    trajectories = root_var['Trajectories'][0,0]['Unidentified'][0,0]['Data']
    new_content = {
            'frame_rate': root_var['FrameRate'][0,0], 
            'trajectories': trajectories,
            'frames': root_var['Frames'][0,0],
            'number_markers': trajectories.shape[0] 
            }
    
    return new_content
