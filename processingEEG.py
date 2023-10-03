from sovaharmony.datasets import BIOMARCADORES_OE, BIOMARCADORES_CE, CHBMP, SRM, DUQUE
from sovaharmony.datasets import BIOMARCADORES_OE_server, BIOMARCADORES_CE_server
from sovaharmony.datasets import BIOMARCADORES_CE_54X10, CHBMP_54X10, SRM_54X10, DUQUE_54X10
from sovaharmony.datasets import test_portables
from sovaharmony.pipeline import pipeline
from .misc.neuroharmonaze import neurosovaHarmonize

#joblib para paralelizar flujos 
# THE_DATASETS=[
#     CHBMP_54X10,
#     SRM_54X10,
#     DUQUE_54X10,
#     BIOMARCADORES_CE_54X10
#     ]

THE_DATASETS=[
    BIOMARCADORES_CE_server,
    BIOMARCADORES_OE_server
]

spatial=['58x25']
metrics=['osc']

# Inputs not dataset dependent
bands ={'delta':(1.5,6),
        'theta':(6,8.5),
        'alpha-1':(8.5,10.5),
        'alpha-2':(10.5,12.5),
        'beta1':(12.5,18.5),
        'beta2':(18.5,21),
        'beta3':(21,30),
        'gamma':(30,45)
        }

pipeline (THE_DATASETS,
          portables=False,
          prepdf=False,
          propdf=True,
          spatial_matrix=spatial,
          metrics=metrics,
          IC=True, 
          Sensors=False,
          OVERWRITE=False,
          bands=bands
          )