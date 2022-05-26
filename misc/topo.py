import numpy as np
import mne
from sys import path
import os
#path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))
import sovaflow.utils as us
import matplotlib.pyplot as plt

#ch_names = [us.chn_name_mapping(x) for x in ch_names]
montage_kind = 'standard_1020'
A,W,ch_names = us.get_spatial_filter('58x25')

#comp = 0

#%% Solo una componente
for comp in range(len(A)):
    A_ = np.expand_dims(A[:,comp],axis=-1)
    W_ = np.expand_dims(W[comp,:],axis=0)
    figSingle = us.topomap(A_,W_,ch_names,cmap='seismic',show=False)
    plt.show()
#%% Otra forma
#fig3 = us.single_topomap(A[:,comp],ch_names,show=True,label='1',show_names=False)
#plt.show()

#%% Todas las componentes
#figMany = us.topomap(A,W,ch_names,cmap='seismic',show=False)
#plt.show()