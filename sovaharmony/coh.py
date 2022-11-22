'''
@autor: Verónica Henao Isaza, Universidad de Antioquia, 2022
'''

from scipy.signal import coherence
from mne_connectivity import spectral_connectivity_epochs as mne_conn
import numpy as np
#from sovaharmony.utils import _verify_epochs_axes,_verify_epoch_continuous
import itertools
# Why not use https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.spectral_connectivity_epochs.html???

def get_coherence(signal,bands,window='hann',freqs=None,Cfxy=None):
    if not freqs and not Cfxy and window:
        freqs,Cfxy = coherence(signal,window)
        
    blist = list(bands.keys())
    nbands = len(bands.keys())
    nchans = len(signal.info['ch_names'])
    Cbxy = np.empty((nbands,nchans,nchans))
    for b,brange in bands.items():
        bidx = blist.index(b)
        band_freqs_idxs = np.where(np.logical_and(brange[0]<=freqs, freqs<=brange[1]))[0]
        Cbxy[bidx,:,:] = np.mean(Cfxy[band_freqs_idxs,:,:],axis=0)

    return bands,Cbxy
