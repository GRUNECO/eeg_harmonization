from sovaharmony.processing import harmonize 
from sovaharmony.getDataframes import get_dataframe_prep,get_dataframe_wica,get_dataframe_powers,get_dataframe_reject
from datasets import SRM,BIOMARCADORES,BIOMARCADORES_test


THE_DATASETS=[BIOMARCADORES,SRM]

for dataset in THE_DATASETS:
    #process=harmonize(dataset,fast_mode=False)
    get_dataframe_powers(dataset,mode="channels",stage=None)
    get_dataframe_powers(dataset,mode="channels",stage="norm")
    get_dataframe_powers(dataset,mode="components",stage=None)
    get_dataframe_powers(dataset,mode="components",stage="norm")
    get_dataframe_prep(dataset)
    get_dataframe_wica(dataset)
    get_dataframe_reject(dataset)




