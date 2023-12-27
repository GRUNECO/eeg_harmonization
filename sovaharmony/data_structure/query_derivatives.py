import os
import errno
from bids import BIDSLayout
import numpy as np
import re
import pandas as pd
from bids.layout import parse_file_entities
from sovaharmony.utils import load_txt, load_file

def get_dataframe_columnsIC(THE_DATASET,feature=str,spatial_matrix='54x10',fit_params=False,norm='False',demographic=False):  
    '''
    Generate dataframes with metrics of components in separate columns.

    Parameters:
        THE_DATASET (dict): The dataset containing the relevant information about database.
        feature (str): The specific feature for which the dataframe is generated.
        spatial_matrix (str, optional): The spatial matrix identifier. Default is '54x10'.
        fit_params (bool, optional): Whether to include fit parameters when using toolbox irasa. Default is False.
        norm (str, optional): Normalization option. Default is 'False'. If you need generate the df using the data normalice. 

    Returns:
        pandas.DataFrame: A dataframe containing the metric of components in separate columns.

    Example:
        df = get_dataframe_columnsIC(my_dataset, 'power', spatial_matrix='54x10', fit_params=True, norm='True')

    Note:
        This function extracts relevant information from the dataset and organizes it into a dataframe,
        with each component's power in a separate column. The columns may include spatial information,
        fit parameters, and normalization factors based on the specified parameters.
    '''
    input_path = THE_DATASET.get('input_path',None)
    demographic_path= THE_DATASET.get('demographic',None)
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
        
        if data['metadata']['type']=='irasa' and fit_params:
            icvalues = np.array(data['fit_params']['values'])
            for a, ax in enumerate(data['fit_params']['axes']):
                for c in range(len(comp_labels)):
                    datos_1_sujeto[f'{feature}_{comp_labels[c]}_{ax}']=icvalues[c,a]
            
        else:
            for b,band in enumerate(bandas):
                for c in range(len(comp_labels)):
                    if data['metadata']['type']=='crossfreq':
                        for b1,band1 in enumerate(bandas):
                            datos_1_sujeto[f'{feature}_{comp_labels[c]}_M{band1}_{band.title()}']=icvalues[c][b][b1]
                    elif data['metadata']['type']=='sl' or data['metadata']['type']=='coherence-bands':
                        datos_1_sujeto[f'{feature}_{comp_labels[c]}_{band.title()}']=np.mean(icvalues[b][c])
                    elif (data['metadata']['type']=='entropy' or data['metadata']['type']=='power' or data['metadata']['type']=='irasa') and fit_params==False:
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
    if feature=='ape' and fit_params:
        feature= 'ape_fit_params'
    if demographic:
        demograficos=load_file(demographic_path)
        demograficos.rename(columns={'subject':'participant_id'},inplace=True)
        demograficos['participant_id']='sub-' + demograficos['participant_id'].astype(str)
        df_merge=pd.merge(df,demograficos,how='outer',on=["participant_id",'visit','group'])
        df_merge.dropna(inplace=True)
        df_merge.to_feather(r'{path}\data_{name}_{task}_columns_{feature}_{spatial_matrix}_{norm}_components_dem.feather'.format(name=name,path=path,task=task,feature=feature,spatial_matrix=spatial_matrix,norm=norm).replace('\\','/'))
        print('Done df with demographic data!')
        
    else:
        df.to_feather(r'{path}\data_{name}_{task}_columns_{feature}_{spatial_matrix}_{norm}_components.feather'.format(name=name,path=path,task=task,feature=feature,spatial_matrix=spatial_matrix,norm=norm).replace('\\','/'))
        print('Done!')
    return df 

def get_dataframe_columns_sensors(THE_DATASET,feature,norm='False',roi=False,fit_params=False,demographic=False):  
    '''Obtain data frames with powers of Components in different columns'''
    input_path = THE_DATASET.get('input_path',None)
    demographic_path= THE_DATASET.get('demographic',None)
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
        data=load_txt(paths[i])
        new_rois = []

        key_prefixes = ['spaces', 'spaces1', 'spaces2']
        for key_prefix in key_prefixes:
            if key_prefix in data['metadata']['axes'].keys():
                sensors = data['metadata']['axes'][key_prefix]
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
                    elif data['metadata']['type']=='entropy' or data['metadata']['type']=='power' or data['metadata']['type']=='irasa':
                        datos_1_sujeto[f'{feature}_{roi_labels[r]}_{band.title()}']=np.mean(icvalues[b,roi])
            list_subjects.append(datos_1_sujeto)
        else:
            if data['metadata']['type']=='irasa' and fit_params:
                icvalues = np.array(data['fit_params']['values'])
                for a, ax in enumerate(data['fit_params']['axes']):
                    for s,sensor in enumerate(sensors):
                        datos_1_sujeto[f'{feature}_{sensor}_{ax}']=icvalues[s,a]
            else:
                for b,band in enumerate(bandas):
                    for s,sensor in enumerate(sensors):
                        if data['metadata']['type']=='crossfreq':
                            for b1,band1 in enumerate(bandas):
                                datos_1_sujeto[f'{feature}_{sensor}_M{band1}_{band.title()}']= icvalues[s][b][b1][np.nonzero(icvalues[s][b][b1])].mean()
                        elif data['metadata']['type']=='sl' or data['metadata']['type']=='coherence-bands':
                            datos_1_sujeto[f'{feature}_{sensor}_{band.title()}']=np.mean(icvalues[b][s])
                        elif data['metadata']['type']=='entropy' or data['metadata']['type']=='power' or data['metadata']['type']=='irasa':
                            datos_1_sujeto[f'{feature}_{sensor}_{band.title()}']=icvalues[b,s]
                        
            list_subjects.append(datos_1_sujeto)
    df = pd.DataFrame(list_subjects)
    df['database']=[name]*len(list_subjects)
    if feature=='ape' and fit_params:
        feature= 'ape_fit_params'
    data_type = "ROI" if roi else "SENSORS"
    
    try:
        path = os.path.join(input_path, "derivatives", "data_columns", data_type)
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    # Handle demographic data if specified
    if demographic:
        demograficos = load_file(demographic_path)
        demograficos.rename(columns={'subject': 'participant_id'}, inplace=True)
        demograficos['participant_id'] = 'sub-' + demograficos['participant_id'].astype(str)
        df_merge = pd.merge(df, demograficos, how='outer', on=["participant_id", 'visit', 'group'])
        df_merge.dropna(inplace=True)
        file_name = f"data_{name}_{task}_columns_{feature}_{norm}_{data_type.lower()}_dem.feather"
    else:
        file_name = f"data_{name}_{task}_columns_{feature}_{norm}_{data_type.lower()}.feather"
    
    file_path = os.path.join(path, file_name).replace('\\', '/')
    df.to_feather(file_path)
    print('Done!')
    return df 
