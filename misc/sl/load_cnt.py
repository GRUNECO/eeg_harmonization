"""
@author: Brayan Hoyos Madera, Universidad de Antioquia, leobahm72@gmail.com

"""

import mne 
from sovaflow.utils import createRaw
import numpy as np

def load(path):
    try:
        raw_data = mne.read_epochs(path + '.fif', verbose='error')
        data = raw_data.get_data()
        (e, c, t) = data.shape
        da_eeg_cont = np.reshape(data,(c,e*t),order='F')
        signal = createRaw(da_eeg_cont,raw_data.info['sfreq'])
        return signal._data, signal.info['sfreq']
    except:
        print("The file path: %s no found"%path)
