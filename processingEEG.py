from sovaharmony.preprocessing import harmonize 
from sovaharmony.postprocessing import features
from sovaharmony.data_structure.getDataframes import get_dataframe_prep
from sovaharmony.data_structure.getDataframes import get_dataframe_wica
from sovaharmony.data_structure.getDataframes import get_dataframe_reject
from sovaharmony.data_structure.query_derivatives import get_dataframe_columnsIC
from sovaharmony.data_structure.query_derivatives import get_dataframe_columnsROI
from sovaharmony.datasets import DUQUEVHI as DATA    
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

    # Preprocessing 
    get_dataframe_prep(dataset)
    get_dataframe_wica(dataset)
    get_dataframe_reject(dataset)
    metricas=['power','sl','crossfreq','entropy','cohfreq']
    for i in metricas:
        get_dataframe_columnsIC(dataset,feature=i)
        get_dataframe_columnsROI(dataset,feature=i)


    




