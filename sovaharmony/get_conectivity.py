from sovaharmony.coh import get_coherence_freq
from sovaharmony.sl import get_sl_freq
from sovaharmony.p_entropy import get_entropy_freq
#from sovaharmony.pme import get_pme_freq
#from sovaharmony.pme import Modulation_Bands_Decomposition,Modulation_Bands_Spectrum,Modulation_Bands_Decomposition_Hamming
#from sovaharmony.pme import Algorithm_Amplitude_Modulation_Analysis

def get_conectivity_band(signal,mode):
    bands =[[1.5,6] #delta
    ,[6,8.5] #theta
    , [8.5,10.5] #alpha1
    , [10.5,12.5] #alpha2
    , [12.5,18.5] #beta1
    , [18.5,21] #beta2
    , [21,30] #beta3
    ,[30,45] #gamma
    ]

    bands_labels = ['delta', 'theta', 'alpha-1', 'alpha-2', 'beta1', 'beta2','beta3', 'gamma']
    output_channels = {mode : {},
              'channels':signal.info['ch_names'],
              'bands':bands_labels}

    for limits,label in zip(bands,bands_labels):
        fmin = limits[0]
        fmax = limits[1]
        
        
        if mode == 'coherence':
            coherence_ = get_coherence_freq(signal,fmin=fmin,fmax=fmax,passband=True)
            output_channels['coherence'][label] = coherence_
        elif mode == 'sl':
            sl_ = get_sl_freq(signal,fmin=fmin,fmax=fmax,passband=True)
            output_channels['sl'][label] = sl_
        elif mode == 'entropy':
            entropy_ = get_entropy_freq(signal,fmin=fmin,fmax=fmax,passband=True)
            output_channels['entropy'][label] = entropy_
        #elif mode == 'pme':
        #    pme_ = get_pme_freq(signal,fmin=fmin,fmax=fmax,passband=True)
        #    output_channels['pme'][label] = pme_
        
        
    return output_channels