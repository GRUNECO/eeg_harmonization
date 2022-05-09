from sovaharmony.processing import harmonize 
from datasets import SRM


THE_DATASETS=[SRM]
for dataset in THE_DATASETS:
    process=harmonize(dataset,fast_mode=False)