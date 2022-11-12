from sovaharmony.get_conectivity import get_conectivity_band
from sovaharmony.sl import get_sl_freq
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
from sovaflow.flow import get_ics_power_derivatives
from sovaflow.flow import get_power_derivates
from sovaflow.utils import get_spatial_filter
import numpy as np
from sovaharmony.pme import Amplitude_Modulation_Analysis
import time

def features(THE_DATASET):
    # Inputs not dataset dependent
    def_spatial_filter='58x25'
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
        try:
            logger.info(f"File {i+1} of {num_files} ({(i+1)*100/num_files}%) : {eeg_file}")

            reject_path = get_derivative_path(layout,eeg_file,'reject'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
            power_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'powers','.txt',bids_root,derivatives_root)
            icpowers_path = get_derivative_path(layout,eeg_file,'component'+pipelabel,'powers','.txt',bids_root,derivatives_root)
            power_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'powers_norm','.txt',bids_root,derivatives_root)
            icpowers_norm_path = get_derivative_path(layout,eeg_file,'component'+pipelabel,'powers_norm','.txt',bids_root,derivatives_root)
            norm_path = get_derivative_path(layout,eeg_file,'huber'+pipelabel,'eeg','.fif',bids_root,derivatives_root)
            sl_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'sl_norm','.txt',bids_root,derivatives_root)
            sl_band_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'sl_band_norm','.txt',bids_root,derivatives_root)
            coherence_norm_path  = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'coherence_norm','.txt',bids_root,derivatives_root)
            coherence_band_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'coherence_band_norm','.txt',bids_root,derivatives_root)
            entropy_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'entropy_norm','.txt',bids_root,derivatives_root)
            entropy_band_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'entropy_band_norm','.txt',bids_root,derivatives_root)
            cross_frequency_norm_path = get_derivative_path(layout,eeg_file,'channel'+pipelabel,'cross_frequency_norm','.txt',bids_root,derivatives_root)
            os.makedirs(os.path.split(power_path)[0], exist_ok=True)

            json_dict = {"Description":desc_pipeline,"RawSources":[eeg_file.replace(bids_root,'')],"Configuration":THE_DATASET}

            if os.path.isfile(power_path):
                logger.info(f'{power_path}) already existed, skipping...')
            else:
                signal = mne.read_epochs(reject_path)
                startpower = time.perf_counter()
                power_dict = get_power_derivates(signal)
                finalpower = time.perf_counter()
                print('TIME POWER:::::::::::::::::::', finalpower-startpower)
                write_json(power_dict,power_path)
                write_json(json_dict,power_path.replace('.txt','.json'))
            
            if os.path.isfile(power_norm_path):
                logger.info(f'{power_norm_path}) already existed, skipping...')             
            else:
                signal_normas = mne.read_epochs(norm_path)
                startpowernorm = time.perf_counter()
                power_norm = get_power_derivates(signal_normas)
                finalpowernorm = time.perf_counter()
                print('TIME POWER NORM:::::::::::::::::::', finalpowernorm-startpowernorm)
                write_json(power_norm,power_norm_path)
                write_json(json_dict,power_norm_path.replace('.txt','.json'))
            
            if not os.path.isfile(icpowers_norm_path) and spatial_filter is not None:
                signal_normas = mne.read_epochs(norm_path)
                starticpowernorm = time.perf_counter()
                ic_powers_dict_norm = get_ics_power_derivatives(signal_normas,spatial_filter)
                finalicpowernorm = time.perf_counter()
                print('TIME IC POWER NORM:::::::::::::::::::', finalicpowernorm-starticpowernorm)
                write_json(ic_powers_dict_norm,icpowers_norm_path)
                write_json(json_dict,icpowers_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{icpowers_path}) already existed or no spatial filter given, skipping...')
  
            if not os.path.isfile(icpowers_path) and spatial_filter is not None:
                signal = mne.read_epochs(reject_path)
                starticpower = time.perf_counter()
                ic_powers_dict = get_ics_power_derivatives(signal,spatial_filter)
                finalicpower = time.perf_counter()
                print('TIME IC POWER:::::::::::::::::::', finalicpower-starticpower)
                write_json(ic_powers_dict,icpowers_path)
                write_json(json_dict,icpowers_path.replace('.txt','.json'))

            else:
                logger.info(f'{icpowers_path}) already existed or no spatial filter given, skipping...')

            if not os.path.isfile(sl_norm_path):
                raw_data = mne.read_epochs(norm_path)
                startsl = time.perf_counter()
                sl = get_sl_freq(raw_data)
                finalsl = time.perf_counter()
                print('TIME SL:::::::::::::::::::', finalsl-startsl)
                sl_dict = {'sl' : sl,'channels':raw_data.info['ch_names']}
                write_json(sl_dict,sl_norm_path)
                write_json(json_dict,sl_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{sl_norm_path}) already existed, skipping...')

            if not os.path.isfile(sl_band_norm_path):
                raw_data = mne.read_epochs(norm_path)
                startbandsl = time.perf_counter()
                sl_band_dict = get_conectivity_band(raw_data,mode='sl')
                finalbandsl = time.perf_counter()
                print('TIME BANDS SL:::::::::::::::::::', finalbandsl-startbandsl)
                write_json(sl_band_dict,sl_band_norm_path)
                write_json(json_dict,sl_band_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{sl_norm_path}) already existed, skipping...')

            if not os.path.isfile(coherence_norm_path):
                raw_data = mne.read_epochs(norm_path)
                startcoherence = time.perf_counter()
                fc,Cxyc = get_coherence_freq(raw_data)
                finalcoherence = time.perf_counter()
                print('TIME COHERENCE:::::::::::::::::::', finalcoherence-startcoherence)
                coherence_dict = {'fc' : fc,'Cxyc' : Cxyc ,'channels':raw_data.info['ch_names']}
                write_json(coherence_dict,coherence_norm_path)
                write_json(json_dict,coherence_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{coherence_norm_path}) already existed, skipping...')

            if not os.path.isfile(coherence_band_norm_path):
                raw_data = mne.read_epochs(norm_path)
                startbandscoherence = time.perf_counter()
                coherence_band_dict = get_conectivity_band(raw_data,mode='coherence')
                finalbandscoherence = time.perf_counter()
                print('TIME BANDS COHERENCE:::::::::::::::::::', finalbandscoherence-startbandscoherence)
                write_json(coherence_band_dict,coherence_band_norm_path)
                write_json(json_dict,coherence_band_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{coherence_norm_path}) already existed, skipping...')

            if not os.path.isfile(entropy_norm_path):
                raw_data = mne.read_epochs(norm_path)
                startentropy = time.perf_counter()
                mean_entropy = get_entropy_freq(raw_data) 
                finalentropy = time.perf_counter()
                print('TIME ENTROPY:::::::::::::::::::', finalentropy-startentropy)
                entropy_dict = {'mean_entropy' : mean_entropy,'channels':raw_data.info['ch_names']}
                write_json(entropy_dict,entropy_norm_path)
                write_json(json_dict,entropy_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{entropy_norm_path}) already existed, skipping...')

            if not os.path.isfile(entropy_band_norm_path):
                raw_data = mne.read_epochs(norm_path)
                startbandsentropy = time.perf_counter()
                entropy_band_dict = get_conectivity_band(raw_data,mode='entropy')
                finalbandsentropy = time.perf_counter()
                print('TIME BANDS ENTROPY:::::::::::::::::::', finalbandsentropy-startbandsentropy)
                write_json(entropy_band_dict,entropy_band_norm_path)
                write_json(json_dict,entropy_band_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{entropy_norm_path}) already existed, skipping...')

            if not os.path.isfile(cross_frequency_norm_path):
                raw_data = mne.read_epochs(norm_path)
                startcross = time.perf_counter()
                cross_frequency = get_conectivity_band(raw_data,mode='pme')
                finalcross = time.perf_counter()
                print('TIME CROSS FREQUENCY:::::::::::::::::::', finalcross-startcross)
                cross_frequency_dict = {'cross_frequency' : cross_frequency,'channels':raw_data.info['ch_names']}
                write_json(cross_frequency_dict,cross_frequency_norm_path)
                write_json(json_dict,cross_frequency_norm_path.replace('.txt','.json'))
            else:
                logger.info(f'{entropy_norm_path}) already existed, skipping...')
       
            try:
                print('TIME POWER:::::::::::::::::::', finalpower-startpower)
            except:
                pass
                print('TIME POWER NORM:::::::::::::::::::', finalpowernorm-startpowernorm)
            try:
                print('TIME IC POWER NORM:::::::::::::::::::', finalicpowernorm-starticpowernorm)
            except:
                pass
                print('TIME IC POWER:::::::::::::::::::', finalicpower-starticpower)
            try:
                print('TIME SL:::::::::::::::::::', finalsl-startsl)
            except:
                pass
                print('TIME BANDS SL:::::::::::::::::::', finalbandsl-startbandsl)
            try:
                print('TIME COHERENCE:::::::::::::::::::', finalcoherence-startcoherence)
            except:
                pass
                print('TIME BANDS COHERENCE:::::::::::::::::::', finalbandscoherence-startbandscoherence)
            try:
                print('TIME ENTROPY:::::::::::::::::::', finalentropy-startentropy)
            except:
                pass
                print('TIME BANDS ENTROPY:::::::::::::::::::', finalbandsentropy-startbandsentropy)
            try:
                print('TIME CROSS FREQUENCY:::::::::::::::::::', finalcross-startcross)
            except:
                pass
        except Exception as error:
            e+=1
            logger.exception(f'Error for {eeg_file}')
            archivosconerror.append(eeg_file)
            print(error)
            pass
    
    return