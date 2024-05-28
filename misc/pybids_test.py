from bids import BIDSLayout

def test_bids():
    sourcePath = input('Ingrese el Path: ')
    try:
        layout = BIDSLayout(sourcePath)
        eegs = layout.get(extension='.fif', task='CE',suffix='eeg', return_type='filename')
        #eegs += layout.get(extension='.edf', task='OE',suffix='eeg', return_type='filename')
        print('BIDS format OK')
    except:
        print('Try to convert of Dataset in BIDS format using "conversion_bids"')
      
if __name__ == '__main__':
    test_bids()

