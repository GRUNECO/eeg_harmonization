import os
import errno
from bids import BIDSLayout
import numpy as np
import re
import pandas as pd
from bids.layout import parse_file_entities
from sovaharmony.utils import load_txt, load_file


def get_dataframe_columnsIC(
    THE_DATASET,
    feature=None,
    spatial_matrix='54x10',
    fit_params=False,
    norm=False,
    demographic=False
):
    """
    Generate dataframes with metrics of components in separate columns.

    Parameters:
        THE_DATASET (dict): Dataset info (input_path, layout, etc.).
        feature (str): Feature para generar el dataframe (e.g. 'power').
        spatial_matrix (str): Identificador de la matriz espacial.
        fit_params (bool): Incluir parámetros de ajuste si se usa IRASA.
        norm (bool): Si usar versión normalizada.
        demographic (bool): Si incluir datos demográficos.

    Returns:
        pandas.DataFrame o DataFrame vacío si no se encuentra nada.
    """
    import os
    import re
    import numpy as np
    import pandas as pd
    from bids import BIDSLayout
    from bids.layout import parse_file_entities

    # Paths y metadatos base
    input_path = THE_DATASET.get('input_path', None)
    demographic_path = THE_DATASET.get('demographic', None)
    task = THE_DATASET.get('layout', {}).get('task', None)
    group_regex = THE_DATASET.get('group_regex', None)
    name = THE_DATASET.get('name', None)
    layout = BIDSLayout(input_path)
    runlabel = THE_DATASET.get('run-label', '')

    if not input_path or not feature:
        print("[ERROR] Faltan input_path o feature en THE_DATASET")
        return pd.DataFrame()

    # Layout BIDS
    layout = BIDSLayout(input_path, derivatives=True)
    layout.get(scope='derivatives', return_type='file')
    if feature == 'power':
        # Buscar archivos que coincidan con la característica y matriz espacial
        paths = layout.get(extension='.txt', task=task, suffix='psd', return_type='filename')
    else:
        paths = layout.get(extension='.txt', task=task, suffix=feature, return_type='filename')

    norm_str = 'True' if norm else 'False'
    filter_tag = f"space-ics[{spatial_matrix}]_norm-{norm_str}"
    paths = [x for x in paths if filter_tag in x]

    if not paths:
        print(f"[WARN] No hay archivos para {feature} ({spatial_matrix}, norm={norm_str}) en {input_path}")
        return pd.DataFrame()

    list_subjects = []
    
    for file_path in paths:
        data = load_txt(file_path)

        # Etiquetas de componentes según la matriz espacial
        if spatial_matrix == '58x25':
            comp_labels = [f'C{i}' for i in range(1, 26)]
            bandas = data['metadata']['kwargs']['bands']
        elif spatial_matrix == '54x10':
            comp_labels = [f'C{i}' for i in range(1, 11)]
            bandas = data['metadata']['kwargs']['bands']
        elif spatial_matrix in ('cresta', 'openBCI', 'paper'):
            comp_labels = ['C1', 'C2', 'C3', 'C5', 'C6', 'C8', 'C9', 'C10']
            bandas = data['metadata']['axes']['bands']
        else:
            print(f"[WARN] spatial_matrix desconocido: {spatial_matrix}")
            continue

        icvalues = np.array(data['values'])
        datos_1_sujeto = {}
        info_bids_sujeto = parse_file_entities(file_path)
        datos_1_sujeto['participant_id'] = 'sub-' + info_bids_sujeto['subject']

        if group_regex:
            regex = re.search('(.+).{3}', info_bids_sujeto['subject'])
            datos_1_sujeto['group'] = regex.string[regex.regs[-1][0]:regex.regs[-1][1]]
        else:
            datos_1_sujeto['group'] = 'Control'

        datos_1_sujeto['visit'] = info_bids_sujeto.get('session', 'V0')
        datos_1_sujeto['condition'] = info_bids_sujeto.get('task', '')

        # Guardar valores
        if data['metadata']['type'] == 'irasa' and fit_params:
            icvalues = np.array(data['fit_params']['values'])
            for a, ax in enumerate(data['fit_params']['axes']):
                for c in range(len(comp_labels)):
                    datos_1_sujeto[f'{feature}_{comp_labels[c]}_{ax}'] = icvalues[c, a]
        else:
            for b, band in enumerate(bandas):
                for c in range(len(comp_labels)):
                    if data['metadata']['type'] == 'crossfreq':
                        for b1, band1 in enumerate(bandas):
                            datos_1_sujeto[f'{feature}_{comp_labels[c]}_M{band1}_{band.title()}'] = icvalues[c][b][b1]
                    elif data['metadata']['type'] in ('sl', 'coherence-bands'):
                        datos_1_sujeto[f'{feature}_{comp_labels[c]}_{band.title()}'] = np.mean(icvalues[b][c])
                    elif data['metadata']['type'] in ('entropy', 'power', 'irasa', 'psd') and not fit_params:
                        datos_1_sujeto[f'{feature}_{comp_labels[c]}_{band.title()}'] = icvalues[b, c]
            list_subjects.append(datos_1_sujeto)

    if not list_subjects:
        print(f"[WARN] Lista de sujetos vacía para {feature} ({spatial_matrix}, norm={norm_str})")
        return pd.DataFrame()

    df = pd.DataFrame(list_subjects)
    df['database'] = [name] * len(df)

    # Carpeta destino
    save_dir = f"{input_path}/derivatives/data_columns/IC".replace('\\', '/')
    os.makedirs(save_dir, exist_ok=True)

    # Ajustar nombre de feature si es ape con fit_params
    if feature == 'ape' and fit_params:
        feature = 'ape_fit_params'

    # Guardar archivo
    if demographic:
        demograficos = load_file(demographic_path)
        demograficos.rename(columns={'subject': 'participant_id'}, inplace=True)
        demograficos['participant_id'] = 'sub-' + demograficos['participant_id'].astype(str).str.replace('_', '')
        if 'visit' not in demograficos.columns:
            demograficos['visit'] = 'V0'
        df_merge = pd.merge(df, demograficos, how='outer', on=["participant_id", 'visit', 'group'])
        df_merge.dropna(inplace=True)
        out_file = f"{save_dir}/data_{name}_{task}_columns_{feature}_{spatial_matrix}_{norm_str}_components_dem.feather".replace('\\', '/')
        df_merge.to_feather(out_file)
        print(f"[OK] Guardado con demográficos: {out_file}")
    else:
        out_file = f"{save_dir}/data_{name}_{task}_columns_{feature}_{spatial_matrix}_{norm_str}_components.feather".replace('\\', '/')
        df.to_feather(out_file)
        print(f"[OK] Guardado: {out_file}")

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
    paths = [x for x in paths if f'space-sensors_norm-{norm}' in x and 'sovaharmony' in x]
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
                print(sensors)
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
            if data['metadata']['type']=='irasa' and fit_params:
                icvalues = np.array(data['fit_params']['values'])
                for a, ax in enumerate(data['fit_params']['axes']):
                    for r,roi in enumerate(new_rois):
                        datos_1_sujeto[f'{feature}_{roi_labels[r]}_{ax}']=icvalues[r,a]
            else:
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
