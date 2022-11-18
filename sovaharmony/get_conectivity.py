from sovaharmony.coh import get_coherence_freq
from sovaharmony.sl import get_sl
from sovaharmony.p_entropy import get_entropy_freq
#from sovaharmony.pme import get_pme_freq
#from sovaharmony.pme import Modulation_Bands_Decomposition,Modulation_Bands_Spectrum,Modulation_Bands_Decomposition_Hamming
from sovaharmony.pme import Amplitude_Modulation_Analysis
import numpy as np
from sovaflow.flow import fit_spatial_filter
from sovaflow.utils import createRaw
import mne


def get_conectivity_band(signal,mode,spatial_filter):
    bands =[[1.5,6] #delta
    ,[6,8.5] #theta
    , [8.5,10.5] #alpha1
    , [10.5,12.5] #alpha2
    , [12.5,18.5] #beta1
    , [18.5,21] #beta2
    , [21,30] #beta3
    ,[30,45] #gamma
    ]
    if spatial_filter is not None:
        # ICs powers
        A,W,spatial_filter_chs = spatial_filter
        intersection_chs = list(set(spatial_filter_chs).intersection(signal.ch_names))
        W_adapted = fit_spatial_filter(W,spatial_filter_chs,intersection_chs,mode='demixing')

        bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
        output_channels = {mode : {},
                'channels':signal.info['ch_names'],
                'bands':bands_labels}
        output_ics = {mode :{},
                    'channels':signal.info['ch_names'],
                    'bands':bands_labels,
                    'W':W_adapted}

        if mode == 'pme':    
                data = signal.get_data()
                (e, c, t) = data.shape
                new_data = np.transpose(data.copy(),(1,2,0))
                for e in range(data.shape[0]):
                    for c in range(data.shape[1]):
                        assert np.all(data[e,c,:] == new_data[c,:,e])
                ics_epoch_pme = run_ics(signal,spatial_filter)
                pme_ = Amplitude_Modulation_Analysis(ics_epoch_pme,signal.info['sfreq'],Bands=bands)
                output_channels['pme'] = pme_
                output_ics['ics_pme'] = ics_epoch_pme
        
        else:
            for limits,label in zip(bands,bands_labels):
                fmin = limits[0]
                fmax = limits[1]
                
                if mode == 'coherence':
                    ics_epoch_coherence = run_ics(signal,spatial_filter)
                    coherence_ = get_coherence_freq(ics_epoch_coherence,fmin=fmin,fmax=fmax,passband=True)
                    output_channels['coherence'][label] = coherence_
                    output_ics['ics_coherence'] = ics_epoch_coherence
                elif mode == 'sl':
                    sl_ = get_sl_freq(signal,fmin=fmin,fmax=fmax,passband=True)
                    output_channels['sl'][label] = sl_
                    output_ics['ics_sl'] = ics_epoch_sl
                elif mode == 'entropy':
                    ics_epoch_entropy = run_ics(signal,spatial_filter)
                    entropy_ = get_entropy_freq(ics_epoch_entropy,fmin=fmin,fmax=fmax,passband=True)
                    output_channels['entropy'][label] = entropy_
                    output_ics['ics_entropy'] = ics_epoch_entropy
      
    return output_channels,output_ics

    
########################################### SL ############################################
def get_sl_derivates(signal):
    """
    signal: mne.Epochs object
    """
    channel_powers_by_band = run_sl_channels(signal,passband=True)
    return channel_powers_by_band

def get_ics_sl_derivatives(signal,spatial_filter=None):
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
        #data_for_ics = np.transpose(signal._data,(1,2,0))

        ic_powers_by_band = run_sl_ics(signal,W_adapted)

        if ic_powers_by_band is not None:
            output_ics = {'ics_sl' :  ic_powers_by_band,
                'channels':intersection_chs,
                'bands':bands_labels,
                'W':W_adapted}
        else:
            output_ics = None
    else:
        output_ics = None
    return output_ics

def run_sl_channels(signal,passband=False):
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
    output_channels = {'sl': {},
              'channels':signal.info['ch_names'],
              'bands':bands_labels}
    for limits,label in zip(bands,bands_labels):
        fmin = limits[0]
        fmax = limits[1]
        if passband:
            signal = signal.filter(fmin,fmax)
        data = signal.get_data()
        new_data = np.transpose(data.copy(),(1,2,0))
        for e in range(data.shape[0]):
            for c in range(data.shape[1]):
                assert np.all(data[e,c,:] == new_data[c,:,e])
        sl = get_sl(new_data, signal.info['sfreq'])
        output_channels['sl'][label] = sl
    return output_channels

