#from sovaharmony.datasets import Estudiantes2021 as DATA    
from sovaharmony.datasets import Estudiantes_CE
from sovaharmony.datasets import Estudiantes_OE
from sovaharmony.datasets import Estudiantes_T1
from sovaharmony.datasets import Estudiantes_T2
from sovaharmony.datasets import Estudiantes_T3
from sovaharmony.datasets import Residentes_CE
from sovaharmony.datasets import Residentes_OE
from sovaharmony.datasets import Residentes_T1
from sovaharmony.datasets import Residentes_T2
from sovaharmony.datasets import Residentes_T3
from sovaharmony.datasets import Estudiantes2021_OE
from sovaharmony.datasets import Estudiantes2021_CE
from sovaharmony.datasets import Estudiantes2021_T1
from sovaharmony.datasets import Estudiantes2021_T2
from sovaharmony.datasets import BIOMARCADORES_OE, BIOMARCADORES_CE, CHBMP, SRM, DUQUE
from sovaharmony.datasets import BIOMARCADORES_OE_server, BIOMARCADORES_CE_server
from sovaharmony.datasets import BIOMARCADORES_CE_54X10, CHBMP_54X10, SRM_54X10, DUQUE_54X10
from sovaharmony.datasets import test_portables
from sovaharmony.pipeline import pipeline
#from .misc.neuroharmonaze import neurosovaHarmonize


#THE_DATASETS=[
            #   Estudiantes2021_OE,
            #   Estudiantes2021_CE,
            #   Estudiantes2021_T1,
            #   Estudiantes2021_T2,
            #   Estudiantes_CE,
            #   Estudiantes_OE,
            #  Estudiantes_T1,# no da
            #   Estudiantes_T2,
            #   Estudiantes_T3,
            #   Residentes_CE,
            #   Residentes_OE,
            #   Residentes_T1,
            #   Residentes_T2,
            #  Residentes_T3,
#              ]
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
pipeline (THE_DATASETS,
          portables=False,
          prepdf=False,
          propdf=True,
          spatial_matrix=spatial,
          metrics=metrics,
          IC=True, 
          Sensors=False)