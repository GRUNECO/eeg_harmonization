import mne
from regex import E
import statsmodels.api as sm
from sovaharmony.processing import get_derivative_path, write_json
from bids import BIDSLayout
from datasets import BIOMARCADORES 
import os
import numpy as np
from sovaflow.utils import createRaw
from sovaflow.flow import  get_power_derivates, crop_raw_data, make_fixed_length_epochs
from astropy.stats import mad_std
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

THE_DATASET=BIOMARCADORES
layout_dict = THE_DATASET.get('layout',None)
input_path = THE_DATASET.get('input_path',None)
layout = BIDSLayout(input_path)
eegs = layout.get(**layout_dict)
pipelabel = '['+THE_DATASET.get('run-label', '')+']'
bids_root = layout.root
pipeline = 'sovaharmony'
derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
desc_pipeline = "sovaharmony, a harmonization eeg pipeline using the bids standard"


for i,eeg_file in enumerate(eegs):
    power_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'_norm_powers','.txt',bids_root,derivatives_root)
    norm_path = get_derivative_path(layout,eeg_file,'norm','eeg','.fif',bids_root,derivatives_root)
    json_dict = {"Description":desc_pipeline,"RawSources":[eeg_file.replace(bids_root,'')],"Configuration":THE_DATASET}
    json_dict["Sources"]=norm_path.replace(bids_root,'')
    reject_path = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
    signal = mne.read_epochs(reject_path)
    signal_hp = signal.filter(None,20,fir_design='firwin')
    (e, c, t) = signal_hp._data.shape
    da_eeg_cont = np.reshape(signal_hp,(c,e*t),order='F')
    signal_ch = createRaw(da_eeg_cont,signal_hp.info['sfreq'],ch_names=signal_hp.info['ch_names'])
    std_ch = []
    for ch in signal_ch._data:
        std_ch.append(mad_std(ch))
    
    k = sm.robust.scale.huber(np.array(std_ch))
    signal_norm = signal._data/k[0]
    
    signal_nn = np.resize(signal_norm,(c,e,t))
    (c, e, t) = signal_nn.shape
    signal_norm = np.reshape(signal_nn,(c,e*t),order='F')
    signal_norma = createRaw(signal_norm,signal.info['sfreq'],ch_names=signal.info['ch_names'])
    
    
    if THE_DATASET.get('events_to_keep', None) is not None:
        events_file = os.path.splitext(eeg_file)[0].replace('_eeg','_events.tsv')
        events_raw=pd.read_csv(events_file,sep='\t')
        samples = events_raw['sample'].tolist()
        values = events_raw['value'].tolist()
        events = list(zip(values,samples))
        events_to_keep = THE_DATASET.get('events_to_keep', None)
    else:
        events = None
        events_to_keep = None
    
    signal_n = crop_raw_data(signal_norma,events, events_to_keep)
    raw_norm = make_fixed_length_epochs(signal_n,duration=e/signal.info['sfreq'],reject_by_annotation=False,preload=True) 
    raw_norm.save(norm_path ,split_naming='bids', overwrite=True)
    write_json(json_dict,norm_path.replace('.fif','.json'))

    #signal_n = mne.io.read_raw(norm_path,preload=True)
    signal_normas = mne.read_epochs(norm_path)
    signal_up = np.resize(signal_normas,(c,e,t))
    (c, e, t) = signal_up.shape
    signal_norm_up = np.reshape(signal_up,(c,e*t),order='F')
    signal_norma_up = createRaw(signal_norm_up,signal.info['sfreq'],ch_names=signal.info['ch_names'])

    power_norm = get_power_derivates(signal_norma_up)
    
    
    
    write_json(power_norm,power_norm_path)
    write_json(json_dict,power_norm_path.replace('.txt','.json'))

    


