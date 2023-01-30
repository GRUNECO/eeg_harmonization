from bids import BIDSLayout
import os

data_path = r'/home/pyeeglapsim/Documents/Proyecto_EEG_LapSim/BIDS/Test_BIDS/convert2bids'
try:
    layout = BIDSLayout(data_path)
    eegs = layout.get(extension='.edf', task='CE',suffix='eeg', return_type='filename')
    eegs += layout.get(extension='.edf', task='OE',suffix='eeg', return_type='filename')
    print('BIDS format OK')
except:
    print('Try to convert of Dataset in BIDS format using "conversion_bids"')