def run_sl_ics(signal_mne,spatial_filter):
    """
    signal: array with shape nchans,points,epochs
    spatial_filter: W demixing matrix, channels in the same order as signal
    """
    signal = signal_mne.get_data()
    signal = np.transpose(signal,(1,2,0))
    if spatial_filter is not None:
        nchans,points,epochs = signal.shape
        signalCont = np.reshape(signal,(nchans,points*epochs),order='F')
        ics = spatial_filter @ signalCont
        ics_epoch = np.reshape(ics,(ics.shape[0],points,epochs),order='F')
        for test_epoch in range(np.max([epochs,10])):
            assert np.all(ics[:,test_epoch*points:(test_epoch+1)*points]==ics_epoch[:,:,test_epoch])
        info_epochs=mne.create_info([str(x) for x in range(spatial_filter.shape[0])], signal_mne.info['sfreq'], ch_types='eeg')
        ics_epoch = mne.EpochsArray(np.transpose(ics_epoch,axes=(2,0,1)),info_epochs)
        result = run_sl_channels(ics_epoch,passband=True)
        #sl:{}
        #cpot_d, cpot_t, cpot_a1, cpot_a2, cpot_b1, cpot_b2,cpot_b3, cpot_g
        return (result['sl']['delta'],result['sl']['theta'],result['sl']['alpha-1'],result['sl']['alpha-2'],result['sl']['beta1'],result['sl']['beta2'],result['sl']['beta3'],result['sl']['gamma'])
    else:
        return None

########################################### COHERENCE ####################################################
def get_coherence_derivates(signal):
    """
    signal: mne.Epochs object
    """
    # Channel Powers
    data = np.transpose(signal._data,(1,2,0))
    # powers_by_bands --> icpot_d, icpot_t, icpot_a1, icpot_a2, icpot_a, icpot_b, icpot_g
    channel_powers_by_band = run_coherence_channels(data,signal.info['sfreq'])
    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
    output_channels = {'channel_power' : channel_powers_by_band,
              'channels':signal.info['ch_names'],
              'bands':bands_labels}
    return output_channels
def get_ics_coherence_derivatives(signal,spatial_filter=None):
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

        ic_powers_by_band = run_power_ics(data_for_ics,W_adapted,signal.info['sfreq'])

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

def run_coherence_channels(signal,s_freq):
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
        cpot_d[chan], cpot_t[chan], cpot_a1[chan], cpot_a2[chan], cpot_b1[chan], cpot_b2[chan], cpot_b3[chan], cpot_g[chan] = qeeg_psd_chronux(signal[chan,:,:],s_freq)
    return cpot_d, cpot_t, cpot_a1, cpot_a2, cpot_b1, cpot_b2,cpot_b3, cpot_g

def run_coherence_ics(signal,spatial_filter,s_freq):
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
        result = run_power_channels(ics_epoch,s_freq)
        return result
    else:
        return None
########################################### ENTROPY ###################################################
def get_entropy_derivates(signal):
    """
    signal: mne.Epochs object
    """
    # Channel Powers
    data = np.transpose(signal._data,(1,2,0))
    # powers_by_bands --> icpot_d, icpot_t, icpot_a1, icpot_a2, icpot_a, icpot_b, icpot_g
    channel_powers_by_band = run_entropy_channels(data,signal.info['sfreq'])
    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
    output_channels = {'channel_power' : channel_powers_by_band,
              'channels':signal.info['ch_names'],
              'bands':bands_labels}
    return output_channels
def get_ics_entropy_derivatives(signal,spatial_filter=None):
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

        ic_powers_by_band = run_power_ics(data_for_ics,W_adapted,signal.info['sfreq'])

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

def run_entropy_channels(signal,s_freq):
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
        cpot_d[chan], cpot_t[chan], cpot_a1[chan], cpot_a2[chan], cpot_b1[chan], cpot_b2[chan], cpot_b3[chan], cpot_g[chan] = qeeg_psd_chronux(signal[chan,:,:],s_freq)
    return cpot_d, cpot_t, cpot_a1, cpot_a2, cpot_b1, cpot_b2,cpot_b3, cpot_g

def run_entropy_ics(signal,spatial_filter,s_freq):
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
        result = run_power_channels(ics_epoch,s_freq)
        return result
    else:
        return None
########################################### CROSS_FREQUENCY ###############################################
def get_cross_frequency_derivates(signal):
    """
    signal: mne.Epochs object
    """
    # Channel Powers
    data = np.transpose(signal._data,(1,2,0))
    # powers_by_bands --> icpot_d, icpot_t, icpot_a1, icpot_a2, icpot_a, icpot_b, icpot_g
    channel_powers_by_band = run_cross_frequency_channels(data,signal.info['sfreq'])
    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
    output_channels = {'channel_power' : channel_powers_by_band,
              'channels':signal.info['ch_names'],
              'bands':bands_labels}
    return output_channels
def get_ics_cross_frequency_derivatives(signal,spatial_filter=None):
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

        ic_powers_by_band = run_power_ics(data_for_ics,W_adapted,signal.info['sfreq'])

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

def run_cross_frequency_channels(signal,s_freq):
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
        cpot_d[chan], cpot_t[chan], cpot_a1[chan], cpot_a2[chan], cpot_b1[chan], cpot_b2[chan], cpot_b3[chan], cpot_g[chan] = qeeg_psd_chronux(signal[chan,:,:],s_freq)
    return cpot_d, cpot_t, cpot_a1, cpot_a2, cpot_b1, cpot_b2,cpot_b3, cpot_g

def run_cross_frequency_ics(signal,spatial_filter,s_freq):
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
        result = run_power_channels(ics_epoch,s_freq)
        return result
    else:
        return None