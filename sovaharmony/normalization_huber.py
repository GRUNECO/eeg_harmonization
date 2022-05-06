import mne
from regex import E
import statsmodels.api as sm
from sovaharmony.processing import get_derivative_path, write_json
from bids import BIDSLayout
from datasets import BIOMARCADORES 
import os
import numpy as np
from sovaflow.utils import createRaw
from sovaflow.flow import  get_power_derivates, crop_raw_data, make_fixed_length_epochs, run_power_channels
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
    signal2=signal.copy()
    signal_hp = signal.filter(None,20,fir_design='firwin')
    (e, c, t) = signal_hp._data.shape
    da_eeg_cont = np.reshape(signal_hp,(c,e*t),order='F')
    signal_ch = createRaw(da_eeg_cont,signal_hp.info['sfreq'],ch_names=signal_hp.info['ch_names'])
    std_ch = []
    for ch in signal_ch._data:
        std_ch.append(mad_std(ch))
    
    k = sm.robust.scale.huber(np.array(std_ch))
    signal2._data=signal._data/k[0]
    signal2.save(norm_path ,split_naming='bids', overwrite=True)
    write_json(json_dict,norm_path.replace('.fif','.json'))

    #signal_n = mne.io.read_raw(norm_path,preload=True)
    signal_normas = mne.read_epochs(norm_path)
    power_norm = get_power_derivates(signal_normas)
    
    
    
    write_json(power_norm,power_norm_path)
    write_json(json_dict,power_norm_path.replace('.txt','.json'))

    print('listo')

    


