from sovaharmony.pipeline import pipeline
from config_params.config_params_tutorial import * 
#from .misc.neuroharmonaze import neurosovaHarmonize


pipeline(THE_DATASETS,
         L_FREQ = L_FREQ,
         H_FREQ = H_FREQ,
         epoch_length = epoch_length,
         prep=False,# if you need preprocessing 
         post=True,# if you need postprocessing
         portables=True,# if you need reduce the number of the sensors
         prepdf=False,
         propdf=True,
         spatial_matrix=spatial,
         metrics=metrics,
         IC=False, 
         Sensors=True,
         roi=False,
         OVERWRITE=True,
         bands=bands,
        )
