from sovaharmony.coh import get_coherence
from sovaharmony.sl import get_sl_1band
from sovaharmony.p_entropy import get_entropy_freq
#from sovaharmony.pme import get_pme_freq
#from sovaharmony.pme import Modulation_Bands_Decomposition,Modulation_Bands_Spectrum,Modulation_Bands_Decomposition_Hamming
from sovaharmony.pme import Amplitude_Modulation_Analysis
import numpy as np
from sovaflow.flow import fit_spatial_filter
from sovaflow.utils import createRaw
from sovachronux.qeeg_psd_chronux import qeeg_psd_chronux
from sovaharmony.utils import _verify_epoch_continuous,_verify_epochs_axes
import mne

## USE PYTHON >3.7 , fundamental to guarantee dict order

# each metric has an internal function that is executed internally in get_derivative
# that function should receive signal (mne.Epochs) and kwargs, its arguments
#_get_[derivative_name]

### INTERNAL FEATURES FUNCTIONS ###
def _get_power(signal_epoch,bands):
    signal = np.transpose(signal_epoch.get_data(),(1,2,0)) # epochs spaces times -> spaces times epochs
    _verify_epochs_axes(signal_epoch.get_data(),signal)
    space_names = signal_epoch.info['ch_names']
    spaces,times,epochs = signal.shape
    output = {}
    output['metadata'] = {'type':'power','kwargs':{'bands':bands}}
    bands_list = list(bands.keys())
    values = np.empty((len(bands_list),spaces))
    output['metadata']['axes']={'bands':bands_list,'spaces':space_names}
    for space in space_names:
        space_idx = space_names.index(space)
        dummy = qeeg_psd_chronux(signal[space_idx,:,:],signal_epoch.info['sfreq'],bands)
        for b in bands.keys():
            band_idx = bands_list.index(b)
            values[band_idx,space_idx]=dummy[b]
    output['values'] = values
    return output

def _get_sl(signal_epoch,bands):
    space_names = signal_epoch.info['ch_names']
    epochs,spaces,times = signal_epoch.get_data().shape

    output = {}
    output['metadata'] = {'type':'sl','kwargs':{'bands':bands}}

    bands_list = list(bands.keys())
    values = np.empty((len(bands_list),spaces,spaces))
    output['metadata']['axes']={'bands':bands_list,'spaces1':space_names,'spaces2':space_names}

    for b,brange in bands.items():
        dummy = get_sl_1band(signal_epoch,brange[0],brange[1])
        band_idx = bands_list.index(b)
        values[band_idx,:,:]=dummy
    output['values'] = values
    return output

def _get_coh(signal_epoch,window,bands):
    chs = signal_epoch.info['ch_names']
    blist=list(bands.keys())
    _,Cfxy = get_coherence(signal_epoch,bands,signal_epoch.info['sfreq'],window)
    axes = {'bands':blist,'spaces1':chs,'spaces2':chs}
    output = {}
    dim0 = list(axes.keys())[0]
    output['metadata'] = {'type':f'coherence-{dim0}','kwargs':{'window':window,'bands':bands}}
    output['metadata']['axes']=axes
    output['values']=Cfxy
    return output

def _get_pme(signal_epoch,bands):
    signal = np.transpose(signal_epoch.get_data(),(1,2,0)) # epochs spaces times -> spaces times epochs
    _verify_epochs_axes(signal_epoch.get_data(),signal)
    space_names = signal_epoch.info['ch_names']
    spaces,times,epochs = signal.shape
    output = {}
    output['metadata'] = {'type':'crossfreq','kwargs':{'bands':bands}}
    bands_list = list(bands.keys())
    values = np.empty((len(bands_list),spaces))
    output['metadata']['axes']={'spaces':space_names,'bands':bands_list,'bands':bands_list}

    values = Amplitude_Modulation_Analysis(signal,signal_epoch.info['sfreq'],Bands=list(bands.values()))
    output['values'] = values
    return output

def _get_entropy(signal_epoch,bands,D):
    space_names = signal_epoch.info['ch_names']
    epochs,spaces,times = signal_epoch.get_data().shape

    output = {}
    output['metadata'] = {'type':'entropy','kwargs':{'bands':bands,'D':D}}

    bands_list = list(bands.keys())
    values = np.empty((len(bands_list),spaces))
    output['metadata']['axes']={'bands':bands_list,'spaces':space_names}

    for b,brange in bands.items():
        fmin,fmax=brange
        dummy = get_entropy_freq(signal_epoch,fmin=fmin,fmax=fmax,D=D)
        band_idx = bands_list.index(b)
        values[band_idx,:]=dummy
    output['values'] = values
    return output

#### generalizado#######

foo_map={
    'power':_get_power,
    'sl':_get_sl,
    'cohfreq':_get_coh,
    'crossfreq':_get_pme,
    'entropy':_get_entropy
}
def get_derivative(in_signal,feature,kwargs,spatial_filter=None):
    """
    Returns derivative
    If spatial_filter is not None, it will be computed over ics, otherwise over channels

    signal: mne.Epochs object
    feature: str, the feature you want
    kwargs: arguments for the fuction that calculates that feature
    spatial_filter: tuple (A,W,spatial_filter_chs)
    """
    signal = in_signal.copy()
    if spatial_filter is not None:
        # ICs powers
        A,W,spatial_filter_chs,sf_name = spatial_filter['A'],spatial_filter['W'],spatial_filter['ch_names'],spatial_filter['name']
        intersection_chs = list(set(spatial_filter_chs).intersection(signal.ch_names))
        W_adapted = fit_spatial_filter(W,spatial_filter_chs,intersection_chs,mode='demixing')
        signal.reorder_channels(intersection_chs)
        signal2 = np.transpose(signal.get_data(),(1,2,0)) # epochs spaces times -> spaces times epochs
        _verify_epochs_axes(signal.get_data(),signal2)
        nchans,points,epochs = signal2.shape
        signalCont = np.reshape(signal2,(nchans,points*epochs),order='F')
        _verify_epoch_continuous(signal.get_data(),signalCont,('epochs','spaces','times'))
        ics = W_adapted @ signalCont
        comps = ics.shape[0]
        ics_epoch = np.reshape(ics,(comps,points,epochs),order='F')
        _verify_epoch_continuous(ics_epoch,ics,('spaces','times','epochs'))
        ics_epoch2 = np.transpose(ics_epoch,(2,0,1))
        _verify_epochs_axes(ics_epoch2,ics_epoch)
        del ics_epoch
        del ics
        del signalCont
        del signal2
        info_epochs=mne.create_info(['C'+str(x) for x in range(comps)], in_signal.info['sfreq'], ch_types='eeg')
        signal = mne.EpochsArray(ics_epoch2,info_epochs)
    output=foo_map[feature](signal,**kwargs)

    if spatial_filter is not None:
        output['metadata']['space']='ics'
        output['metadata']['W'] = W_adapted
        output['metadata']['W_channels']=intersection_chs
        output['metadata']['spatial_filter_name']=sf_name
    else:
        output['metadata']['space']='sensors'
    return output
    