from sovaharmony.spatial import get_spatial_filter
from bids import BIDSLayout
from sovaharmony.preprocessing import get_derivative_path
from sovaflow.utils import cfg_logger
import os
import mne
from datasets import test_portables
from sovaflow.utils import createRaw
import numpy as np
from preprocessing import write_json

THE_DATASET=test_portables
def_spatial_filter='54x10'
bands ={'delta':(1.5,6),
        'theta':(6,8.5),
        'alpha-1':(8.5,10.5),
        'alpha-2':(10.5,12.5),
        'beta1':(12.5,18.5),
        'beta2':(18.5,21),
        'beta3':(21,30),
        'gamma':(30,45)
        }
channels_reduction={'cresta':['F3 ','F4 ','C3 ','C4 ','P3 ','P4 ','O1 ','O2 '],
                    'openBCI':['F3 ','F4 ','P3 ','P4 ','T5 ','O1 ','O2 ','T6 '],
                    'paper':['F3 ','F4 ','C3 ','C4 ','T3 ','T4 ','O1 ','O2 ']}
#Quantitative electroencephalography in mild cognitive impairment:
#longitudinal changes and possible prediction of Alzheimer’s disease

if THE_DATASET.get('spatial_filter',def_spatial_filter):
    spatial_filter = get_spatial_filter(THE_DATASET.get('spatial_filter',def_spatial_filter))
index_ch_portables=[spatial_filter['ch_names'].index(channels_reduction['cresta'][i]) for i in range(len(channels_reduction['cresta']))] 
comp_select=[0,1,2,3,4,6,7,9]# Delete components no neurals
spatial_filter_reduction=spatial_filter['A'][index_ch_portables,:] # Select channels, rows
spatial_filter_reduction=spatial_filter_reduction[:,[comp_select]] # Select components, columns
spatial_filter_reduction=np.squeeze(spatial_filter_reduction)

layout_dict = THE_DATASET.get('layout',None)
input_path = THE_DATASET.get('input_path',None)
layout = BIDSLayout(input_path)
pipeline = 'sovaharmony'
derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
log_path = os.path.join(derivatives_root,'code')
logger,currentdt = cfg_logger(log_path)
eegs = layout.get(**layout_dict)
num_files = len(eegs)
pipelabel = '['+THE_DATASET.get('run-label', '')+']'
bids_root = layout.root
desc_pipeline = "sovaharmony, a harmonization eeg pipeline using the bids standard"

for i,eeg_file in enumerate(eegs):
    msg =f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}"
    logger.info(msg)
    

    reject_path = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
    reduce_path = get_derivative_path(layout,eeg_file,'reduce'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
    signal = mne.read_epochs(reject_path)
    (e, c, t) = signal._data.shape
    signal_data = signal.get_data()
    da_eeg_cont = np.concatenate(signal_data,axis=-1)
    
    for e in range(signal_data.shape[0]):
        for c in range(signal_data.shape[1]):
            assert np.all(signal_data[e,c,:] == da_eeg_cont[c,e*t:(e+1)*t])
    da_eeg_cont=da_eeg_cont[index_ch_portables,:] 
    signal_ch = createRaw(da_eeg_cont,signal.info['sfreq'],ch_names=channels_reduction['cresta']) # 8xpuntos
    resample= signal_ch.info['sfreq']/4 
    signal_resample=signal_ch.get_data()[:,::4] # Signal chx resample
    S=np.dot((spatial_filter_reduction.T),signal_resample)
    matrix_S = createRaw(S,signal.info['sfreq'],ch_names=channels_reduction['cresta']) # 8xpuntos

    matrix_S.save(reduce_path ,split_naming='bids', overwrite=True)
    
    json_dict = {"Description":desc_pipeline,"RawSources":[eeg_file.replace(bids_root,'')],"Configuration":THE_DATASET}
    json_dict["Sources"]=reduce_path.replace(bids_root,'')
    write_json(json_dict,reduce_path.replace('.fif','.json'))
        
    #signal_ch = createRaw(signal_data,signal_data.info['sfreq'],ch_names=signal_data.info['ch_names']) #Fro SRM signal_lp.info['ch_names']
    #print(signal)