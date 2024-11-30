# eeg-harmonization

## Installation
```bash
Third-party installation
pip install git+https://github.com/GRUNECO/eeg_harmonization.git
```

```bash
git clone https://github.com/GRUNECO/eeg_harmonization.git
cd eeg_harmonization
pip install -r requirements.txt
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
```
Orden de archivos:

1. eeg_harmonization\processingEEG.py 
2. Data_analysis_ML_Harmonization_Proyect\Manipulation\Dataframes_potencias_Componentes_Demograficos.py | Data_analysis_ML_Harmonization_Proyect\Manipulation\Dataframes_potencias_Rois_demograficos.py
3. Data_analysis_ML_Harmonization_Proyect\Manipulation\Borrar_datos_atipicos_potencias.py
4. Data_analysis_ML_Harmonization_Proyect\Manipulation\Dataframes_SL_Coherencia_Entropy_Cross.py
5. eeg_harmonization\misc\neuroharmonaze.py
6. Data_analysis_ML_Harmonization_Proyect\Manipulation\unirfeatherharmonize.py
7. Data_analysis_ML_Harmonization_Proyect\Manipulation\Graficos_power_sl_coherencia_entropia_cross.py
8. Data_analysis_ML_Harmonization_Proyect\Manipulation\graficos_data_harmonized.py
9. Data_analysis_ML_Harmonization_Proyect\Manipulation\training_script.py

*old*
9. ML_models_G1_ic_sovaharmony.py
10. ML_models_G1_ic_neuroHarmonize.py

* Los pasos 7,8,9 y 10 pueden ejecutarse simultáneamente sin necesidad de esperar los resultados de los pasos anteriores
```
  ## Refereed article
### 1.	Refereed article
*Title of article:* 	Tackling EEG Test-Retest Reliability with a Pre-Processing Pipeline based on ICA and Wavelet-ICA.<br>
*Author(s):* 	Henao Isaza V, Cadavid Castro V, Zapata Saldarriaga L, Mantilla-Ramos Y, Tobón Quintero C, Suarez Revelo J, Ochoa Gómez J.<br>
*Title of publication:* 	Authorea Preprints<br>
*ISSN:* 	Pre-print<br>
*Volume/Issue and page number:* 	Pre-print<br>
*Date of publication or accepted for publication:* 	June 2023<br>
*Peer review proof:* 	Listed on the Scopus database<br>
*Scopus Author ID:* 57209539748<br>

*URL to article:* 	https://doi.org/10.22541/au.168570191.12788016/v1<br>

### 2.	Refereed article
*Title of article:* 	Longitudinal Analysis of qEEG in Subjects with Autosomal Dominant Alzheimer's Disease due to PSEN1-E280A Variant.<br>
*Author(s):* 	Aguillon, D., Guerrero, A., Vasquez, D., Cadavid, V., Henao, V., Suarez, X., ... & Ochoa, J. F.<br>
*Title of publication:* 	Alzheimer's Association International Conference. ALZ.<br>
*ISSN:* 	NA<br>
*Volume/Issue and page number:* 	NA<br>
*Date of publication or accepted for publication:* 	December 2023<br>
*Peer review proof:* 	NA<br>
*URL to article:* 	https://alz-journals.onlinelibrary.wiley.com/doi/abs/10.1002/alz.083226<br>

### 3.	Refereed article
*Title of article:* 	Spectral features of resting-state EEG in Parkinson's Disease: a multicenter study using functional data analysis<br>
*Author(s):* 	Alberto Jaramillo-Jimenez, Diego A Tovar-Rios, Johann Alexis Ospina, Yorguin-Jose Mantilla-Ramos, Daniel Loaiza-López, Verónica Henao Isaza, Luisa María Zapata Saldarriaga, Valeria Cadavid Castro, Jazmin Ximena Suarez-Revelo, Yamile Bocanegra, Francisco Lopera, David Antonio Pineda-Salazar, Carlos Andrés Tobón Quintero, John Fredy Ochoa-Gomez, Miguel Germán Borda, Dag Aarsland, Laura Bonanni, Kolbjørn Brønnick<br>
*Title of publication:* 	Clinical Neurophysiology<br>
*ISSN:* 	1388-2457<br>
*Volume/Issue and page number:* 	Volume 151, July 2023, Pages 28-40<br>
*Date of publication or accepted for publication:* 	April 2023<br>
*Peer review proof:* 	Listed on the Scopus database<br>
*Scopus Author ID:* 57209539748<br>

*URL to article:* 	https://www.sciencedirect.com/science/article/pii/S1388245723005989<br>

