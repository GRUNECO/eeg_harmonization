

import json
from bids import BIDSLayout
import numpy as np
import pandas as pd


data_path = r'E:\Academico\Universidad\Posgrado\Tesis\repositorio\CodificadoBIDSMini'
layout = BIDSLayout(data_path,derivatives=True)
layout.get(scope='derivatives', return_type='file')

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
    name_1_sujeto = {}
    tasks_1_sujeto = {}
    for b,band in enumerate(bandas):
        for r,roi in enumerate(new_rois):
            potencia_promedio = np.average(np.array(data['channel_power'])[b,roi])
            datos_1_sujeto[f'ROI_{roi_labels[r]}_a{band.title()}']=potencia_promedio
            name_1_sujeto[f'subject']=layout.get_subjects()
            tasks_1_sujeto[f'group']=layout.get_tasks()

#col = ['subject','group','visit','condition','ROI_F_aDelta','ROI_C_aDelta','ROI_PO_aDelta','ROI_T_aDelta','ROI_F_aTheta',
#'ROI_C_aTheta','ROI_PO_aTheta','ROI_T_aTheta','ROI_F_aAlpha1','ROI_C_aAlpha1','ROI_PO_aAlpha1','ROI_T_aAlpha1','ROI_F_aAlpha2',
#'ROI_C_aAlpha2','ROI_PO_aAlpha2','ROI_T_aAlpha2','ROI_F_aBeta1','ROI_C_aBeta1','ROI_PO_aBeta1','ROI_T_aBeta1','ROI_F_aBeta2',
#'ROI_C_aBeta2','ROI_PO_aBeta2','ROI_T_aBeta2','ROI_F_aBeta3','ROI_C_aBeta3','ROI_PO_aBeta3','ROI_T_aBeta3','ROI_F_aGamma','ROI_C_aGamma',
#'ROI_PO_aGamma','ROI_T_aGamma','ROI_F_rDelta','ROI_C_rDelta','ROI_PO_rDelta','ROI_T_rDelta','ROI_F_rTheta','ROI_C_rTheta','ROI_PO_rTheta',
#'ROI_T_rTheta','ROI_F_rAlpha1','ROI_C_rAlpha1','ROI_PO_rAlpha1','ROI_T_rAlpha1','ROI_F_rAlpha2','ROI_C_rAlpha2','ROI_PO_rAlpha2','ROI_T_rAlpha2',
#'ROI_F_rBeta1','ROI_C_rBeta1','ROI_PO_rBeta1','ROI_T_rBeta1','ROI_F_rBeta2','ROI_C_rBeta2','ROI_PO_rBeta2','ROI_T_rBeta2','ROI_F_rBeta3','ROI_C_rBeta3',
#'ROI_PO_rBeta3','ROI_T_rBeta3','ROI_F_rGamma','ROI_C_rGamma','ROI_PO_rGamma','ROI_T_rGamma']
print(pd.DataFrame([datos_1_sujeto]))
print(pd.DataFrame([name_1_sujeto]))
print(pd.DataFrame([tasks_1_sujeto]))
