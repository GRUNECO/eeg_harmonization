# eeg-harmonization

> **Update (2026-10-23).** The script `sovaharmony/metrics/pme.py` (cross-frequency / PME features) was updated to correct an inversion error detected by the team: the loops computed the opposite triangle of carrier / modulation-band pairs. If you have used these features in a study, please reinstall, clone or download the repository again. Only the cross-frequency (PME) features are affected, but if you used the previous version of the code, you need to re-run it.
>
> **APPLEE users:** APPLEE ([GNACo/APPLEE](https://github.com/GNACo/APPLEE)) uses this package and its `requirements.txt` still pins a version with the previous code. See [docs/APPLEE_crossfreq_labels.md](docs/APPLEE_crossfreq_labels.md) for how to install the corrected version and how the cross-frequency columns are named.

# eeg-harmonization (`sovaharmony`)

Pipeline to preprocess and harmonize resting-state EEG recorded in different databases and laboratories, and to extract features from it. It works on datasets in [BIDS](https://bids.neuroimaging.io/) format and writes its outputs into a `derivatives/sovaharmony` folder inside each dataset.

By default it is configured for **high-density EEG** (54 channels). A reduction to an 8-channel montage (low density, used with portable devices) is available as an option.

## What the pipeline does

| Stage | Function | What it does | Output (inside `<dataset>/derivatives/sovaharmony`) |
|---|---|---|---|
| 1. Preprocessing | `harmonize` (`sovaharmony/preprocessing.py`) | Cleaning with PREP and wavelet-ICA, epoching, rejection of bad epochs, Huber normalization. | `.fif` files (`prep`, `wica`, `reject[...]`, `huber[...]`), quality statistics, log in `code/` |
| 2. Features | `features` (`sovaharmony/postprocessing.py`) | Computes features per epoch, on the sensors or on independent components (ICs) obtained with a spatial filter. | `.txt` / `.json` files per recording and feature |
| 3. Data frames | `pipeline(..., prepdf=True, propdf=True)` | Collects the previous outputs into tables (one row per participant). | `.feather` / long-format tables |

Stages are controlled with the flags `prep`, `post`, `prepdf`, `propdf` of `sovaharmony.pipeline.pipeline`, so each one can be run separately.

After stage 3, the repository [Data_analysis_ML_Harmonization_Proyect](https://github.com/GRUNECO/Data_analysis_ML_Harmonization_Proyect) takes the tables through cleaning of outliers, ComBat harmonization, plots and machine-learning models (see *Next steps*).

## Installation

Python 3.11 was used for the last tests of this README. The package depends on four group libraries (`sovaflow`, `sovareject`, `sovachronux`, `sovawica`) that `requirements.txt` installs from Git.

```bash
git clone https://github.com/GRUNECO/eeg_harmonization.git
cd eeg_harmonization
python -m venv .venv
# Windows (PowerShell): .venv\Scripts\Activate.ps1      Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

`requirements.txt` fixes exact versions (for example `numpy==2.1.3`, `mne==1.8.0`). Use a separate environment for this package to avoid conflicts with other projects.

### Upgrading

```bash
git pull
pip install -r requirements.txt
pip install -e . --no-deps
```

## Quick start: high-density EEG

1. **Put the data in BIDS.** If your recordings are not in BIDS, the conversion rules used for our databases are in `misc/reglas_bids/` (examples for `sovabids`).
2. **Copy and edit the configuration:** `config_params/config_params_high_density.py`. For each dataset set `input_path` (BIDS root), `layout` (which recordings to process: extension, task, session), `args['line_freqs']` (50 or 60 Hz) and a `run-label`. Channel names must be standard 10-05 names in upper case.
3. **Run each stage:**

```bash
python examples/run_high_density.py prep       # stage 1
python examples/run_high_density.py features   # stage 2
python examples/run_high_density.py tables     # stage 3
```

Equivalent call from Python:

```python
from sovaharmony.preprocessing import harmonize

BIOMARCADORES = {
    'name': 'BIOMARCADORES',
    'input_path': '/path/to/BIOMARCADORES_BIDS',
    'layout': {'extension': '.vhdr', 'task': 'OE', 'suffix': 'eeg', 'return_type': 'filename'},
    'args': {'line_freqs': [60]},
    'group_regex': '(.+).{3}',
    'events_to_keep': None,
    'run-label': 'restEC',
}

harmonize(BIOMARCADORES, L_FREQ=1, H_FREQ=50, epoch_length=5)
```

### Points to check for your own data

- **Channels.** If the dataset has no `channels` key, the 54 channels listed in `sovaharmony/preprocessing.py` (`default_channels`) are kept. The spatial filters (`sovaharmony/spatial_filters/`) were trained on specific channel sets: `54x10` (10 components from 54 channels, the default for high density), `58x25`, `62x19`, `53x53`. The features on components use the intersection between the filter's channels and the recording's channels. Check that your montage contains the channels of the filter you choose.
- **Features.** Stage 2 computes the features listed in the `features` key of each dataset (default `['psd', 'power']`). Options: `psd`, `power`, `power_osc`, `power_ape`, `sl`, `cohfreq`, `entropy`, `crossfreq`. `psd` is the full multitaper spectrum (one value per frequency, no bands); the others are summarized by band. Stage 3 builds tables only from band-based features, so `metrics` in the configuration must list those (for example `power`), not `psd`.
- **Components or sensors.** `spatial = ['54x10']` computes the features on ICs; `spatial = [None]` computes them on sensors.
- **Low density (8 channels).** Use `portables=True` and `tmontage` (`'cresta'`, `'openBCI'` or `'paper'`, defined in `sovaharmony/metrics/features.py`). `processingEEG.py` is an example of this use.
- **Cross-frequency features (`crossfreq`).** See the notice at the top of this file. Use the updated version.

## Repository layout

| Path | Content |
|---|---|
| `sovaharmony/` | The package: `preprocessing.py`, `postprocessing.py`, `pipeline.py`, `spatial.py`, `metrics/` (features), `data_structure/` (tables), `graphics/`, `spatial_filters/`. |
| `config_params/` | Example configurations (`config_params_high_density.py`, `config_params_tutorial.py`). |
| `examples/` | `run_high_density.py`. |
| `misc/` | Historical scripts of earlier analyses (see `misc/README.md`). |
| `docs/` | Notes (`APPLEE_crossfreq_labels.md`) and the group's publication list (`PUBLICATIONS.md`). |

## Next steps after the tables

Order used in our studies (the steps of the second repository are in [Data_analysis_ML_Harmonization_Proyect](https://github.com/GRUNECO/Data_analysis_ML_Harmonization_Proyect), folder `Manipulation`):

1. `eeg_harmonization`: `processingEEG.py` (or `examples/run_high_density.py`)
2. `Dataframes_potencias_Componentes_Demograficos.py` | `Dataframes_potencias_Rois_demograficos.py`
3. `Borrar_datos_atipicos_potencias.py`
4. `Dataframes_SL_Coherencia_Entropy_Cross.py`
5. `eeg_harmonization/misc/neuroharmonaze.py` (ComBat)
6. `unirfeatherharmonize.py`
7. `Graficos_power_sl_coherencia_entropia_cross.py`
8. `graficos_data_harmonized.py`
9. `training_script.py`

Steps 7 to 9 can run in parallel.

## Citation

If you use this pipeline, please cite:

- Henao Isaza V, Aguillon D, Tobón-Quintero CA, Lopera F, Ochoa-Gómez JF. Comprehensive methodology for sample enrichment in EEG biomarker studies for Alzheimer's risk classification. PLOS ONE 21(3): e0343722 (2026). https://doi.org/10.1371/journal.pone.0343722
- Henao Isaza V, Cadavid Castro V, Zapata Saldarriaga L, Mantilla-Ramos Y, Tobón Quintero C, Suarez Revelo J, Ochoa Gómez J. Tackling EEG test-retest reliability with a pre-processing pipeline based on ICA and wavelet-ICA. Authorea Preprints (2023). https://doi.org/10.22541/au.168570191.12788016/v1

More publications of the group: [docs/PUBLICATIONS.md](docs/PUBLICATIONS.md).
