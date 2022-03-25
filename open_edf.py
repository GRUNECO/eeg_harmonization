from mne.io import read_raw

#filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\ds_bids_chbmp\sub-CBM00001\eeg\sub-cbm00001_task-protmap_eeg.edf"
filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM\sub-001\ses-t1\eeg\sub-001_ses-t1_task-resteyesc_eeg.edf"
#filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\LEMON\sub-032301\RSEEG\sub-032301.vhdr"
#filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_eeg.vhdr"
raw = read_raw(filename)
#raw.rename_channels({name: name.replace(' -REF', '').upper() for name in raw.ch_names})
print(raw.ch_names)
#raw.plot_psd(fmax=200)
print(raw.info)
