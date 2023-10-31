import os
import errno
from bids import BIDSLayout
import numpy as np
import re
import pandas as pd
from bids.layout import parse_file_entities
#from sovaharmony.datasets import DUQUEVHI 
from sovaharmony.utils import load_txt

def get_dataframe_columnsIC(THE_DATASET,feature,spatial_matrix='54x10',fit_params=False,norm='False'):  
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
    if spatial_matrix=='54x10' and norm=='False':
        paths = [x for x in paths if f'space-ics[54x10]_norm-False' in x]
    elif spatial_matrix=='54x10' and norm=='True':
        paths = [x for x in paths if f'space-ics[54x10]_norm-True' in x]
    elif spatial_matrix=='58x25' and norm=='False':
        paths = [x for x in paths if f'space-ics[58x25]_norm-False' in x]
    elif spatial_matrix=='58x25' and norm=='True':
        paths = [x for x in paths if f'space-ics[58x25]_norm-True' in x]
    elif spatial_matrix=='cresta' and norm=='False':
        paths = [x for x in paths if f'space-ics[cresta]_norm-False' in x]
    elif spatial_matrix=='cresta' and norm=='True':
        paths = [x for x in paths if f'space-ics[cresta]_norm-True' in x]
    elif spatial_matrix=='paper' and norm=='False':
        paths = [x for x in paths if f'space-ics[paper]_norm-False' in x]
    elif spatial_matrix=='paper' and norm=='True':
        paths = [x for x in paths if f'space-ics[paper]_norm-True' in x]
    elif spatial_matrix=='openBCI' and norm=='False':
        paths = [x for x in paths if f'space-ics[openBCI]_norm-False' in x]
    elif spatial_matrix=='openBCI' and norm=='True':
        paths = [x for x in paths if f'space-ics[openBCI]_norm-True' in x]

    list_subjects = []
    for i in range(len(paths)):
        data=load_txt(paths[i])
        if spatial_matrix=='58x25':
            comp_labels =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25']
        elif spatial_matrix=='54x10':
            comp_labels =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
        elif spatial_matrix=='cresta' or spatial_matrix=='openBCI' or spatial_matrix=='paper':
            comp_labels =['C1', 'C2', 'C3', 'C4', 'C5', 'C7', 'C8', 'C10']

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
        
        if data['metadata']['type']=='power' and fit_params:
            for a, ax in enumerate(data['fit_params']['axes']):
                for c in range(len(comp_labels)):
                    datos_1_sujeto[f'{feature}_{comp_labels[c]}_{ax}']=icvalues[a,c]
            
        else:
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
    if feature=='ape':
        feature= 'ape_fit_params'
    df.to_feather(r'{path}\data_{name}_{task}_columns_{feature}_{spatial_matrix}_components.feather'.format(name=name,path=path,task=task,feature=feature,spatial_matrix=spatial_matrix).replace('\\','/'))
    print('Done!')
    return df 

def get_dataframe_columns_sensors(THE_DATASET,feature,norm='False',roi=False):  
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
    paths = [x for x in paths if f'space-sensors_norm-{norm}' in x]
    list_subjects = []
    
    if roi:
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
        if roi:
            for roi_ in rois:
                channels = set(sensors).intersection(roi_)
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
        if len(new_rois)!=0:
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
        else:
            for b,band in enumerate(bandas):
                for s,sensor in enumerate(sensors):
                    if data['metadata']['type']=='crossfreq':
                        for b1,band1 in enumerate(bandas):
                            datos_1_sujeto[f'{feature}_{sensor}_M{band1}_{band.title()}']= icvalues[s][b][b1][np.nonzero(icvalues[s][b][b1])].mean()
                    elif data['metadata']['type']=='sl' or data['metadata']['type']=='coherence-bands':
                        datos_1_sujeto[f'{feature}_{sensor}_{band.title()}']=np.mean(icvalues[b][s])
                    elif data['metadata']['type']=='entropy' or data['metadata']['type']=='power':
                        datos_1_sujeto[f'{feature}_{sensor}_{band.title()}']=icvalues[b,s]
                    
            list_subjects.append(datos_1_sujeto)
    df = pd.DataFrame(list_subjects)
    df['database']=[name]*len(list_subjects)
    if roi:
        try:
            path="{input_path}\derivatives\data_columns\ROI".format(input_path=input_path).replace('\\','/')
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        df.to_feather(r'{path}\data_{name}_{task}_columns_{feature}_roi.feather'.format(name=name,path=path,task=task,feature=feature))
    else:
        try:
            path="{input_path}\derivatives\data_columns\SENSORS".format(input_path=input_path).replace('\\','/')
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        df.to_feather(r'{path}\data_{name}_{task}_columns_{feature}_sensors.feather'.format(name=name,path=path,task=task,feature=feature))
    print('Done!')
    return df 
