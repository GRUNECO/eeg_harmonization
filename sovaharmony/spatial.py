from scipy.io import loadmat
import sovaflow.utils as us
import matplotlib.pyplot as plt
import os
import numpy as np
from sovaharmony.metrics.features import channels_reduction

F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
ROIs = [F,C,PO,T]

# A ROI COULD BE A SPATIAL FILTER

# TODO: Pass spatial filters to sovaharmony

def get_spatial_filter(name='62x19',portables=False,montage_select=None):
    """
    Returns the default spatial filter of the module.
    
    Parameters:
        - name: str
            Name of spatial matrix, for example:
                62x19
                54x25
                54x10
                
        - portables: Bool
            Use portables in False, when use use the high density, for example 54x10 or 54x25
            If you need used the spatial matrix portatil, use portables in True
            
        - montage_select: str
            string associate to the name montage reduction, for example:
                cresta
                openBCI
                paper
            If you need add other configuration, added to the dictionary 
    
    Returns:
        sf: dictionary 
            A, W, Mixing and Demixing Matrices of the default spatial filter of the module.
        
    
    """
    if name is None:
        return None
    # How sure are we that the order of the channels of matlab is the same as of python?
    mat_contents = loadmat(os.path.join(os.path.dirname(os.path.abspath(__file__)),'spatial_filters','spatial_filter__'+name+'.mat'))
    W = mat_contents['W']
    A = mat_contents['A']
    ch_names = [x[0] for x in mat_contents['ch_names'][0,:].tolist()]
    sf = {'A':A,'W':W,'ch_names':ch_names,'name':name}
    if portables:
        montage_select=montage_select
        sf['ch_names']=[x.replace(' ','') for x in sf['ch_names']]
        index_ch_portables=[sf['ch_names'].index(channels_reduction[montage_select][i]) for i in range(len(channels_reduction[montage_select]))]
        #comp_select=[0,1,2,3,4,6,7,9]
        comp_select = [0,1,2,4,5,7,8,9]
        A=sf['A'][index_ch_portables,:] # Select channels, rows
        A=A[:,[comp_select]] # Select components, columns
        A=np.squeeze(A)
        W=sf['W'][:,index_ch_portables] # Select channels, rows
        W=W[[comp_select],:] # Select components, columns
        W=np.squeeze(W)
        sf={'A':A,'W':W,'ch_names':channels_reduction[montage_select],'name':montage_select}
        return sf
    else:   
        return sf

def plot_spatial_filter(name='62x19'):
    #ch_names = [us.chn_name_mapping(x) for x in ch_names]
    montage_kind = 'standard_1020'
    A,W,ch_names = get_spatial_filter(name)
    #%% Todas las componentes
    figMany = us.topomap(A,W,ch_names,cmap='seismic',show=False)
    plt.show()
