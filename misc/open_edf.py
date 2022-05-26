from mne.io import read_raw
import mne 
import glob
import pandas as pd
import matplotlib.pyplot as plt


#filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\ds_bids_chbmp\sub-CBM00001\eeg\sub-cbm00001_task-protmap_eeg.edf"
#filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM\sub-001\ses-t1\eeg\sub-001_ses-t1_task-resteyesc_eeg.edf"
#filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\LEMON\sub-032301\RSEEG\sub-032301.vhdr"
filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_eeg.vhdr"
#filename1 = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_desc-norm_eeg"
#filename2 = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_desc-reject[restCE]_eeg"
raw = read_raw(filename)
#raw1 = mne.read_epochs(filename1 + '.fif', verbose='error')
#raw2 = mne.read_epochs(filename2 + '.fif', verbose='error')
#raw1.plot()
#raw1.plot(scalings={'eeg':'auto'})
#plt.plot(raw1._data[0,:3].T,label='norm')
#plt.plot(raw2._data[0,:3].T,label='reject')
#plt.title("norm vs reject")
#plt.legend()
#plt.show()
#raw.rename_channels({name: name.replace(' -REF', '').upper() for name in raw.ch_names})
#print(raw._data)
#print(raw.ch_names)
#print(raw.info)
raw.plot_psd(fmax=99)

