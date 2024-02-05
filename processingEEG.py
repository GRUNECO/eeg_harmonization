from sovaharmony.datasets import *
from sovaharmony.pipeline import pipeline
#from .misc.neuroharmonaze import neurosovaHarmonize

#joblib para paralelizar flujos 
# THE_DATASETS=[
#     CHBMP_54X10,
#     SRM_54X10,
#     DUQUE_54X10,
#     BIOMARCADORES_CE_54X10
#     ]

THE_DATASETS=[
        #DUQUE_Server,
        BIOMARCADORES_CE_server,
        #BIOMARCADORES_OE_server
]

spatial=['54x10']#[None]#['58x25']#['openBCI']
metrics={#'power':{'fit_params':False,'norm':'False','demographic':False},
         'osc': {'fit_params':False,'norm':'False','demographic': False},
         'ape': {'fit_params':True,'norm':'False' ,'demographic': False},
         'ape': {'fit_params':False,'norm':'False','demographic': False}
         }
# Inputs not dataset dependent
bands ={'Delta':(1.5,6),
        'Theta':(6,8.5),
        'Alpha-1':(8.5,10.5),
        'Alpha-2':(10.5,12.5),
        'Beta1':(12.5,18.5),
        'Beta2':(18.5,21),
        'Beta3':(21,30),
        #'Gamma':(30,45)
        }

pipeline(THE_DATASETS,
         prep=False,# if you need preprocessing 
         post=False,# if you need postprocessing
         portables=False,# if you need reduce the number of the sensors
         tmontage='openBCI',
         prepdf=False,
         propdf=True,
         spatial_matrix=spatial,
         metrics=metrics,
         IC=True, 
         Sensors=False,
         roi=False,
         OVERWRITE=True,
         bands=bands,
        )

# spatial=[None]
# metrics=['sl','crossfreq']
# pipeline(THE_DATASETS,
#          prep=False, 
#          post=False, 
#          portables=True, 
#          tmontage='openBCI', # select reductor montage 
#          prepdf=False, # If you need the dataframe in preprocessing
#          propdf=True, # If you need the dataframe in postprocessing
#          spatial_matrix=spatial, # Select the spatial matrix  or None in case not aplied
#          metrics=metrics, # List with the metrics extract
#          IC=False, # Select the 
#          Sensors=True,
#          OVERWRITE=True,
#          bands=bands,
#         )