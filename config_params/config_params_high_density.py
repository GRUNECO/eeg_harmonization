"""Example configuration for high-density (54 channels) resting-state EEG.

Copy this file, change the paths and the BIDS query of each dataset, and pass the
values to `sovaharmony.pipeline.pipeline` (see examples/run_high_density.py).

Every dataset must already be in BIDS format.
"""

THE_DATASETS = [
    {
        'name': 'MY_DATASET',                      # free label
        'input_path': r'/path/to/MY_DATASET_BIDS',  # BIDS root folder
        # Query passed to pybids' BIDSLayout.get(): selects which recordings are processed
        'layout': {'extension': '.vhdr', 'task': 'rest', 'suffix': 'eeg',
                   'return_type': 'filename'},
        'args': {'line_freqs': [60]},               # power-line frequency (60 Hz Americas, 50 Hz Europe)
        'group_regex': None,                        # regex to get the group from the subject ID, or None
        'events_to_keep': None,                     # list of event codes to keep, or None
        'run-label': 'restCE',                      # names the derivatives; change it to avoid overwriting
        # 'channels': [...],                        # optional; default is the 54-channel list in preprocessing.py
        # 'spatial_filter': '54x10',                # optional; overrides the filter chosen below
        # 'features': ['psd', 'power'],             # optional; features computed in stage 2 (this is the default)
    },
]

# Spatial filter that projects the 54 channels onto independent components (ICs).
# Available: '54x10' (default, same 54 channels as default_channels), '58x25', '62x19', '53x53' (see sovaharmony/spatial_filters).
# Use [None] to compute the features on the sensors instead of on components.
spatial = ['54x10']

# Frequency bands (Hz)
bands = {'Delta': (1.5, 6),
         'Theta': (6, 8.5),
         'Alpha-1': (8.5, 10.5),
         'Alpha-2': (10.5, 12.5),
         'Beta1': (12.5, 18.5),
         'Beta2': (18.5, 21),
         'Beta3': (21, 30),
         'Gamma': (30, 45)}

L_FREQ = 1          # high-pass frequency (Hz)
H_FREQ = 50         # low-pass frequency (Hz)
epoch_length = 5    # epoch length (s)

# Features that are collected into data frames in stage 3. They must be band-based
# features computed in stage 2 (see 'features' above): 'power', 'power_osc', 'power_ape',
# 'sl', 'cohfreq', 'entropy' or 'crossfreq'. 'psd' is the full multitaper spectrum (it has no
# band axis), so it is saved in stage 2 but cannot go through the stage 3 tables.
metrics = {'power': {'fit_params': False, 'norm': 'False', 'demographic': False}}
