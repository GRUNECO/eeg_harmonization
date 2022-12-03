'''
@autor: Verónica Henao Isaza, Universidad de Antioquia, 2022
'''

from scipy.signal import coherence
import numpy as np
from sovaharmony.utils import _verify_epochs_axes,_verify_epoch_continuous
import itertools
# Why not use https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.spectral_connectivity_epochs.html???

def get_coherence_epochs(signal,window=3):
    '''
    Parameters
    ----------
        signal:mne.Epochs
        window: in seconds
    Returns
    -------
        fc:
        Cxyc:
    '''
    ch_names = signal.info['ch_names']
    data = signal.get_data()
    (e, c, t) = data.shape
    new_data = np.concatenate(data,axis=0)
    nperseg = int(np.floor(window*signal.info['sfreq']))
    _verify_epoch_continuous(data,new_data,('epochs','spaces','times'))
    fc, Cxyc = coherence(new_data[0,:], new_data[0,:], signal.info['sfreq'], 'hann', nperseg = nperseg)
    Cfxy =np.empty((len(fc),c,c))
    pairs = itertools.product(ch_names,ch_names)
    for x,y in pairs:
        a = ch_names.index(x)
        b = ch_names.index(y)
        fc2, Cxy = coherence(new_data[a,:], new_data[b,:], signal.info['sfreq'], 'hann', nperseg = nperseg)
        assert np.all(fc==fc2)
        Cfxy[:,a,b]=Cxy
    return fc, Cfxy

def get_coherence_continuous(signal,bands,window=3,freqs=None,Cfxy=None):
    if not freqs and not Cfxy and window:
        freqs,Cfxy = get_coherence_epochs(signal,window)
    blist = list(bands.keys())
    nbands = len(bands.keys())
    nchans = len(signal.info['ch_names'])
    Cbxy = np.empty((nbands,nchans,nchans))
    for b,brange in bands.items():
        bidx = blist.index(b)
        band_freqs_idxs = np.where(np.logical_and(brange[0]<=freqs, freqs<=brange[1]))[0]
        Cbxy[bidx,:,:] = np.mean(Cfxy[band_freqs_idxs,:,:],axis=0)

    return bands,Cbxy

def get_coherence(signal,bands,window):
    freqs,Cfxy = get_coherence_epochs(signal,window)
    _,Cbxy = get_coherence_continuous(signal,bands,freqs=freqs,Cfxy=Cfxy,window=None)
    return _,Cbxy