from re import S
from sovaflow.flow_mongo import mne_open
from sovaflow.utils import topomap
from sovachronux.qeeg_psd_chronux import qeeg_psd_chronux
from mne import make_fixed_length_epochs
from mne.io import read_raw 
from mne.channels import make_standard_montage
import copy
import numpy as np
from pyprep import PrepPipeline
from mne.preprocessing import ICA
from sklearn.decomposition import FastICA
from sovawica.wica import w_ica_matlab
from sovareject.tools import format_data
from sovaflow.utils import createRaw
from sovareject import eegthresh
from sovareject import rejtrend
from sovareject import rejkurt
from sovareject import spectrumthresh
from sovareject import rejection
from sovareject import metrics as mt
from sovareject._rejection import get_reject_vector

filename = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\ds_bids_chbmp\sub-CBM00001\eeg\sub-cbm00001_task-protmap_eeg.edf"

raw = read_raw(filename)
print(raw.ch_names)
