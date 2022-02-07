from re import I
from sovaflow.flow import single_flow
from sovaflow.utils import cfg_logger
import json
import os
import csv
from bids import BIDSLayout
import logging
from datetime import datetime
import numpy as np
#Inputs
input_path = r'Y:\datasets\CodificadoBIDSMini'
channels = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8', 'FC5', 'FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'FC6', 'T7', 'C5', 'C3', 'C1', 'CZ', 'C2', 'C4', 'C6', 'T8', 'TP7', 'CP5', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4', 'CP6', 'TP8', 'P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'O1', 'OZ', 'O2']
fast_mode = False

# Static Params
pipeline = 'sovaflow'
layout = BIDSLayout(input_path)
bids_root = layout.root
output_path = os.path.join(bids_root,'derivatives',pipeline)

eegs = layout.get(extension='.vhdr', task='CE',suffix='eeg', return_type='filename')
eegs += layout.get(extension='.vhdr', task='OE',suffix='eeg', return_type='filename')

derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
log_path = os.path.join(derivatives_root,'code')
os.makedirs(log_path, exist_ok=True)
logger,currentdt = cfg_logger(log_path)

def get_derivative_path(eeg_file,output_entity,suffix,output_extension,bids_root,derivatives_root):
    entities = layout.parse_file_entities(eeg_file)
    derivative_path = eeg_file.replace(bids_root,derivatives_root)
    derivative_path = derivative_path.replace(entities['extension'],'')
    derivative_path = derivative_path.split('_')
    desc = 'desc-' + output_entity
    derivative_path = derivative_path[:-1] + [desc] + [suffix]
    derivative_path = '_'.join(derivative_path) + output_extension 
    return derivative_path

def default(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))

def write_json(data,filepath):
    with open(filepath, 'w') as fp:
        json.dump(data, fp,indent=4,default=default)
e = 0
archivosconerror = []

description = layout.get_dataset_description()
desc_sovaflow = "sovaflow, an automatic resting-state eeg processing pipeline using: 1) Robust Reference (PREP); 2) High Pass 1Hz; 3) Wavelet ICA Denoising; 4) Low Pass 50Hz; 5) Epoch Auto Rejection; 6) Band Power Calculation"
description['GeneratedBy']=[{'Name':'sovaflow','Description':desc_sovaflow,'CodeURL':'https://github.com/GRUNECO/sovaflow'}]
write_json(description,os.path.join(derivatives_root,'dataset_description.json'))
num_files = len(eegs)
for i,eeg_file in enumerate(eegs):
    try:
        logger.info(f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}")
        power_path = get_derivative_path(eeg_file,'preprocessed','powers','.txt',bids_root,derivatives_root)
        prepoc_path = get_derivative_path(eeg_file,'preprocessed','eeg','.fif',bids_root,derivatives_root)
        stats_path = get_derivative_path(eeg_file,'preprocessed','stats','.txt',bids_root,derivatives_root)
        os.makedirs(os.path.split(power_path)[0], exist_ok=True)

        if os.path.isfile(power_path) and os.path.isfile(prepoc_path):
            logger.info(f'{power_path} and {prepoc_path} already existed, skipping...')
            continue

        power_dict,signal,stats=single_flow(eeg_file,correct_montage=channels,drop_channels=None,line_freqs=[60],fast_mode=fast_mode)
        
        write_json(power_dict,power_path)
        signal.save(prepoc_path ,split_naming='bids', overwrite=True)
        write_json(stats,stats_path)

        #Saving jsons

        json_dict = {"Description":desc_sovaflow,"RawSources":[eeg_file.replace(bids_root,'')]}
        write_json(json_dict,prepoc_path.replace('.fif','.json'))

        json_dict["Sources"]=prepoc_path.replace(bids_root,'')
        write_json(json_dict,power_path.replace('.txt','.json'))
        write_json(json_dict,stats_path.replace('.txt','.json'))

    except Exception as error:
        e+=1
        logger.exception(f'Error for {eeg_file}')
        archivosconerror.append(eeg_file)
        pass

print('end')