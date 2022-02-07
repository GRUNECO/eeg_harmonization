from re import I
from sovaflow.flow import single_flow
import json
import os
import csv
from bids import BIDSLayout
import logging
from datetime import datetime

def cfg_logger(log_path):
    """Configures the logger of the pipeline.
    Parameters
    ----------
    log_path : string
        Directory of the log file without filename.
    Returns
    -------
    dalogger : logging.Logger instance
        The logger object to be used by the pipeline.
    currentDT : instance of datetime.datetime
        The current date and time.
    Examples
    --------
    >>> log, date = cfg_logger(log_path)
    """
    for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
    currentDT = datetime.now()
    currentDT.strftime("%Y-%m-%d %H:%M:%S")
    log_name = os.path.join(log_path, 'sovaflow__' + currentDT.strftime("%Y-%m-%d__%H_%M_%S") + '.log')
    logging.basicConfig(filename= log_name, level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    dalogger=logging.getLogger(__name__)
    return dalogger, currentDT

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

def get_derivative_path(eeg_file,output_entity,output_extension,bids_root,derivatives_root):
    entities = layout.parse_file_entities(eeg_file)
    derivative_path = eeg_file.replace(bids_root,derivatives_root)
    derivative_path = derivative_path.replace(entities['extension'],'')
    derivative_path = derivative_path.split('_')
    desc = 'desc-' + output_entity
    derivative_path = derivative_path[:-1] + [desc] + [derivative_path[-1]]
    derivative_path = '_'.join(derivative_path) + output_extension 
    return derivative_path

e = 0
archivosconerror = []

for eeg_file in eegs:
    try:

        power_path = get_derivative_path(eeg_file,'power','.json',bids_root,derivatives_root)
        prepoc_path = get_derivative_path(eeg_file,'preprocessed','.fif',bids_root,derivatives_root)
        os.makedirs(os.path.split(power_path)[0], exist_ok=True)

        if os.path.isfile(power_path) and os.path.isfile(prepoc_path):
            logger.info(f'{power_path} and {prepoc_path} already existed, skipping...')
            continue

        power_dict,signal=single_flow(eeg_file,correct_montage=channels,drop_channels=None,line_freqs=[60],fast_mode=fast_mode)
        
        with open(power_path, 'w') as fp:
            json.dump(power_dict, fp)
        signal.save(prepoc_path ,split_naming='bids', overwrite=True)
    except Exception as error:
        e+=1
        logger.exception(f'Error for {eeg_file}')
        archivosconerror.append(eeg_file)
        pass

print('end')