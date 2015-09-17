import oga_api.ml.cmac as cmac
import numpy as np
import matplotlib.pyplot as plt

class BasicCMAC(cmac.CMAC):
    def __init__(self, trajectories, markers, activations, output, num_iterations):
        self._num_iterations = num_iterations
        confs = []
        conf = None
        data_set = None
        for marker in markers:
            if 'xCheckedForInput' in marker and marker['xCheckedForInput'] and 'qx'in marker:
                data = trajectories[marker['index'], 0, :]
                conf = cmac.SignalConfiguration(data.min(), data.max(), marker['qx'],  marker['description'])
                if conf != None: confs.append(conf)        
                if data_set == None: data_set = np.reshape(data, (len(data), 1))
                else: data_set = np.concatenate((data_set,  np.reshape(data, (len(data), 1))), axis=1)
            if 'yCheckedForInput' in marker and marker['yCheckedForInput'] and 'qy'in marker:
                data = trajectories[marker['index'], 1, :]
                conf = cmac.SignalConfiguration(data.min(), data.max(), marker['qy'],  marker['description'])
                if conf != None: confs.append(conf)        
                if data_set == None: data_set = np.reshape(data, (len(data), 1))
                else: data_set = np.concatenate((data_set,  np.reshape(data, (len(data), 1))), axis=1)
            if 'zCheckedForInput' in marker and marker['zCheckedForInput'] and 'qz'in marker:
                data = trajectories[marker['index'], 2, :]
                conf = cmac.SignalConfiguration(data.min(), data.max(), marker['qz'],  marker['description'])
                if conf != None: confs.append(conf)        
                if data_set == None: data_set = np.reshape(data, (len(data), 1))
                else: data_set = np.concatenate((data_set,  np.reshape(data, (len(data), 1))), axis=1)
 
        super(BasicCMAC, self).__init__(confs, activations)
        self._data_set = data_set
        self._generate_data_for_training_and_test(trajectories)

    def _generate_data_for_training_and_test(self, trajectories):
        data_out = None
        data_out_test = None
        data_in = None
        data_test = None
        data = self._data_set
""""kk 
        for i in range(data.shape[0]):
            new = np.reshape(data[i, :], (1, data.shape[1]))
            out = np.reshape(loader.data[i, out_index], (1,1))
            if i % 2 == 0:
                if data_in == None:
                    data_in = new
                    data_out = out
                else:
                    data_in = np.concatenate((data_in, new))
                    data_out = np.concatenate((data_out, out))
            else:
                if data_test == None:
                    data_test = new
                    data_out_test = out
                else:
                    data_test = np.concatenate((data_test, new))
                    data_out_test = np.concatenate((data_out_test, out))

        self._data_out = data_out 
        self._data_out_test = data_out_test
        self._data_in = data_in
        self._data_test = data_test
    def train(self): 
        if self._um_iterations < 1:
            raise ParameterInvalid('Number of iterations must be greater than 1')
        t = cmac.Train(self, self._data_in, self._data_out, 1, self._num_iterations)
        t.train()
        self.t = t
""" 
