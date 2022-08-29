"""
@author: Brayan Hoyos Madera, Universidad de Antioquia, leobahm72@gmail.com

"""

from lib2to3.pgen2.token import LSQB
from time import time
from load_cnt import load
from sl import get_sl
from matplotlib import pyplot as plt
import numpy as np

path = r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_desc-norm_eeg"
#capture the start time
star_time = time()
#Read input data
'''data, fs = load_continuos(path)
sl = get_sl(data, fs)
#For parameter control
#sl = get_sl(data, fs, time_delay=4, w1=16, w2=215, pref=0.05)
M1 =100*sl
M1[np.diag_indices_from(M1)] = 1
#Show sl data
print(M1)
plt.pcolor(M1,cmap=plt.cm.Blues)
plt.colorbar()
plt.ylabel('Channels')
plt.xlabel('Channels')
plt.show()
#show the execution time
print("The execution time [seconds]:")
print(time()-star_time)
'''
data, fs = load(path)
#data, fs = load_epoch(path)
#For default values
sl = get_sl(data, fs)
#For parameter control
#sl = get_sl(data, fs, time_delay=4, w1=16, w2=215, pref=0.05)

plt.pcolor(sl,cmap=plt.cm.Blues)
plt.colorbar()
plt.ylabel('Channels')
plt.xlabel('Channels')
plt.show()
#show the execution time
print("The execution time [seconds]:")
print(time()-star_time)



