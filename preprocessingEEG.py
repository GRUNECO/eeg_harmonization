from sovaharmony.processing import harmonize 
from datasets import SRM,SRM_test


THE_DATASETS=[SRM]
for dataset in THE_DATASETS:
    process=harmonize(dataset,fast_mode=False)