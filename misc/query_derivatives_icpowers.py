import json
from bids import BIDSLayout
import numpy as np
import re
import pandas as pd
from bids.layout import parse_file_entities
from sovaharmony.datasets import DUQUE 



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
    eegs_powers = layout.get(extension='.txt',task=task,suffix=feature, return_type='filename')
    eegs_powers = [x for x in eegs_powers if f'_space-ics[58x25]_norm-True_' in x]

    list_subjects = []
    for i in range(len(eegs_powers)):
        with open(eegs_powers[i], 'r') as f:
            data = json.load(f)

        if 'spaces' in data['metadata']['axes'].keys():
            comp_labels = data['metadata']['axes']['spaces']
            
        elif 'spaces1' in data['metadata']['axes'].keys():
            comp_labels = data['metadata']['axes']['spaces1']

        icvalues = np.array(data['values'])
        bandas = data['metadata']['axes']['bands']

        datos_1_sujeto = {}
        info_bids_sujeto = parse_file_entities(eegs_powers[i])
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
                        datos_1_sujeto[f'{feature}_{comp_labels[c]}_M_{band1}_{band.title()}']=icvalues[c][b][b1]
                elif data['metadata']['type']=='sl':
                    datos_1_sujeto[f'{feature}_{comp_labels[c]}_{band.title()}']=np.mean(icvalues[b][c])
                elif data['metadata']['type']=='entropy':
                    datos_1_sujeto[f'{feature}_{comp_labels[c]}_{band.title()}']=icvalues[b,c]

        list_subjects.append(datos_1_sujeto)

    df = pd.DataFrame(list_subjects)
    df['database']=[name]*len(list_subjects)
    df.to_feather(r'{input_path}\derivatives\data_{feature}_columns_components_{name}.feather'.format(name=name,input_path=input_path,feature=feature))
    print('Done!')

metricas=['crossfreq','entropy','sl']
get_dataframe_columnsIC(DUQUE,feature='crossfreq')
