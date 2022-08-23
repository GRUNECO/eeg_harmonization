"""
@author: Brayan Hoyos Madera, Universidad de Antioquia, leobahm72@gmail.com

"""

from time import time
from load_cnt import load
from sl import get_sl
from matplotlib import pyplot as plt


#capture the start time
star_time = time()
#Read input data
data, fs = load(r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-OE_desc-norm_eeg")
#For default values
sl = get_sl(data, fs)
#For parameter control
#sl = get_sl(data, fs, time_delay=4, w1=16, w2=215, pref=0.05)

#Show sl data
print(sl)

#show the execution time
print("The execution time [seconds]:")
print(time()-star_time)
