#manejo de elemeotos del sistema, como carpetas
import scipy.io as sio;
import numpy as np;
from numpy.linalg import matrix_rank
import glob
import os
import copy
import pickle

# General imports
import matplotlib.pyplot as plt
from matplotlib import cm, colors, colorbar
import pandas as pd


#importamos la rutina de welch
from scipy.signal import welch as pwelch
from scipy.stats import mode

# Import MNE, as well as the MNE sample dataset
import mne
from mne import io
import tarfile
from fieldtrip2mne import read_epoched

# FOOOF imports
from fooof import FOOOFGroup
from fooof.bands import Bands
from fooof.analysis import get_band_peak_fg
from fooof.plts.spectra import plot_spectrum


fs = 500;

def select_1_event(all_data,events,desired):
    """
    
    Parameters
    ----------
    all_data: Matriz canalesxframes
    events: lista de tuplas tal como se obtiene de mne.events_from_annotations
            (ultimo lugar de la tupla es el identificador del evento)
    desired: identificador del evento que quieres

    Returns
    -------
    lista con las secciones del evento deseado 
        [arreglos[canales,frame], ...]
    """
    segments = []
    desired=210
    for i in range(1,len(events)-1):
        this = events[i][2]
        next = events[i+1][2]
        if this == desired and next == desired:
            segments.append(all_data[:,events[i][0]:events[i+1][0]])

    len_trend = mode([x.shape[-1] for x in segments]).mode[0]

    for i in range(len(segments)):
        if segments[i].shape[-1] > len_trend:
            segments[i] = segments[i][:,:len_trend]
        if segments[i].shape[-1] <len_trend:
            segments[i] = None
    return [x for x in segments if x is not None ]

def continua(path,raw_list,events_from_annot_list,sub):
  data_continuous_list = []
  segments = select_1_event(raw_list[sub].get_data(),events_from_annot_list[sub],210)
  data_epochs = np.dstack(segments) #canales,puntos,epocas
  data_continuous = np.hstack(segments) #canales,puntos
  data_continuous_list.append(data_continuous)
  return data_epochs,data_continuous_list

def verify_same_data(archivos,keep_1,keep_2):
  same_vector = []
  if len(keep_1) > len(keep_2):
    more_channels = keep_1
    less_channels = keep_2
  else:
    less_channels = keep_1
    more_channels = keep_2


  for archivo in archivos:
    rawM = mne.read_epochs_eeglab(archivo)
    rawM.reorder_channels(more_channels)
    rawL = mne.read_epochs_eeglab(archivo)
    rawL.reorder_channels(less_channels)
    indexes = [more_channels.index(x) for x in less_channels]

    dataM = np.transpose(rawM._data,(1,2,0))
    dataL = np.transpose(rawL._data,(1,2,0))
    dataM = np.reshape(dataM,(dataM.shape[0],dataM.shape[1]*dataM.shape[2]),order='F')
    dataL = np.reshape(dataL,(dataL.shape[0],dataL.shape[1]*dataL.shape[2]),order='F')
    print(np.array(rawM.ch_names,dtype=object)[indexes])
    print(rawL.ch_names)

    same_vector.append(np.all(np.isclose(dataL,dataM[indexes,:])))
  all_result = np.all(same_vector)
  return same_vector,all_result

matrices = glob.glob('/content/drive/Shareddrives/Maestría Verónica Henao Isaza/Datasets/matrices.mat')

def fit_spatial_filter(M,all_channels,keep_channels,mode='demixing'):
  """
  all_channels = ['FP1',  'FPZ',  'FP2',  'AF3',  'AF4',  'F7',  'F5',  'F3',  'F1',  'FZ',  'F2',  'F4',  'F6',  'F8',  'FT7',  'FC5',  'FC3',  'FC1',  'FCZ',  'FC2',  'FC4',  'FC6',  'FT8',  'T7',  'C5',  'C3',  'C1',  'CZ',  'C2',  'C4',  'C6',  'T8',  'TP7',  'CP5',  'CP3',  'CP1',  'CPZ',  'CP2',  'CP4',  'CP6',  'TP8',  'P7',  'P5',  'P3',  'P1',  'PZ',  'P2',  'P4',  'P6',  'P8',  'PO7',  'PO5',  'PO3',  'POZ',  'PO4',  'PO6',  'PO8',  'I1',  'O1',  'OZ',  'O2',  'I2']
  keep_channels = ['FP1', 'FP2', 'F7', 'F3', 'FZ', 'F4', 'F8', 'T7', 'C3', 'CZ', 'C4', 'T8', 'P7', 'P3', 'PZ', 'P4', 'P8', 'O1', 'O2']
  fuentes = 19
  A = np.array([[x]*fuentes for x in all_channels],dtype=object)
  W = A.T
  print(indexes)
  print(A)
  print(W)
  """
  # asumir que all_channels tiene el orden original
  # asumir que keep_channels tiene el orden deseado
  indexes = [all_channels.index(x) for x in keep_channels]

  if mode == 'demixing':
    return M[:,indexes]
  else:
    return M[indexes,:]

M = sio.loadmat(matrices[0])
A = M["A"]
W = M["W"]

all_channels = ['FP1',  'FPZ',  'FP2',  'AF3',  'AF4',  'F7',  'F5',  'F3',  'F1',  'FZ',  'F2',  'F4',  'F6',  'F8',  'FT7',  'FC5',  'FC3',  'FC1',  'FCZ',  'FC2',  'FC4',  'FC6',  'FT8',  'T7',  'C5',  'C3',  'C1',  'CZ',  'C2',  'C4',  'C6',  'T8',  'TP7',  'CP5',  'CP3',  'CP1',  'CPZ',  'CP2',  'CP4',  'CP6',  'TP8',  'P7',  'P5',  'P3',  'P1',  'PZ',  'P2',  'P4',  'P6',  'P8',  'PO7',  'PO5',  'PO3',  'POZ',  'PO4',  'PO6',  'PO8',  'I1',  'O1',  'OZ',  'O2',  'I2']
keep_channels = ['FP1', 'FP2', 'F7', 'F3', 'FZ', 'F4', 'F8', 'T7', 'C3', 'CZ', 'C4', 'T8', 'P7', 'P3', 'PZ', 'P4', 'P8', 'O1', 'O2']
keep = ['FP1', 'FP2', 'F7', 'F3', 'F4', 'F8', 'T7', 'T8', 'P7', 'P3', 'P4', 'P8', 'O1', 'O2']
#m={1:'FP1', 2:'FP2', 3:'F7', 4:'F3', 5:'FZ', 6:'F4', 7:'F8', 8:'T7', 9:'C3', 10:'CZ', 11:'C4', 12:'T8', 13:'P7', 14:'P3', 15:'PZ', 16:'P4', 17:'P8', 18:'O1', 19:'O2'}
lemon_channels = set([x.upper() for x in raw_list_set1[0].ch_names])
intersection = set(all_channels).intersection(lemon_channels)

intersection = sorted(list(intersection))
print(intersection)