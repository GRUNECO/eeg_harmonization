"""Run sovaharmony on high-density EEG, one stage at a time.

Usage (from the repository root):
    python examples/run_high_density.py prep      # 1. preprocessing
    python examples/run_high_density.py features  # 2. features
    python examples/run_high_density.py tables    # 3. data frames

Edit config_params/config_params_high_density.py first.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repository root

from sovaharmony.pipeline import pipeline
from config_params.config_params_high_density import (
    THE_DATASETS, spatial, bands, metrics, L_FREQ, H_FREQ, epoch_length)

stage = sys.argv[1] if len(sys.argv) > 1 else None
if stage not in ('prep', 'features', 'tables'):
    sys.exit(__doc__)

pipeline(THE_DATASETS,
         L_FREQ=L_FREQ,
         H_FREQ=H_FREQ,
         epoch_length=epoch_length,
         prep=(stage == 'prep'),
         post=(stage == 'features'),
         portables=False,            # False = high density; True = reduce to 8 channels
         prepdf=(stage == 'tables'),
         propdf=(stage == 'tables'),
         spatial_matrix=spatial,
         metrics=metrics,
         IC=(None not in spatial),   # features on components
         Sensors=(None in spatial),  # features on sensors
         roi=False,
         OVERWRITE=False,
         bands=bands)
