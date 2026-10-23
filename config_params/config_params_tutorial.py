from sovaharmony.datasets import *

THE_DATASETS=[
    CHBMP_54X10,
    SRM_54X10
    ,DUQUE_54X10,
    BIOMARCADORES_CE_54X10
    ]

spatial=[None]##['58x25']#['openBCI']

# Inputs not dataset dependent
bands ={'Delta':(1.5,6),
        'Theta':(6,8.5),
        'Alpha-1':(8.5,10.5),
        'Alpha-2':(10.5,12.5),
        'Beta1':(12.5,18.5),
        'Beta2':(18.5,21),
        'Beta3':(21,30),
        'Gamma':(30,45)
        }

L_FREQ = 1 #high-pass frequency for detrending (def 1)
H_FREQ = 50 #low-pass frequency (def 50)
epoch_length = 5 #length of epoching in seconds (def 5)

metrics={'power':{'fit_params':False,'norm':'False','demographic':False},
         #'osc': {'fit_params':False,'norm':'False','demographic': False},
         #'ape': {'fit_params':True,'norm':'False' ,'demographic': False},
         #'ape': {'fit_params':False,'norm':'False','demographic': False}
         }