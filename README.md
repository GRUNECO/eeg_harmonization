# eeg-harmonization

## Installation

```bash
git clone https://github.com/GRUNECO/eeg-harmonization.git
cd eeg_harmonization
pip install -r requirements-install.txt
```

## Upgrading

```bash
pip uninstall sovaharmony
```

Then in the eeg_harmonization repo folder

```bash
git pull
pip install -r requirements-install.txt
```

## Usage

```python

from sovaharmony.processing import harmonize

BIOMARCADORES = {
    'name':'BIOMARCADORES',
    'input_path':'E:/Datos/BASESDEDATOS/BIOMARCADORES_BIDS',
    'layout':{'extension':'.vhdr', 'task':'OE','suffix':'eeg', 'return_type':'filename'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restEC'
}

harmonize(BIOMARCADORES)
```
