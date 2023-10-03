from sovaharmony.preprocessing import harmonize 
from sovaharmony.postprocessing import features
from sovaharmony.data_structure.getDataframes import get_dataframe_prep
from sovaharmony.data_structure.getDataframes import get_dataframe_wica
from sovaharmony.data_structure.getDataframes import get_dataframe_reject
from sovaharmony.data_structure.query_derivatives import get_dataframe_columnsIC
from sovaharmony.data_structure.query_derivatives import get_dataframe_columnsROI
from sovaharmony.utils import * 
import time 

def pipeline (THE_DATASETS,portables=False, prepdf=False,propdf=False,spatial_matrix=list,metrics=list,IC=False, Sensors=False):
    '''
    spatial_matrix=['58x25']
    metricas=['cohfreq','entropy','power','sl','crossfreq','osc','irasa']
    '''
    for dataset in THE_DATASETS:
        path=dataset['input_path']+'/derivatives'
        ## Preprocessing pipeline
        start = time.perf_counter()
        process=harmonize(dataset,fast_mode=False)
        final = time.perf_counter()
        print('TIME PREPROCESSING:::::::::::::::::::'+ dataset['input_path']+ dataset['layout']['task'], final-start)

        ## Postprocessing pipeline (extraction of features)
        if portables:
            montages_portatil=['openBCI','paper','cresta']
            for tmontage in montages_portatil:
                start = time.perf_counter()
                postprocess=features(dataset,def_spatial_filter='54x10',portables=portables,montage_select=tmontage)
                final = time.perf_counter()
                print('TIME POSTPROCESSING:::::::::::::::::::'+ dataset['input_path']+ dataset['layout']['task'], final-start)
        else:
            postprocess=features(dataset,def_spatial_filter='58x25',portables=portables,montage_select=None)
        
        if prepdf:
            ## Preprocessing dataframes 
            start = time.perf_counter()
            get_dataframe_prep(dataset)
            get_dataframe_wica(dataset)
            get_dataframe_reject(dataset)
            final = time.perf_counter()

        if propdf:
            for m in metrics:
                for j in spatial_matrix:
                    if IC: 
                        start = time.perf_counter()
                        data_IC=get_dataframe_columnsIC(dataset,feature=i,spatial_matrix=j ,norm='False')
                        final = time.perf_counter()
                        print('TIME FEATHER IC:::::::::::::::::::'+ dataset['input_path']+ i + dataset['layout']['task'], final-start)
                    if Sensors:
                        start = time.perf_counter()
                        data_ROI=get_dataframe_columnsROI(dataset,feature=i)
                        final = time.perf_counter()
                        print('TIME FEATHER ROI:::::::::::::::::::'+ dataset['input_path']+ i + dataset['layout']['task'], final-start)
                   
                    if m!='crossfreq':
                        if Sensors:
                            dataframe_long_roi(data_ROI,m,columns=columns_powers_rois,name="data_long_{i}_roi",path=path)
                        if IC:
                            columns_powers_ic = [palabra for palabra in list(data_IC.keys()) if palabra.startswith(m)]
                            dataframe_long_components(data_IC,m,columns=columns_powers_ic,name="data_long_{i}_components",path=path,spatial_matrix=j)
                            print(f'Done! {m}')

                    if m== 'crossfreq':
                        columns_cross_ic = [palabra for palabra in list(data_IC.keys()) if palabra.startswith(m)]
                        if IC:
                            dataframe_long_cross_ic(data_IC,type='Cross Frequency',columns=columns_cross_ic,name="data_long_{m}_components",path=path,spatial_matrix=j)
                        if Sensors:
                            dataframe_long_cross_roi(data_ROI,type='Cross Frequency',columns=columns_cross_roi,name="data_long_{m}_roi",path=path)
                        #dataframe_long_components(data_IC,type='Cross Frequency',columns=columns_cross_ic,name="data_long_crossfreq_components",path=path)

