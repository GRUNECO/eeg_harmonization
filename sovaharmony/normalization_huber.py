import mne
import statsmodels.api as sm
from sovaharmony.processing import get_derivative_path
from bids import BIDSLayout
from datasets import BIOMARCADORES 
import os
import statistics

THE_DATASET=BIOMARCADORES
layout_dict = THE_DATASET.get('layout',None)
input_path = THE_DATASET.get('input_path',None)
layout = BIDSLayout(input_path)
eegs = layout.get(**layout_dict)
pipelabel = '['+THE_DATASET.get('run-label', '')+']'
bids_root = layout.root
pipeline = 'sovaharmony'
derivatives_root = os.path.join(layout.root,'derivatives',pipeline)

for i,eeg_file in enumerate(eegs):
    reject_path = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
    signal = mne.read_epochs(reject_path)
    signal_hp = signal.filter(None,20,fir_design='firwin')
    desv = statistics.pstdev(channel)
    k = sm.robust.scale.Huber(signal)