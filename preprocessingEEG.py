from sovaharmony.processing import harmonize 
from sovaharmony.postprocessing import features
from sovaharmony.getDataframes import get_dataframe_prep
from sovaharmony.getDataframes import get_dataframe_wica
from sovaharmony.getDataframes import get_dataframe_powers
from sovaharmony.getDataframes import get_dataframe_reject
from sovaharmony.getDataframes import get_dataframe_powers
from datasets import BIOMARCADORESMini as DATA    
import time 

THE_DATASETS=[DATA]
for dataset in THE_DATASETS:
    start = time.perf_counter()
    process=harmonize(dataset,fast_mode=False)
    final = time.perf_counter()
    print('TIME PREPROCESSING:::::::::::::::::::', final-start)
    start = time.perf_counter()
    postprocess=features(dataset)
    final = time.perf_counter()
    print('TIME POSTPROCESSING:::::::::::::::::::', final-start)
    start = time.perf_counter()
    get_dataframe_prep(dataset)
    get_dataframe_wica(dataset)
    get_dataframe_reject(dataset)
    get_dataframe_powers(dataset,mode="channels",stage=None)
    get_dataframe_powers(dataset,mode="channels",stage="norm")
    get_dataframe_powers(dataset,mode="components",stage=None)
    get_dataframe_powers(dataset,mode="components",stage="norm")
    final = time.perf_counter()
    print('TIME CREATE FEATHERS:::::::::::::::::::', final-start)




