from sovaharmony.processing import harmonize 
from sovaharmony.getDataframes import get_dataframe_prep,get_dataframe_wica,get_dataframe_powers,get_dataframe_reject
from datasets import SRM_test


THE_DATASETS=[SRM_test]
get_dataframe_powers(THE_DATASETS,mode="channels",stage=None)
get_dataframe_powers(THE_DATASETS,mode="channels",stage="norm")
get_dataframe_powers(THE_DATASETS,mode="components",stage=None)
get_dataframe_powers(THE_DATASETS,mode="components",stage="norm")
get_dataframe_prep(THE_DATASETS)
get_dataframe_wica(THE_DATASETS)
get_dataframe_reject(THE_DATASETS)
for dataset in THE_DATASETS:
    process=harmonize(dataset,fast_mode=False)


