import mne
from datasets import LEMON as THE_DATASET
import pandas as pd
from mne.io import read_raw
import mne 
import pandas as pd
import numpy as np

def crop_raw_data(path_events,path_eeg,marks_rest):
    events_raw=pd.read_csv(path_events,sep='\t')
    eeg_raw = read_raw(path_eeg)
    raw_final = []
    fs = eeg_raw.info['sfreq']
    for i in range(0,len(events_raw['value'])):
        if events_raw['value'][i] == marks_rest:
            a = events_raw['sample'][i]
            s = events_raw['sample'][i+1]
            new_raw =eeg_raw.get_data()[:,a:s]
            
            raw_final.append(new_raw)
    raw_all = np.concatenate((raw_final),axis=1)
    raw = mne.io.RawArray(raw_all, eeg_raw.info)
    return raw

path_events = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\ds_bids_chbmp\sub-CBM00001\eeg\sub-CBM00001_task-protmap_events.tsv"
path_eeg = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\ds_bids_chbmp\sub-CBM00001\eeg\sub-CBM00001_task-protmap_eeg.edf"
marks_rest = 65
raw=crop_raw_data(path_events,path_eeg,marks_rest)
print(raw)
