from sovaharmony.preprocessing import harmonize 
#from sovaharmony.postprocessingprep import features
from sovaharmony.postprocessing import features
from sovaharmony.data_structure.getDataframes import get_dataframe_prep
from sovaharmony.data_structure.getDataframes import get_dataframe_wica
from sovaharmony.data_structure.getDataframes import get_dataframe_reject
from sovaharmony.data_structure.query_derivatives import get_dataframe_columnsIC
from sovaharmony.data_structure.query_derivatives import get_dataframe_columnsROI
from sovaharmony.utils import * 
from sovaharmony.datasets import Estudiantes2021 as DATA    
import time 

THE_DATASETS=[DATA]
for dataset in THE_DATASETS:
    #Preprocessing pipeline
    start = time.perf_counter()
    process=harmonize(dataset,fast_mode=False)
    final = time.perf_counter()
    print('TIME PREPROCESSING:::::::::::::::::::', final-start)

    # Postprocessing pipeline (extraction of features)
    start = time.perf_counter()
    postprocess=features(dataset)
    final = time.perf_counter()
    print('TIME POSTPROCESSING:::::::::::::::::::', final-start)

    # Preprocessing files 
    start = time.perf_counter()
    get_dataframe_prep(dataset)
    get_dataframe_wica(dataset)
    get_dataframe_reject(dataset)
    
    path=r'D:\XIMENA\BIDS\Estudiantes\derivatives\sovaharmony'
    metricas=['entropy','cohfreq','power','sl','crossfreq']
    for i in metricas:
        data_IC=get_dataframe_columnsIC(dataset,feature=i)
        data_ROI=get_dataframe_columnsROI(dataset,feature=i)

        """Conversion of dataframes to perform the different SL, coherence, entropy, cross frequency, etc. graphs"""
        if i=='power':
            dataframe_long_roi(data_ROI,i,columns=columns_powers_rois,name="data_long_power_roi",path=path)
            dataframe_long_components(data_IC,'Power',columns=columns_powers_ic,name="data_long_power_components",path=path)
        
        elif i == 'entropy':
            dataframe_long_roi(data_ROI,type='Entropy',columns=columns_entropy_rois,name="data_long_entropy_roi",path=path)
            dataframe_long_components(data_IC,type='Entropy',columns=columns_entropy_ic,name="data_long_entropy_components",path=path)
        
        elif i == 'cohfreq':
            dataframe_long_roi(data_ROI,type='Coherence',columns=columns_coherence_roi,name="data_long_coherence_roi",path=path)
            dataframe_long_components(data_IC,type='Coherence',columns=columns_coherence_ic,name="data_long_coherence_components",path=path)
        elif i == 'sl':
            dataframe_long_roi(data_ROI,type='SL',columns=columns_SL_roi,name="data_long_sl_roi",path=path)
            dataframe_long_components(data_IC,type='SL',columns=columns_SL_ic,name="data_long_sl_components",path=path)
        elif i== 'crossfreq':
            columns_cross_roi=data_ROI.columns.tolist()
            for i in ['participant_id', 'group', 'visit', 'condition','database']:
                columns_cross_roi.remove(i)

            columns_cross_ic=data_IC.columns.tolist()
            columns_cross_ic.remove('participant_id')

            dataframe_long_cross_roi(data_ROI,type='Cross Frequency',columns=columns_cross_roi,name="data_long_crossfreq_roi",path=path)
            dataframe_long_cross_ic(data_IC,type='Cross Frequency',columns=columns_cross_ic,name="data_long_crossfreq_components",path=path)
            



    




