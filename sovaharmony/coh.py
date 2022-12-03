'''
@autor: Verónica Henao Isaza, Universidad de Antioquia, 2022
'''

from scipy.signal import coherence
#from mne_connectivity import spectral_connectivity_epochs as mne_conn
import numpy as np
#from sovaharmony.utils import _verify_epochs_axes,_verify_epoch_continuous
import itertools
# Why not use https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.spectral_connectivity_epochs.html???

def get_coherence(signal,bands,fs,window='hann',Cfxy=None):
    for a in range(len(signal.get_data()[1])):
        for b in range(a,len(signal.get_data()[1])):
            if a != b:
                freq,Cfxy = coherence(signal.get_data()[a,:],signal.get_data()[b,:],fs,window)
    blist = list(bands.keys())
    nbands = len(bands.keys())
    nchans = len(signal.info['ch_names'])
    Cbxy = np.empty((nbands,nchans,nchans))

    return bands,Cbxy
