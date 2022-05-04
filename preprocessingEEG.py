from sovaharmony.processing import harmonize 
from datasets import BIOMARCADORES 


THE_DATASETS=[BIOMARCADORES ]
for dataset in THE_DATASETS:
    process=harmonize(dataset,fast_mode=False)