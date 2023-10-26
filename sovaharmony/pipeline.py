from sovaharmony.preprocessing import harmonize 
from sovaharmony.postprocessing import features
from sovaharmony.data_structure.getDataframes import get_dataframe_prep
from sovaharmony.data_structure.getDataframes import get_dataframe_wica
from sovaharmony.data_structure.getDataframes import get_dataframe_reject
from sovaharmony.data_structure.query_derivatives import get_dataframe_columnsIC
from sovaharmony.data_structure.query_derivatives import get_dataframe_columns_sensors
from sovaharmony.utils import * 
import time 

def pipeline (THE_DATASETS=list,prep=False,post=False,portables=False,tmontage=str,prepdf=False,propdf=False,spatial_matrix=list,metrics=list,IC=False, Sensors=False,OVERWRITE= False,bands=dict,norm='False'):
    '''
    Input
        - THE_DATASETS: list
        - prep: boolean
        - portables: boolean 
        - tmontage: str
            If tmontage is None select all channels  
        - prepdf: boolean
        - propdf: boolean
        - spatial_matrix: list
            ['58x25']
        - metricas:list
            ['cohfreq','entropy','power','sl','crossfreq','osc','irasa']
        - IC: boolean 
        - Sensors: boolean
        - OVERWRITE: boolean
        - bands: dict 
    '''
    for dataset in THE_DATASETS:
        path=dataset['input_path']+'/derivatives'
        ## Preprocessing pipeline
        if prep:
            start = time.perf_counter()
            harmonize(dataset,fast_mode=False)
            final = time.perf_counter()
            print('TIME PREPROCESSING:::::::::::::::::::'+ dataset['input_path']+ dataset['layout']['task'], final-start)

        ## Postprocessing pipeline (extraction of features)
        if post:
            if not None in spatial_matrix: # Enfoque para sacar las features in ICs
                for sm in spatial_matrix:
                    start = time.perf_counter()
                    features(dataset,def_spatial_filter=sm,portables=portables,montage_select=tmontage,OVERWRITE = OVERWRITE,bands=bands)
                    final = time.perf_counter()
                    print('TIME POSTPROCESSING:::::::::::::::::::'+ dataset['input_path']+ dataset['layout']['task'], final-start)
            
            elif None in spatial_matrix: # Enfoque para sacar las features pero en sensors
                for sm in spatial_matrix:
                    features(dataset,def_spatial_filter=sm,portables=portables,montage_select=tmontage,OVERWRITE = OVERWRITE,bands=bands)
            
        
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
                        data_IC=get_dataframe_columnsIC(dataset,feature=m,spatial_matrix=j ,norm=norm)
                        final = time.perf_counter()
                        print('TIME FEATHER IC:::::::::::::::::::'+ dataset['input_path']+ m + dataset['layout']['task'], final-start)
                    if Sensors:
                        start = time.perf_counter()
                        data_ROI=get_dataframe_columns_sensors(dataset,feature=m,norm=norm,roi=False)
                        final = time.perf_counter()
                        print('TIME FEATHER ROI:::::::::::::::::::'+ dataset['input_path']+ m + dataset['layout']['task'], final-start)
                   
                    # if m!='crossfreq':
                    #     if Sensors:
                    #         dataframe_long_roi(data_ROI,m,columns=columns_powers_rois,name="data_long_{i}_roi",path=path)
                    #     if IC:
                    #         columns_powers_ic = [palabra for palabra in list(data_IC.keys()) if palabra.startswith(m)]
                    #         dataframe_long_components(data_IC,m,columns=columns_powers_ic,name="data_long_{i}_components",path=path,spatial_matrix=j)
                    #         print(f'Done! {m}')

                    # if m== 'crossfreq':
                    #     columns_cross_ic = [palabra for palabra in list(data_IC.keys()) if palabra.startswith(m)]
                    #     if IC:
                    #         dataframe_long_cross_ic(data_IC,type='Cross Frequency',columns=columns_cross_ic,name="data_long_{m}_components",path=path,spatial_matrix=j)
                    #     if Sensors:
                    #         dataframe_long_cross_roi(data_ROI,type='Cross Frequency',columns=columns_cross_roi,name="data_long_{m}_roi",path=path)
                    #     #dataframe_long_components(data_IC,type='Cross Frequency',columns=columns_cross_ic,name="data_long_crossfreq_components",path=path)

