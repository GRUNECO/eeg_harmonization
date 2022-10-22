from sovaharmony.processing import harmonize 
from sovaharmony.postprocessing import features
from sovaharmony.getDataframes import get_dataframe_prep
from sovaharmony.getDataframes import get_dataframe_wica
from sovaharmony.getDataframes import get_dataframe_powers
from sovaharmony.getDataframes import get_dataframe_reject
from sovaharmony.getDataframes import get_dataframe_powers
from sovaharmony.datasets import BIOMARCADORES_CE as DATA    
import time 

THE_DATASETS=[DATA]
for dataset in THE_DATASETS:
    # Preprocessing pipeline
    start = time.perf_counter()
    process=harmonize(dataset,fast_mode=False)
    final = time.perf_counter()
    print('TIME PREPROCESSING:::::::::::::::::::', final-start)

    # Postprocessing pipeline (extraction of features)
    start = time.perf_counter()
    postprocess=features(dataset)
    final = time.perf_counter()
    print('TIME POSTPROCESSING:::::::::::::::::::', final-start)

    start = time.perf_counter()
    # Preprocessing 
    get_dataframe_prep(dataset)
    get_dataframe_wica(dataset)
    get_dataframe_reject(dataset)
    # Extraction of features 
    get_dataframe_powers(dataset,mode="channels",stage=None)
    get_dataframe_powers(dataset,mode="channels",stage="norm")
    get_dataframe_powers(dataset,mode="components",stage=None)
    get_dataframe_powers(dataset,mode="components",stage="norm")
    
    final = time.perf_counter()
    print('TIME CREATE FEATHERS:::::::::::::::::::', final-start)
    #get_dataframe_sl(dataset,mode='ROIs',ROIs=dataset['ROIs'])
    #get_dataframe_mean_sl(dataset)
    
    




