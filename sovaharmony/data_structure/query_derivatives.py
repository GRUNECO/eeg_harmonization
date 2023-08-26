import json
import ast
import os
import errno
from bids import BIDSLayout
import numpy as np
import re
import pandas as pd
from bids.layout import parse_file_entities
#from sovaharmony.datasets import DUQUEVHI 
from sovaharmony.utils import load_txt

def get_dataframe_columnsIC(THE_DATASET,feature):  
    '''Obtain data frames with powers of Components in different columns'''
    input_path = THE_DATASET.get('input_path',None)
    task = THE_DATASET.get('layout',None).get('task',None)
    group_regex = THE_DATASET.get('group_regex',None)
    name = THE_DATASET.get('name',None)
    runlabel = THE_DATASET.get('run-label','')
    data_path = input_path
    layout = BIDSLayout(data_path,derivatives=True)
    layout.get(scope='derivatives', return_type='file')
    paths= layout.get(extension='.txt',task=task,suffix=feature, return_type='filename')
    #paths = [x for x in paths if f'space-ics[58x25]_norm-True' in x]
    paths = [x for x in paths if f'space-ics[54x10]_norm-True' in x]
    list_subjects = []
    print(paths)
    for i in range(len(paths)):
        data=load_txt(paths[i])
        # if 'spaces' in data['metadata']['axes'].keys():
        #     comp_labels = data['metadata']['axes']['spaces']
            
        # elif 'spaces1' in data['metadata']['axes'].keys():
        #     comp_labels = data['metadata']['axes']['spaces1']
        comp_labels =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25']

        icvalues = np.array(data['values'])
        bandas = data['metadata']['axes']['bands']
        datos_1_sujeto = {}
        info_bids_sujeto = parse_file_entities(paths[i])
        datos_1_sujeto['participant_id'] = 'sub-'+info_bids_sujeto['subject']   
        if group_regex:
            regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
            datos_1_sujeto['group'] = regex.string[regex.regs[-1][0]:regex.regs[-1][1]]
        else:
            datos_1_sujeto['group'] = 'Control'
        try:
            datos_1_sujeto['visit'] = info_bids_sujeto['session']
        except:
            datos_1_sujeto['visit']='V0'
        datos_1_sujeto['condition'] = info_bids_sujeto['task']

        for b,band in enumerate(bandas):
            for c in range(len(comp_labels)):
                if data['metadata']['type']=='crossfreq':
                    for b1,band1 in enumerate(bandas):
                        datos_1_sujeto[f'{feature}_{comp_labels[c]}_M{band1}_{band.title()}']=icvalues[c][b][b1]
                elif data['metadata']['type']=='sl' or data['metadata']['type']=='coherence-bands':
                    datos_1_sujeto[f'{feature}_{comp_labels[c]}_{band.title()}']=np.mean(icvalues[b][c])
                elif data['metadata']['type']=='entropy' or data['metadata']['type']=='power':
                    datos_1_sujeto[f'{feature}_{comp_labels[c]}_{band.title()}']=icvalues[b,c]
        list_subjects.append(datos_1_sujeto)
    df = pd.DataFrame(list_subjects)
    df['database']=[name]*len(list_subjects)
    try:
        path="{input_path}\derivatives\data_columns\IC".format(input_path=input_path).replace('\\','/')
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    df.to_feather(r'{path}\data_{name}_{task}_columns_{feature}_components.feather'.format(name=name,path=path,task=task,feature=feature))
    print('Done!')
    return df 

def get_dataframe_columnsROI(THE_DATASET,feature):  
    '''Obtain data frames with powers of Components in different columns'''
    input_path = THE_DATASET.get('input_path',None)
    task = THE_DATASET.get('layout',None).get('task',None)
    group_regex = THE_DATASET.get('group_regex',None)
    name = THE_DATASET.get('name',None)
    runlabel = THE_DATASET.get('run-label','')
    data_path = input_path
    layout = BIDSLayout(data_path,derivatives=True)
    layout.get(scope='derivatives', return_type='file')
    paths= layout.get(extension='.txt',task=task,suffix=feature, return_type='filename')
    paths = [x for x in paths if f'space-sensors_norm-True' in x]
    list_subjects = []
    F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
    T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
    C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
    PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
    rois = [F,C,PO,T]
    roi_labels = ['F','C','PO','T']

    for i in range(len(paths)):
        # with open(paths[i],'r', encoding='utf-8', errors='ignore') as f:
        #     data=ast.literal_eval(f.read())
        data=load_txt(paths[i])
        new_rois = []

        if 'spaces' in data['metadata']['axes'].keys():
            sensors = data['metadata']['axes']['spaces']

        elif 'spaces1' in data['metadata']['axes'].keys():
            sensors = data['metadata']['axes']['spaces1']
            
        elif 'spaces2' in data['metadata']['axes'].keys():
            sensors = data['metadata']['axes']['spaces2']
        
        for roi in rois:
            channels = set(sensors).intersection(roi)
            new_roi = []
            for channel in channels:
                index=sensors.index(channel)
                new_roi.append(index)
            new_rois.append(new_roi)

        icvalues = np.array(data['values'])
        bandas = data['metadata']['axes']['bands']
        datos_1_sujeto = {}
        info_bids_sujeto = parse_file_entities(paths[i])
        datos_1_sujeto['participant_id'] = 'sub-'+info_bids_sujeto['subject']   
        if group_regex:
            regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
            datos_1_sujeto['group'] = regex.string[regex.regs[-1][0]:regex.regs[-1][1]]
        else:
            datos_1_sujeto['group'] = 'Control'
        try:
            datos_1_sujeto['visit'] = info_bids_sujeto['session']
        except:
            datos_1_sujeto['visit']='V0'
        datos_1_sujeto['condition'] = info_bids_sujeto['task']

        for b,band in enumerate(bandas):
            for r,roi in enumerate(new_rois):
                if data['metadata']['type']=='crossfreq':
                    for b1,band1 in enumerate(bandas):
                        datos_1_sujeto[f'{feature}_{roi_labels[r]}_M{band1}_{band.title()}']= icvalues[roi][b][b1][np.nonzero(icvalues[roi][b][b1])].mean()
                elif data['metadata']['type']=='sl' or data['metadata']['type']=='coherence-bands':
                    datos_1_sujeto[f'{feature}_{roi_labels[r]}_{band.title()}']=np.mean(icvalues[b][roi])
                elif data['metadata']['type']=='entropy' or data['metadata']['type']=='power':
                    datos_1_sujeto[f'{feature}_{roi_labels[r]}_{band.title()}']=np.mean(icvalues[b,roi])
        list_subjects.append(datos_1_sujeto)
    df = pd.DataFrame(list_subjects)
    df['database']=[name]*len(list_subjects)
    try:
        path="{input_path}\derivatives\data_columns\ROI".format(input_path=input_path).replace('\\','/')
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    df.to_feather(r'{path}\data_{name}_{task}_columns_{feature}_ROI.feather'.format(name=name,path=path,task=task,feature=feature))
    print('Done!')
    return df 
