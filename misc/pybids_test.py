from bids import BIDSLayout

data_path = r'E:\CodificadoBIDS'
layout = BIDSLayout(data_path)
eegs = layout.get(extension='.vhdr', task='CE',suffix='eeg', return_type='filename')
eegs += layout.get(extension='.vhdr', task='OE',suffix='eeg', return_type='filename')
