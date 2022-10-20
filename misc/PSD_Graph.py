from matplotlib.cbook import flatten
import numpy as np
import matplotlib.pyplot as plt
from regex import R
from sovaflow.flow import organize_channels
import mne
import copy
from sovaflow.utils import createRaw
from sovaharmony.postprocessing import get_spatial_filter,get_ics_power_derivatives
import scipy.signal as scsignal
from sovaflow.flow import fit_spatial_filter
from pandas.core.common import flatten
import os
from sovaharmony.datasets import BIOMARCADORES_CE as DATA    
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
    return signal_ics,ics

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
    return signal_ics,ics

def welch_pds(signal_wech,roi,comp=24,continuo=True):
    ch_roi_signal=ch_roi(roi,signal_wech)
    if continuo:
        ics_signal,ics=create_raw_ics(ch_roi_signal)
    else:
        ics_signal,ics=create_raw_ics_c(ch_roi_signal)
    
    ff, Pxx=scsignal.welch(ics_signal.get_data(), fs=signal_wech.info['sfreq'],nperseg=signal_wech.info['sfreq']*2, noverlap=signal_wech.info['sfreq']/2)
    ffcomp, Pxxcomp=scsignal.welch(ics[comp,:], fs=signal_wech.info['sfreq'],nperseg=signal_wech.info['sfreq']*2, noverlap=signal_wech.info['sfreq']/2)
    return ff, Pxx,ffcomp, Pxxcomp

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

def mean_sbj(all_mean):
    mean_sbj = []
    mean_mean = []
    for m in range(len(all_mean[0])):
        for s in range(len(all_mean)):
            mean_mean.append(all_mean[s][m])
        l=list(flatten(mean_mean))
        mean_sbj.append(np.mean(l))
        mean_mean = []
    return mean_sbj

