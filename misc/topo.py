import numpy as np
from sys import path
import os
path.append(os.path.join(os.path.dirname(os.path.abspath(__file__))))
import sovaflow.utils as us
import matplotlib.pyplot as plt
from sovaharmony.spatial import get_spatial_filter



#A,W,ch_names = us.get_spatial_filter('58x25')
A,W,ch_names = us.get_spatial_filter('54x10')
# sf=get_spatial_filter('54x10',portables=True,montage_select='cresta')
# A=sf['A']
# W=sf['W']
# ch_names=sf['ch_names']
ch_names=[x.replace(' ','') for x in ch_names]
comp = 0

#%% Solo una componente
A_ = np.expand_dims(A[:,comp],axis=-1)
W_ = np.expand_dims(W[comp,:],axis=0)
figSingle = us.topomap(A_,W_,ch_names,cmap='seismic',show=True)
plt.show()
#%% Uno por uno
fig3 = us.single_topomap(A[:,comp],ch_names,show=True,label='1',show_names=False)
plt.show()
label = ['1', '2', '3', '4', '5', '6', '7', '8', '9','10']
#%% Todas las componentes
figMany = us.topomap(A,W,ch_names,cmap='seismic',show=False,ncols=5,labels=label)
plt.show()