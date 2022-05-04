import mne
from regex import E
import statsmodels.api as sm
from sovaharmony.processing import get_derivative_path, write_json
from bids import BIDSLayout
from datasets import BIOMARCADORES 
import os
import numpy as np
from sovaflow.utils import createRaw
from sovaflow.flow import  get_power_derivates
from astropy.stats import mad_std
import matplotlib.pyplot as plt
import seaborn as sns

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
    json_dict = {"Description":desc_pipeline,"RawSources":[eeg_file.replace(bids_root,'')],"Configuration":THE_DATASET}
    power_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'_norm_powers','.txt',bids_root,derivatives_root)
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
    signal_norm = signal/k[0]

    power_norm = get_power_derivates(signal_norm)
    write_json(power_norm,power_norm_path)
    write_json(json_dict,power_norm.replace('.txt','.json'))
    print('listo')
    


