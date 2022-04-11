

import json
from bids import BIDSLayout
import numpy as np
import re
import pandas as pd
from bids.layout import parse_file_entities
from datasets import SRM as THE_DATASET


input_path = THE_DATASET.get('input_path',None)
task = THE_DATASET.get('layout',None).get('task',None)
group_regex = THE_DATASET.get('group_regex',None)
name = THE_DATASET.get('name',None)
runlabel = THE_DATASET.get('run-label','')

data_path = input_path
layout = BIDSLayout(data_path,derivatives=True)
layout.get(scope='derivatives', return_type='file')
eegs_powers = layout.get(extension='.txt', task=task,desc='channel'+f'[{runlabel}]',suffix='powers', return_type='filename')

F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
rois = [F,C,PO,T]
roi_labels = ['F','C','PO','T']

list_subjects = []
for i in range(len(eegs_powers)):
    print(eegs_powers[i])
    with open(eegs_powers[i], 'r') as f:
        data = json.load(f)
    channels=np.array(data['channels'])
    bandas = data['bands']
    new_rois = []
    potencias_roi_banda=[]

    for roi in rois:
        channels = set(data['channels']).intersection(roi)
        new_roi = []
        for channel in channels:
            index=data['channels'].index(channel)
            new_roi.append(index)
        new_rois.append(new_roi)

    datos_1_sujeto = {}
    info_bids_sujeto = parse_file_entities(eegs_powers[i])
    datos_1_sujeto['subject'] = info_bids_sujeto['subject']
    regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
    if group_regex:
        regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
        datos_1_sujeto['group'] = regex.string[regex.regs[-1][0]:regex.regs[-1][1]]
    datos_1_sujeto['visit'] = info_bids_sujeto['session']
    datos_1_sujeto['condition'] = info_bids_sujeto['task']
    for b,band in enumerate(bandas):
        for r,roi in enumerate(new_rois):
            potencia_promedio = np.average(np.array(data['channel_power'])[b,roi])
            datos_1_sujeto[f'ROI_{roi_labels[r]}_r{band.title()}']=potencia_promedio
    list_subjects.append(datos_1_sujeto)


df = pd.DataFrame(list_subjects)
df.to_excel(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\longitudinal_data_rois_'+name+'.xlsx')
