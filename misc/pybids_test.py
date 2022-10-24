from bids import BIDSLayout
import os

data_path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\OTRASBASESDEDATOS\NEW'
try:
    layout = BIDSLayout(data_path)
    eegs = layout.get(extension='.vhdr', task='CE',suffix='eeg', return_type='filename')
    eegs += layout.get(extension='.vhdr', task='OE',suffix='eeg', return_type='filename')
    print('BIDS format OK')
except:
    print('Try to convert of Dataset in BIDS format using "conversion_bids"')
