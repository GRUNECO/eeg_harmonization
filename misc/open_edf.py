import mne 
import glob
import pandas as pd
import matplotlib.pyplot as plt

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

filename=r'E:\PROYECTO_EEG_LAPSIM\FORMATO_EDF\estudiantes_2021\TRLP28~ S1CE_b9bd277d-86d9-40a1-880a-3e334c68c7bb.edf'
filename2=r'D:\XIMENA\BIDS\Estudiantes2021\sub-28\ses-S1\eeg\sub-28_ses-S1_task-CE_eeg.vhdr'
filename3=r'D:\XIMENA\BIDS\Estudiantes2021\derivatives\sovaharmony\sub-28\ses-S1\eeg\sub-28_ses-S1_task-CE_desc-reject[CE]_eeg.fif'
raw = mne.io.read_raw(filename,preload=True )
raw2= mne.io.read_raw(filename2,preload=True )


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

raw.plot()

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
raw.plot_psd()

