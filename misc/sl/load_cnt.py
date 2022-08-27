"""
@author: Brayan Hoyos Madera, Universidad de Antioquia, leobahm72@gmail.com

"""

import mne 
from sovaflow.utils import createRaw
import numpy as np

def load(path):
    raw_data = mne.read_epochs(path + '.fif', verbose='error')
    data = raw_data.get_data()
    new_data = np.transpose(data.copy(),(1,2,0))
    for e in range(data.shape[0]):
        for c in range(data.shape[1]):
            assert np.all(data[e,c,:] == new_data[c,:,e])
    return new_data, raw_data.info['sfreq']