
#from sovaharmony.features import get_sl_freq
from sovaharmony.coh import get_coherence_freq
from sovaharmony.p_entropy import get_entropy_freq
#from sovaharmony.pme import get_pme_freq
from sovaflow.utils import cfg_logger
from sovaharmony.processing import get_derivative_path
from sovaharmony.processing import write_json
from bids import BIDSLayout
import mne
import json
import os
from sovaharmony.features import get_derivative
from sovaharmony.spatial import get_spatial_filter
import numpy as np
from sovaharmony.pme import Amplitude_Modulation_Analysis
import time
import traceback
OVERWRITE = False # Ojo con esta variable, es para obligar a sobreescribir los archivos
# en general deberia estar en False
def features(THE_DATASET):
    # Inputs not dataset dependent
    def_spatial_filter='58x25'
    bands ={'delta':(1.5,6),
            'theta':(6,8.5),
            'alpha-1':(8.5,10.5),
            'alpha-2':(10.5,12.5),
            'beta1':(12.5,18.5),
            'beta2':(18.5,21),
            'beta3':(21,30),
            'gamma':(30,45)}
    if THE_DATASET.get('spatial_filter',def_spatial_filter):
        spatial_filter = get_spatial_filter(THE_DATASET.get('spatial_filter',def_spatial_filter))
    input_path = THE_DATASET.get('input_path',None)
    layout_dict = THE_DATASET.get('layout',None)
    e = 0
    archivosconerror = []
    # Static Params
    pipelabel = '['+THE_DATASET.get('run-label', '')+']'
    layout = BIDSLayout(input_path)
    bids_root = layout.root
    eegs = layout.get(**layout_dict)
    pipeline = 'sovaharmony'
    derivatives_root = os.path.join(layout.root,'derivatives',pipeline)
    log_path = os.path.join(derivatives_root,'code')
    os.makedirs(log_path, exist_ok=True)
    logger,currentdt = cfg_logger(log_path)
    desc_pipeline = "sovaharmony, a harmonization eeg pipeline using the bids standard"
    num_files = len(eegs)
    for i,eeg_file in enumerate(eegs):
        #process=str(i)+'/'+str(num_files)
        logger.info(f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}")

        reject_path = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
        norm_path = get_derivative_path(layout,eeg_file,'huber'+pipelabel,'eeg','.fif',bids_root,derivatives_root)

        json_dict = {"Description":desc_pipeline,"RawSources":[eeg_file.replace(bids_root,'')],"Configuration":THE_DATASET}
        
        features_tuples=[
            ('power',{'bands':bands}),
            ('sl',{'bands':bands}),
            ('cohfreqs',{'window':3,'bands':None}),
            ('cohbands',{'window':3,'bands':bands}),
            ('entropy',{'bands':bands,'D':3}),
            ('crossfreq',{'bands':bands}),
        ]
        times_strings = []
        for feature,kwargs in features_tuples:
            try:
                for sf in [None, spatial_filter]:
                    for norm_ in [True,False]:
                        if sf is not None:
                            sf_label = f'ics[{spatial_filter["name"]}]'
                        else:
                            sf_label = 'sensors'
                        feature_suffix = f'space-{sf_label}_norm-{norm_}_{feature}'
                        feature_path = get_derivative_path(layout,eeg_file,pipelabel,feature_suffix,'.txt',bids_root,derivatives_root)
                        os.makedirs(os.path.split(feature_path)[0], exist_ok=True)

                        if OVERWRITE or not os.path.isfile(feature_path):
                            if norm_:
                                signal = mne.read_epochs(norm_path)
                            else:
                                signal = mne.read_epochs(reject_path)
                            start = time.perf_counter()
                            val_dict = get_derivative(signal,feature=feature,kwargs=kwargs,spatial_filter=sf)
                            final = time.perf_counter()
                            tstring = f'TIME {feature_suffix}:::::::::::::::::::{final-start}'
                            times_strings.append(tstring)
                            print(tstring)
                            write_json(val_dict,feature_path)
                            write_json(json_dict,feature_path.replace('.txt','.json'))
                        else:
                            logger.info(f'{feature_path}) already existed, skipping...')
            except Exception as error:
                e+=1
                logger.exception(f'Error for {eeg_file}-{feature_path}')
                archivosconerror.append((eeg_file,feature_path))
                print(error)
                print(traceback.format_exc())
                pass
        [print(x) for x in times_strings]
    return