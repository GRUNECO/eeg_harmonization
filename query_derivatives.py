
import json
from bids import BIDSLayout
import numpy as np
data_path = r'Y:\datasets\CodificadoBIDSMini'
layout = BIDSLayout(data_path,derivatives=True)
layout.get(scope='derivatives', return_type='file')
import pandas as pd
eegs_powers = layout.get(extension='.txt', task='CE',suffix='powers', return_type='filename')
eegs_powers += layout.get(extension='.txt', task='OE',suffix='powers', return_type='filename')

F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
rois = [F,C,PO,T]
roi_labels = ['F','C','PO','T']

for i in range(len(eegs_powers)):
    with open(eegs_powers[i], 'r') as f:
        data = json.load(f)
    print(None)
    channels=np.array(data['channels'])
    bandas = data['bands']
    new_rois = []
    potencias_roi_banda=[]

    for roi in rois:
        channels = set(data['channels']).intersection(roi)
        new_roi = []
        for channel in channels:
            i=data['channels'].index(channel)
            new_roi.append(i)
        new_rois.append(new_roi)

    datos_1_sujeto = {}
    for b,band in enumerate(bandas):
        for r,roi in enumerate(new_rois):
            potencia_promedio = np.average(np.array(data['channel_power'])[b,roi])
            datos_1_sujeto[f'ROI_{roi_labels[r]}_a{band.title()}']=potencia_promedio
    print(None)

    pd.DataFrame([datos_1_sujeto,datos_1_sujeto])