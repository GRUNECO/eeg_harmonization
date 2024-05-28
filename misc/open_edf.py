import mne 
import glob
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sy 

# %     ind1 = find(type==32767);    % Marca de inicio de grabación
# %     ind2 = find(type==9728); % Marca de fin de grabación

# % Selección segmento de grabación
#     event = EEG.event;
#     type = zeros(2,1);
#     for ii = 1:length(event)
#         type(ii) = event(1,ii).type;
#     end
# %     ind1 = find(type==32767);    % Marca de inicio de grabación
# %     ind2 = find(type==9728); % Marca de fin de grabación
#       ind1 = type(1);
#       ind2 = type(2);
#     %if isempty(ind1)
#     if ind1 == 0
#         ini_rec = 1;
#     else
#         ini_rec = event(1,1).latency;
#     end
#     if ind2 == 0
#         end_rec = length(EEG.data);
#     else

#filename1=r'E:\PROYECTO_EEG_LAPSIM\FORMATO_EDF\estudiantes_2021\TRLP28~ S1CE_b9bd277d-86d9-40a1-880a-3e334c68c7bb.edf'
#filename2=r'D:\XIMENA\BIDS\Estudiantes2021\sub-28\ses-S1\eeg\sub-28_ses-S1_task-CE_eeg.vhdr'
#filename=r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\BIOMARCADORES\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_desc-prep_eeg.fif"


# Biomarcadores = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\BIOMARCADORES\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_eeg.vhdr"
# B = mne.io.read_raw(Biomarcadores, preload=True)
# print('UdeA 1:  \n Number of channels: ',len(B.ch_names),'Channels: ',B.ch_names)
# Duque=r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\DUQUE\sub-ALZCE001\eeg\sub-ALZCE001_task-resting_eeg.vhdr"
# D = mne.io.read_raw(Duque,preload=True )
# print('UdeA 2:  \n Number of channels: ',len(D.ch_names),'Channels: ',D.ch_names)
# SRM=r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\SRM\sub-001\ses-t1\eeg\sub-001_ses-t1_task-resteyesc_eeg.edf"
# S = mne.io.read_raw(SRM,preload=True )
# print('SRM:  \n Number of channels: ',len(S.ch_names),'Channels: ',S.ch_names)
# CHBMP=r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\CHBMP\sub-CBM00001\eeg\sub-CBM00001_task-protmap_eeg.edf"
# C = mne.io.read_raw(CHBMP,preload=True )
# print('CHBMP:  \n Number of channels: ',len(C.ch_names),'Channels: ',C.ch_names)
# print("Ok")


#raw = mne.io.read_raw(filename,preload=True )
#raw2= mne.io.read_raw(filename2,preload=True )


# raw.pick_types(eeg=True, eog=True, stim=True).crop(tmax=60).load_data()
# report = mne.Report(title='Raw')
# # This method also accepts a path, e.g., raw=raw_path
# report.add_raw(raw=raw, title='Raw 1', psd=True)  # omit PSD plot
# report.save(r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena\report_raw.html', overwrite=True)

# raw2.pick_types(eeg=True, eog=True, stim=True).crop(tmax=60).load_data()
# report2 = mne.Report(title='Raw in BIDS')
# report2.add_raw(raw=raw, title='Raw BDIS', psd=True)  # omit PSD plot
# report2.save(r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena\report_raw_BIDS.html', overwrite=True)

# print('\nChannels whitout BIDS')
# print(raw.ch_names)

# print('\nChannels whit BIDS')
# print(raw2.ch_names)

#raw.plot()

#raw1 = read_raw(filename1,preload=True )
#raw2 = read_raw(filename2,preload=True )
#raw3 = read_raw(filename3,preload=True )
#raw4 = read_raw(filename4,preload=True )
#raw = mne.read_epochs(filename, verbose='error')
#raw2 = mne.read_epochs(filename2, verbose='error')
#raw3 = mne.read_epochs(filename3, verbose='error')
#raw4 = mne.read_epochs(filename4, verbose='error')

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
#raw1.plot()
#raw2.plot()
#raw3.plot()
#raw4.plot()
#raw.plot_psd()

signal=r"D:\portables\Data\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-OE_desc-reduce[restOE]_eeg.fif"
raw= mne.io.read_raw(signal,preload=True )
fig=raw.plot()
fig.savefig('test_fig.png', bbox_inches='tight')
