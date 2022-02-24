

import json
from bids import BIDSLayout
import numpy as np
import re
data_path = r'Y:\datasets\CodificadoBIDSMini'
layout = BIDSLayout(data_path,derivatives=True)
layout.get(scope='derivatives', return_type='file')
import pandas as pd
from bids.layout import parse_file_entities
eegs_powers = layout.get(extension='.txt', task='CE',suffix='icpowers', return_type='filename')
eegs_powers += layout.get(extension='.txt', task='OE',suffix='icpowers', return_type='filename')

list_subjects = []
for i in range(len(eegs_powers)):
    with open(eegs_powers[i], 'r') as f:
        data = json.load(f)

    ncomps = np.array(data['ics_power']).shape[1]
    comp_labels = ['C'+str(i+1) for i in range(ncomps)]
    icpowers = np.array(data['ics_power'])
    bandas = data['bands']

    datos_1_sujeto = {}
    info_bids_sujeto = parse_file_entities(eegs_powers[i])
    datos_1_sujeto['subject'] = info_bids_sujeto['subject']
    regex = re.search('(.+).{3}',info_bids_sujeto['subject'])
    datos_1_sujeto['group'] = regex.string[regex.regs[-1][0]:regex.regs[-1][1]]
    datos_1_sujeto['visit'] = info_bids_sujeto['session']
    datos_1_sujeto['condition'] = info_bids_sujeto['task']
    for b,band in enumerate(bandas):
        for c in range(ncomps):
            datos_1_sujeto[f'{comp_labels[c]}_r{band.title()}']=icpowers[b,c]
    list_subjects.append(datos_1_sujeto)


df = pd.DataFrame(list_subjects)
