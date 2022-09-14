from scipy.signal import coherence
import numpy as np

def get_coherence_freq(signal,fmin,fmax):
    new_signal =signal.filter(fmin,fmax)
    data = new_signal.get_data()
    new_data = np.transpose(data.copy(),(1,2,0))
    for e in range(data.shape[0]):
        for c in range(data.shape[1]):
            assert np.all(data[e,c,:] == new_data[c,:,e])
    for a in range(len(signal.info['ch_names'])):
        for b in range(a,len(signal.info['ch_names'])):
            if a != b:
                fc, Cxyc = coherence(new_data[a,:], new_data[b,:], signal.info['sfreq'], 'hanning', nperseg = 25)
    return fc, Cxyc

def get_coherence_band(signal):
    bands =[[1.5,6] #delta
    ,[6,8.5] #theta
    , [8.5,10.5] #alpha1
    , [10.5,12.5] #alpha2
    , [12.5,18.5] #beta1
    , [18.5,21] #beta2
    , [21,30] #beta3
    ,[30,45] #gamma
    ]

    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
    output_channels = {'sl' : {},
              'channels':signal.info['ch_names'],
              'bands':bands_labels}

    for limits,label in zip(bands,bands_labels):
        fmin = limits[0]
        fmax = limits[1]
        
        
        coherence_ = get_coherence_freq(signal,fmin,fmax)
        output_channels['sl'][label] = coherence_
        
    return output_channels