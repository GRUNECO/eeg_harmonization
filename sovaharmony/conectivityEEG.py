from sovaharmony.conectivity import sl_connectivity
from datasets import BIOMARCADORES_OE as DATA    
import time 

THE_DATASETS=[DATA]
for dataset in THE_DATASETS:
    start = time.perf_counter()
    sl_connectivity(dataset,fast_mode=False)
    final = time.perf_counter()
    print('TIME PREPROCESSING:::::::::::::::::::', final-start)
    start = time.perf_counter()
    final = time.perf_counter()
    print('TIME CREATE FEATHERS:::::::::::::::::::', final-start)