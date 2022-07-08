from sovaharmony.processing import harmonize 
from sovaharmony.getDataframes import get_dataframe_prep,get_dataframe_wica,get_dataframe_powers,get_dataframe_reject
from datasets import CHBMP      
import time 

THE_DATASETS=[CHBMP]
for dataset in THE_DATASETS:
    start = time.perf_counter()
    process=harmonize(dataset,fast_mode=False)
    final = time.perf_counter()
    print('TIME PREPROCESSING:::::::::::::::::::', final-start)
    start = time.perf_counter()
    get_dataframe_powers(dataset,mode="channels",stage=None)
    get_dataframe_powers(dataset,mode="channels",stage="norm")
    get_dataframe_powers(dataset,mode="components",stage=None)
    get_dataframe_powers(dataset,mode="components",stage="norm")
    get_dataframe_prep(dataset)
    get_dataframe_wica(dataset)
    get_dataframe_reject(dataset)
    final = time.perf_counter()
    print('TIME CREATE FEATHERS:::::::::::::::::::', final-start)




