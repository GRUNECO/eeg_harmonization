import mne
import statsmodels.api as sm
from sovaharmony.processing import get_derivative_path, write_json
from bids import BIDSLayout
from datasets import BIOMARCADORES
import os
import numpy as np
import pandas as pd
from sovaflow.utils import createRaw
from sovaflow.flow import  get_power_derivates,get_ics_power_derivatives
from astropy.stats import mad_std
from sovaflow.utils import cfg_logger,get_spatial_filter

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
def_spatial_filter='58x25'
spatial_filter = get_spatial_filter(THE_DATASET.get('spatial_filter',def_spatial_filter))
default_channels = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8', 'FC5', 'FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'FC6', 'T7', 'C5', 'C3', 'C1', 'CZ', 'C2', 'C4', 'C6', 'T8', 'TP7', 'CP5', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4', 'CP6', 'TP8', 'P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'O1', 'OZ', 'O2']
channels = THE_DATASET.get('channels',default_channels)

lista_signal=[]
lista_signal2=[]
path=[]

for i,eeg_file in enumerate(eegs):
    power_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'powers_norm','.txt',bids_root,derivatives_root)
    norm_path = get_derivative_path(layout,eeg_file,'norm','eeg','.fif',bids_root,derivatives_root)
    icpowers_norm_path = get_derivative_path(layout,eeg_file,'component'+pipelabel,'_norm_powers','.txt',bids_root,derivatives_root)
    json_dict = {"Description":desc_pipeline,"RawSources":[eeg_file.replace(bids_root,'')],"Configuration":THE_DATASET}
    json_dict["Sources"]=norm_path.replace(bids_root,'')
    reject_path = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
    signal = mne.read_epochs(reject_path)
    signal2=signal.copy()
    signal_hp = signal.filter(None,20,fir_design='firwin')
    (e, c, t) = signal_hp._data.shape
    da_eeg_cont = np.reshape(signal_hp,(c,e*t),order='F')
    signal_ch = createRaw(da_eeg_cont,signal_hp.info['sfreq'],ch_names=channels)
    std_ch = []
    for ch in signal_ch._data:
        std_ch.append(mad_std(ch))

    huber = sm.robust.scale.Huber()
    cont = 0
    try:
        k = huber(np.array(std_ch))[0]
    except:
        print(reject_path,':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
    #     lista.append(reject_path)
    #     # Revisar porque hicimos esto
    #     k = np.median(np.array(std_ch))
        cont+=1   
             
    
    # derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    # log_path = os.path.join(derivatives_root,'code')
    # os.makedirs(log_path, exist_ok=True)
    # logger,currentdt = cfg_logger(log_path)

    #if os.path.isfile(norm_path):
    #   logger.info(f'{norm_path}) already existed, skipping...')
    #else:
    signal2._data=signal2._data/k
    lista_signal.append(len(signal))
    lista_signal2.append(len(signal2))
    path.append(reject_path)

    # signal2.save(norm_path ,split_naming='bids', overwrite=True)
    # # write_json(json_dict,norm_path.replace('.fif','.json'))

    # signal_normas = mne.read_epochs(norm_path)
    # power_norm = get_power_derivates(signal_normas)
                    
    # # write_json(power_norm,power_norm_path)
    # # write_json(json_dict,power_norm_path.replace('.txt','.json'))
    # ic_powers_dict = get_ics_power_derivatives(signal2,spatial_filter)
    # write_json(ic_powers_dict,icpowers_norm_path)
    # write_json(json_dict,icpowers_norm_path.replace('.txt','.json'))


#    if not os.path.isfile(icpowers_norm_path) and spatial_filter is not None:
#        ic_powers_dict = get_ics_power_derivatives(signal2,spatial_filter)
#        write_json(ic_powers_dict,icpowers_norm_path)
#        write_json(json_dict,icpowers_norm_path.replace('.txt','.json'))
#    else:
#        logger.info(f'{icpowers_norm_path}) already existed or no spatial filter given, skipping...')

print(cont,':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
reject=pd.DataFrame()
reject['signal']=lista_signal
reject['signal_2']=lista_signal2
reject['path']=path
reject.to_csv('Reject.csv')

    


