from sovaharmony.pipeline import pipeline


BIOMARCADORES_CE = {
    'name':'original copy',
    'input_path':r'E:\EEG_MULTICENTER\test_bids_biomarcadores',
    'layout':{'extension':'.vhdr', 'task':'CE','suffix':'eeg', 'return_type':'filename', 'session':'V0'},
    'args':{'line_freqs':[60]},
    'group_regex':'(.+).{3}',
    'events_to_keep':None,
    'run-label':'restCE',
    'session':'V',
}

THE_DATASETS=[BIOMARCADORES_CE]
L_FREQ = 1
H_FREQ = 50
epoch_length = 5

spatial=['58x25']

metrics={'power':{'fit_params':False,'norm':'False','demographic':False},
         #'osc': {'fit_params':False,'norm':'False','demographic': False},
         #'ape': {'fit_params':True,'norm':'False' ,'demographic': False},
         #'ape': {'fit_params':False,'norm':'False','demographic': False}
         }

bands ={'Delta':(1.5,6),
        'Theta':(6,8.5),
        'Alpha-1':(8.5,10.5),
        'Alpha-2':(10.5,12.5),
        'Beta1':(12.5,18.5),
        'Beta2':(18.5,21),
        'Beta3':(21,30),
        'Gamma':(30,45)
        }

pipeline(THE_DATASETS,
         L_FREQ = L_FREQ,
         H_FREQ = H_FREQ,
         epoch_length = epoch_length,
         prep=True,# if you need preprocessing 
         post=True,# if you need postprocessing
         portables=False,# if you need reduce the number of the sensors
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