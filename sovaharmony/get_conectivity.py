from sovaharmony.coh import get_coherence_freq
from sovaharmony.sl import get_sl_freq
from sovaharmony.p_entropy import get_entropy_freq
#from sovaharmony.pme import get_pme_freq
#from sovaharmony.pme import Modulation_Bands_Decomposition,Modulation_Bands_Spectrum,Modulation_Bands_Decomposition_Hamming
from sovaharmony.pme import Amplitude_Modulation_Analysis
import numpy as np
from sovaflow.flow import fit_spatial_filter

def get_conectivity_band(signal,mode):
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
    output_channels = {mode : {},
              'channels':signal.info['ch_names'],
              'bands':bands_labels}

    if mode == 'pme':    
            data = signal.get_data()
            (e, c, t) = data.shape
            new_data = np.transpose(data.copy(),(1,2,0))
            for e in range(data.shape[0]):
                for c in range(data.shape[1]):
                    assert np.all(data[e,c,:] == new_data[c,:,e])
            pme_ = Amplitude_Modulation_Analysis(new_data,signal.info['sfreq'],Bands=bands)
            output_channels['pme'] = pme_
    
    else:
        for limits,label in zip(bands,bands_labels):
            fmin = limits[0]
            fmax = limits[1]
            
            if mode == 'coherence':
                coherence_ = get_coherence_freq(signal,fmin=fmin,fmax=fmax,passband=True)
                output_channels['coherence'][label] = coherence_
            elif mode == 'sl':
                sl_ = get_sl_freq(signal,fmin=fmin,fmax=fmax,passband=True)
                output_channels['sl'][label] = sl_
            elif mode == 'entropy':
                entropy_ = get_entropy_freq(signal,fmin=fmin,fmax=fmax,passband=True)
                output_channels['entropy'][label] = entropy_
      
    return output_channels

def run_channels(signal,mode):
    cpot_d = np.zeros(signal.shape[0])
    cpot_t = np.zeros(signal.shape[0])
    cpot_a1 = np.zeros(signal.shape[0])
    cpot_a2 = np.zeros(signal.shape[0])
    cpot_b1 = np.zeros(signal.shape[0])
    cpot_b2 = np.zeros(signal.shape[0])
    cpot_b3 = np.zeros(signal.shape[0])
    cpot_g = np.zeros(signal.shape[0])
    #iaf_parameter = np.zeros(signal.shape[0])
    for chan in np.array(list(range(signal.shape[0]))):
        cpot_d[chan], cpot_t[chan], cpot_a1[chan], cpot_a2[chan], cpot_b1[chan], cpot_b2[chan], cpot_b3[chan], cpot_g[chan] = get_conectivity_band(signal[chan,:,:],mode)
    return cpot_d, cpot_t, cpot_a1, cpot_a2, cpot_b1, cpot_b2,cpot_b3, cpot_g

def run_ics(signal,spatial_filter,s_freq,mode):
    """
    signal: array with shape nchans,points,epochs
    spatial_filter: W demixing matrix, channels in the same order as signal
    """
    if spatial_filter is not None:
        nchans,points,epochs = signal.shape
        signalCont = np.reshape(signal,(nchans,points*epochs),order='F')
        ics = spatial_filter @ signalCont
        ics_epoch = np.reshape(ics,(ics.shape[0],points,epochs),order='F')
        for test_epoch in range(np.max([epochs,10])):
            assert np.all(ics[:,test_epoch*points:(test_epoch+1)*points]==ics_epoch[:,:,test_epoch])
        result = run_channels(ics_epoch,s_freq,mode)
        return result
    else:
        return None

def get_ics_derivatives(signal,mode,spatial_filter=None):
    """
    signal: mne.Epochs object
    spatial_filter = tuple (A,W, spatial filter ch_names)
    """
    signal = signal.copy()
    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']

    if spatial_filter is not None:
        # ICs powers
        A,W,spatial_filter_chs = spatial_filter
        intersection_chs = list(set(spatial_filter_chs).intersection(signal.ch_names))
        W_adapted = fit_spatial_filter(W,spatial_filter_chs,intersection_chs,mode='demixing')
        signal.reorder_channels(intersection_chs)
        data_for_ics = np.transpose(signal._data,(1,2,0))

        ic_powers_by_band = run_ics(data_for_ics,W_adapted,signal.info['sfreq'],mode)

        if ic_powers_by_band is not None:
            output_ics = {'ics_power' :  ic_powers_by_band,
                'channels':intersection_chs,
                'bands':bands_labels,
                'W':W_adapted}
        else:
            output_ics = None
    else:
        output_ics = None
    return output_ics