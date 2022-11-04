'''
@autor: Verónica Henao Isaza, Universidad de Antioquia, 
'''

from scipy.signal import coherence
import numpy as np

def get_coherence_freq(new_signal,fmin=None,fmax=None,passband=False):
    '''
    Parameters
    ----------
        new_signal:
        fmin: None
        fmax: None
        passband: False

    Returns
    -------
        fc:
        Cxyc:
    '''
    if passband:
        new_signal =new_signal.filter(fmin,fmax)

    data = new_signal.get_data()
    (e, c, t) = data.shape
    new_data = np.concatenate(data,axis=-1)
    for e in range(data.shape[0]):
        for c in range(data.shape[1]):
            assert np.all(data[e,c,:] == new_data[c,e*t:(e+1)*t])
    for a in range(len(new_signal.info['ch_names'])):
        for b in range(a,len(new_signal.info['ch_names'])):
            if a != b:
                fc, Cxyc = coherence(new_data[a,:], new_data[b,:], new_signal.info['sfreq'], 'hann', nperseg = 1000)
    return fc, Cxyc

