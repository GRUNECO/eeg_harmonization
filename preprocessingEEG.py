from sovaharmony.processing import harmonize 
<<<<<<< HEAD
from datasets import BIOMARCADORES
=======
from datasets import SRM
>>>>>>> c5511851a053fc0a4cc48e384c8d5eeaf37f8c43


THE_DATASETS=[SRM]
for dataset in THE_DATASETS:
    process=harmonize(dataset,fast_mode=False)