THE_DATASET_=[DATA]
def BIDS_pds(THE_DATASET_):
    all_mean_raw = []
    all_mean_prep = []
    all_mean_wica = []
    all_mean_preprocessing = []
    all_mean_huber = []
    all_mean_trim = []
    all_mean_trim_nolp = []
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
            file_prep = get_derivative_path(layout,eeg_file,'prep','eeg','.fif',bids_root,derivatives_root)
            file_wica = get_derivative_path(layout,eeg_file,'wica','eeg','.fif',bids_root,derivatives_root)
            file_preprocessing = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
            file_huber = get_derivative_path(layout,eeg_file,'huber'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
            file_trim = get_derivative_path(layout,eeg_file,'trim'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
            file_trim_nolp = get_derivative_path(layout,eeg_file,'trim_nolp'+pipelabel,'eeg','.fif',bids_root,derivatives_root)

            raw = mne.io.read_raw(file_raw,preload=True)
            prep = mne.io.read_raw(file_prep, preload=True)
            wica = mne.io.read_raw(file_wica, preload=True)
            preprocessing = mne.read_epochs(file_preprocessing, verbose='error')
            huber = mne.read_epochs(file_huber, verbose='error')
            trim = mne.read_epochs(file_trim, verbose='error')
            trim_nolp = mne.read_epochs(file_trim_nolp, verbose='error')
            ch = ['P2','P4','P1','POZ','PO3','PO6','PO7','P7','PO5','O1','P3','P8','OZ','PZ','O2','PO4','PO8','P6','P5']

            ff_raw, Pxx_raw,ff_comp_raw,Pxx_comp_raw = welch_pds(raw,ch,continuo=False)
            ff_prep, Pxx_prep, ff_comp_prep, Pxx_comp_prep = welch_pds(prep,ch,continuo=False)
            ff_wica, Pxx_wica, ff_comp_wica, Pxx_comp_wica = welch_pds(wica,ch,continuo=False)
            ff_preprocessing, Pxx_preprocessing, ff_comp_preprocessing, Pxx_comp_preprocessing = welch_pds(preprocessing,ch)
            ff_huber, Pxx_huber,ff_comp_huber, Pxx_comp_huber = welch_pds(huber,ch)
            ff_trim, Pxx_trim,ff_comp_trim, Pxx_comp_trim = welch_pds(trim,ch)
            ff_trim_nolp, Pxx_trim_nolp,ff_comp_trim_nolp, Pxx_comp_trim_nolp = welch_pds(trim_nolp,ch)
            mean_raw = mean_Pxx_ff(ff_raw, Pxx_raw)
            mean_prep = mean_Pxx_ff(ff_prep, Pxx_prep)
            mean_wica = mean_Pxx_ff(ff_wica, Pxx_wica)
            mean_preprocessing = mean_Pxx_ff(ff_preprocessing, Pxx_preprocessing)
            mean_huber = mean_Pxx_ff(ff_huber, Pxx_huber)
            mean_trim = mean_Pxx_ff(ff_trim, Pxx_trim)
            mean_trim_nolp = mean_Pxx_ff(ff_trim_nolp, Pxx_trim_nolp)
        
            all_mean_raw.append(mean_raw)
            all_mean_prep.append(mean_prep)
            all_mean_wica.append(mean_wica)
            all_mean_preprocessing.append(mean_preprocessing)
            all_mean_huber.append(mean_huber)
            all_mean_trim.append(mean_trim)
            all_mean_trim_nolp.append(mean_trim_nolp)
        sbj_raw=mean_sbj(all_mean_raw)
        sbj_prep=mean_sbj(all_mean_prep)
        sbj_wica=mean_sbj(all_mean_wica)
        sbj_preprocessing=mean_sbj(all_mean_preprocessing)
        sbj_huber=mean_sbj(all_mean_huber)
        sbj_trim=mean_sbj(all_mean_trim)
        sbj_trim_nolp=mean_sbj(all_mean_trim_nolp)
        #ff_raw,sbj_raw,Pxx_comp_raw
        #ff_prep,sbj_prep,Pxx_comp_prep
        #ff_wica,sbj_wica,Pxx_comp_wica
        #ff_preprocessing,sbj_preprocessing,Pxx_comp_preprocessing
        #ff_huber,sbj_huber,Pxx_comp_huber
        #ff_trim,sbj_trim,Pxx_comp_trim
        #ff_trim_nolp,sbj_trim_nolp,Pxx_comp_trim_nolp
    return ff_raw,sbj_raw,Pxx_comp_raw,ff_prep,sbj_prep,Pxx_comp_prep,ff_wica,sbj_wica,Pxx_comp_wica,ff_preprocessing,sbj_preprocessing,Pxx_comp_preprocessing,ff_trim,sbj_trim,Pxx_comp_trim,ff_trim_nolp,sbj_trim_nolp,Pxx_comp_trim_nolp,ff_huber,sbj_huber,Pxx_comp_huber  
    
ff_raw,sbj_raw,Pxx_comp_raw,ff_prep,sbj_prep,Pxx_comp_prep,ff_wica,sbj_wica,Pxx_comp_wica,ff_preprocessing,sbj_preprocessing,Pxx_comp_preprocessing,ff_trim,sbj_trim,Pxx_comp_trim,ff_trim_nolp,sbj_trim_nolp,Pxx_comp_trim_nolp,ff_huber,sbj_huber,Pxx_comp_huber = BIDS_pds(THE_DATASET_)  

f, (ax1,ax2,ax3,ax4,ax5,ax6,ax7) = plt.subplots(5, 1,sharex=True, sharey=False)
ax1.set_title('Original')
ax1.plot(ff_raw,sbj_raw,color='k')
ax2.set_title('Preprocessing')
ax2.plot(ff_prep,sbj_prep,color='k')
ax3.set_title('Wica')
ax3.plot(ff_wica,sbj_wica,color='k')
ax4.set_title('Processing')
ax4.plot(ff_preprocessing,sbj_preprocessing,color='k')
ax5.set_title('Normalized Trim Mean')
ax5.plot(ff_trim,sbj_trim,color='k')
ax6.set_title('Normalized Huber')
ax6.plot(ff_huber,sbj_huber,color='k')
ax7.set_title('Normalized Trim Mean no lp')
ax7.plot(ff_trim_nolp,sbj_trim_nolp,color='k')
#plt.legend([ax1, ax2, ax3],["Original", "Preprocessing", "Normalizate"])
#plt.yscale('log')
#plt.ylim((pow(10,-18),pow(10,-4)) )
#plt.yticks(color='w') 
ax1.set_xlim(0,60)
plt.xlabel('Frequency [Hz]')
#plt.ylabel('Absolute power')
plt.show()

f, (ax1,ax2,ax3,ax4,ax5,ax6,ax7) = plt.subplots(5, 1,sharex=True, sharey=False)
ax1.set_title('Original')
ax1.plot(ff_raw,Pxx_comp_raw,color='k')
ax2.set_title('Preprocessing')
ax2.plot(ff_prep,Pxx_comp_prep,color='k')
ax3.set_title('Wica')
ax3.plot(ff_wica,Pxx_comp_wica,color='k')
ax4.set_title('Processing')
ax4.plot(ff_preprocessing,Pxx_comp_preprocessing,color='k')
ax5.set_title('Normalized Trim Mean')
ax5.plot(ff_trim,Pxx_comp_trim,color='k')
ax6.set_title('Normalized Huber')
ax6.plot(ff_huber,Pxx_comp_huber,color='k')
ax7.set_title('Normalized Trim Mean no lp')
ax7.plot(ff_trim_nolp,Pxx_comp_trim_nolp,color='k')
#plt.legend([ax1, ax2, ax3],["Original", "Preprocessing", "Normalizate"])
#plt.yscale('log')
#plt.ylim((pow(10,-18),pow(10,-4)) )
#plt.yticks(color='w') 
ax1.set_xlim(0,60)
plt.xlabel('Frequency [Hz]')
#plt.ylabel('Absolute power')
plt.show()


#for m,p,n in zip(all_mean_raw,all_mean_preprocessing,all_mean_norm):

#plt.plot(ff_raw,all_mean_raw,color='c')
#plt.plot(ff_preprocessing,all_mean_preprocessing,color='m')
#plt.plot(ff_norm,all_mean_norm,color='g')
#plt.yscale('log')
#plt.ylim((pow(10,-18),pow(10,-4)) )
#plt.xlim(1,60)
#plt.xlabel('Frequency [Hz]')
#plt.ylabel('Absolute power')
#plt.yticks(color='w')
#plt.legend(['Original','Preprocessing','Normalizate'])
#plt.show()
#for m in all_mean_preprocessing:
#    plt.plot(ff_preprocessing,m,color='m')
#    plt.xlim(1,60)
#plt.show()
#for m in all_mean_norm:
#plt.plot(ff_norm,all_mean_norm,color='g')
#plt.xlim(1,60)
#plt.legend(['Normalizate'])
#plt.show()

#f, (ax1, ax2,ax3) = plt.subplots(3, 1,sharex=True, sharey=False)
#ax1.plot(ff_raw,mean_raw,color='c')
#ax2.plot(ff_preprocessing,mean_preprocessing,color='m')
#ax3.plot(ff_norm,mean_norm,color='g')
#ax1.set_xlim(3,30)
#ax1.set_title('Original')
#ax2.set_title('Preprocessing')
#ax3.set_title('Normalizate')
