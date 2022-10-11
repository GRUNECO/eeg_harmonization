from matplotlib.cbook import flatten
import numpy as np
import matplotlib.pyplot as plt
from regex import R
from sovaflow.flow import organize_channels
import mne
import copy
from sovaflow.utils import createRaw
from sovaharmony.postprocessing import get_spatial_filter,get_ics_power_derivatives
import scipy.signal as signal
from sovaflow.flow import fit_spatial_filter
from pandas.core.common import flatten
import os
from datasets import BIOMARCADORESMini as DATA    
import time 
from bids import BIDSLayout
from sovaharmony.get_conectivity import get_conectivity_band
from sovaharmony.sl import get_sl_freq
from sovaharmony.coh import get_coherence_freq
from sovaharmony.p_entropy import get_entropy_freq
#from sovaharmony.pme import get_pme_freq
from sovaflow.utils import cfg_logger
from sovaharmony.processing import get_derivative_path
from sovaharmony.processing import write_json
from bids import BIDSLayout
import mne
import json
import os
from sovaflow.flow import get_ics_power_derivatives
from sovaflow.flow import get_power_derivates
from sovaflow.utils import get_spatial_filter
import numpy as np

def ch_roi(ch,raw):
    correct_montage = copy.deepcopy(ch)
    raw = raw.copy() 
    raw,correct_montage= organize_channels(raw,correct_montage)
    return raw

def create_raw_ics(raw_epo):
    def_spatial_filter='58x25'
    spatial_filter = get_spatial_filter(def_spatial_filter)
    signal_epo = raw_epo.copy()
    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
    A,W,spatial_filter_chs = spatial_filter
    intersection_chs = list(set(spatial_filter_chs).intersection(signal_epo.ch_names))
    W_adapted = fit_spatial_filter(W,spatial_filter_chs,intersection_chs,mode='demixing')
    signal_epo.reorder_channels(intersection_chs)
    (e, c, t) = signal_epo._data.shape
    signalCont = np.reshape(np.transpose(signal_epo.get_data(),(1,2,0)),(c,t*e),order='F')
    ics = W_adapted @ signalCont
    for e in range(signal_epo._data.shape[0]):
        for c in range(signal_epo._data.shape[1]):
            assert np.all(signal_epo._data[e,c,:] == signalCont[c,e*t:(e+1)*t])
    signal_ics = createRaw(ics,signal_epo.info['sfreq']) 
    return signal_ics

def create_raw_ics_c(raw_epo):
    def_spatial_filter='58x25'
    spatial_filter = get_spatial_filter(def_spatial_filter)
    signal_epo = raw_epo.copy()
    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
    A,W,spatial_filter_chs = spatial_filter
    intersection_chs = list(set(spatial_filter_chs).intersection(signal_epo.ch_names))
    W_adapted = fit_spatial_filter(W,spatial_filter_chs,intersection_chs,mode='demixing')
    signal_epo.reorder_channels(intersection_chs)
    ics = W_adapted @ signal_epo.get_data()
    signal_ics = createRaw(ics,signal_epo.info['sfreq']) 
    return signal_ics

def welch_pds(signal,roi,continuo=True):
    ch_roi_signal=ch_roi(roi,signal)
    if continuo:
        ics_signal=create_raw_ics(ch_roi_signal)
    else:
        ics_signal=create_raw_ics_c(ch_roi_signal)
    
    ff, Pxx=signal.welch(ics_signal.get_data(), fs=signal.info['sfreq'],nperseg=signal.info['sfreq']*2, noverlap=signal.info['sfreq']/2)
    return ff, Pxx

def mean_Pxx_ff(ff,Pxx):
    mean_end = []
    mean_Pxx = []
    for Fr in range(len(ff)):
        for Px in range(len(Pxx)):
            mean_Pxx.append(Pxx[Px][Fr])
        l=list(flatten(mean_Pxx))
        mean_end.append(np.mean(l))
        mean_Pxx = []
    return mean_end

THE_DATASET_=[DATA]
for THE_DATASET in THE_DATASET_:
    input_path = THE_DATASET.get('input_path',None)
    layout_dict = THE_DATASET.get('layout',None)
    e = 0
    archivosconerror = []
    # Static Params
    pipelabel = '['+THE_DATASET.get('run-label', '')+']'
    layout = BIDSLayout(input_path)
    bids_root = layout.root
    eegs = layout.get(**layout_dict)
    pipeline = 'sovaharmony'
    derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    log_path = os.path.join(derivatives_root,'code')
    os.makedirs(log_path, exist_ok=True)
    for i,eeg_file in enumerate(eegs):
        file_raw = eeg_file
        file_preprocessing = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
        file_norm = get_derivative_path(layout,eeg_file,'norm','eeg','.fif',bids_root,derivatives_root)

        raw = mne.io.read_raw(file_raw,preload=True)
        #mne.io.read_raw_brainvision(file_raw + '.vhdr', verbose='error')
        preprocessing = mne.read_epochs(file_preprocessing, verbose='error')
        norm = mne.read_epochs(file_norm, verbose='error')
        ch = ['P2','P4','P1','POZ','PO3','PO6','PO7','P7','PO5','O1','P3','P8','OZ','PZ','O2','PO4','PO8','P6','P5']

        #ff_raw, Pxx_raw = welch_pds(raw,ch,continuo=False)
        ff_preprocessing, Pxx_preprocessing = welch_pds(preprocessing.get_data(),ch)
        ff_norm, Pxx_norm = welch_pds(norm,ch)
        #mean_raw = mean_Pxx_ff(ff_raw, Pxx_raw)
        mean_preprocessing = mean_Pxx_ff(ff_preprocessing, Pxx_preprocessing)
        mean_norm = mean_Pxx_ff(ff_norm, Pxx_norm)

    f, (ax1, ax2,ax3) = plt.subplots(3, 1,sharex=True, sharey=False)
    ax1.set_title('Original')
    #ax1.plot(ff_raw,mean_raw,color='c')
    ax2.set_title('Preprocessing')
    ax2.plot(ff_preprocessing,mean_preprocessing,color='m')
    ax3.set_title('Normalizate')
    ax3.plot(ff_norm,mean_norm,color='g')
    ax1.set_xlim(3,30)
    plt.show()