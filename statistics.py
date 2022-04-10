import seaborn as sns
import json
from matplotlib import pyplot as plt
import numpy as np
from pandas.core.frame import DataFrame
import glob
import pandas as pd 
import itertools
import os

def load_txt(file):
  '''
  Function that reads txt files
  '''
  with open(file, 'r') as f:
    data=json.load(f)
  return data

def final_thresholds(data):
  '''
  Function to extract the final thresholds from the reject metric
  '''
  estudio= data['rejection']['final_thresholds']
  return pd.DataFrame({
  'kurtosis_min':estudio['kurtosis'][0],
  'kurtosis_max':estudio['kurtosis'][1],
  'amplitude_min': estudio['amplitude'][0],
  'amplitude_max':estudio['amplitude'][1],
  'trend':estudio['trend'][0],
  'spectrum_min':estudio['spectrum'][0],
  'spectrum_max':estudio['spectrum'][1]
  })

def final_rejection_percentages(listIn,data,keyInput):
  '''
  Function to extract percentages
  '''
  dataframes={}
  print("-------------------------")
 
  for i,key in enumerate(data['rejection']['criteria']):
    dataframes[key]=data['rejection'][keyInput][i]
  listIn.append(dataframes)
  return listIn 


def indicesWica(sums,data):
  '''
  canales,epocas
  '''
  mat=np.array(data['wica'])
  sum=np.sum(mat.flatten())
  sums.append(sum/mat.size)
  return sums 

def bandsPowers(data):
  '''
  Function to return the power bands
  '''
  df_powers={}
  for i,key in enumerate(data['bands']):
    print(i,key)
    df_powers[key]=data['channel_power'][i]
  powers=pd.DataFrame(df_powers)
  return powers

def graphicsViolinplot(opt,f,c,dataframe,titulo):
  '''
  Function to plot violin plot of various metrics that do not have a similar 'y' axis
  '''
  if opt==1:
    fig,axs= plt.subplots(f,c,figsize=(4,8)) 
    axs=list(itertools.chain(*axs))
    print(axs)
    for i,nombreColumna in enumerate(dataframe.columns.values):
      sns.violinplot(data=dataframe[nombreColumna][:,None],ax=axs[i]) 
      axs[i].set_title(nombreColumna)
    
  if opt==2:
    sns.violinplot(data=dataframe)
  plt.suptitle(titulo,fontsize=20)
  plt.tight_layout()
  plt.show()  
  return


file=r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM'
files=glob.glob(os.path.join(file ,'**/**stats.txt'),recursive=True)
file_powers=glob.glob(os.path.join(file,'**/**_powers.txt'),recursive=True)

dataframesPowers=[]
for power in file_powers:
  dataFile=load_txt(power)
  statsPowers=bandsPowers(dataFile)
dataframesPowers.append(statsPowers)
datosPowers=pd.concat((dataframesPowers[:]))
plt.title('Bandas de frecuencia para un estudio')
sns.violinplot(data=datosPowers)
plt.show()

df_Final_thresholds=[]
porcentajeFilesFinal=[]
suma=[]
porcentajeFilesInitial=[]
for file in files:
  dataFile=load_txt(file) # Carga de los datos
  print(dataFile['prep'])
  # REJECTION
  statsFinalThresholds=final_thresholds(dataFile) # Para varios archivos saca los final thresholds
  percentagesFinalThresholds=final_rejection_percentages(porcentajeFilesFinal,dataFile,'final_rejection_percentages') # Para varios archivos saca los porcentajes de final thresholds
  sumas=indicesWica(suma,dataFile)
  percentagesInitialThresholds=final_rejection_percentages(porcentajeFilesInitial,dataFile,'initial_rejection_percentages')
  # Indices para varios archivos de prep
  # statsPrep=indicesPrep(dataFile)
  # # Indices para varios archivos de wica
  # statsWica=indicesWica(dataFile)
  df_Final_thresholds.append(statsFinalThresholds)

datosFT=pd.concat((df_Final_thresholds[:]))
dataPercentageFT=pd.DataFrame(porcentajeFilesFinal)
dataPercentageIT=pd.DataFrame(porcentajeFilesInitial)
dfstats_wica=pd.DataFrame({'componentes filtradas':sumas})

plt.title('Métricas wICA')
plt.ylabel("Relación cantidad de epocas filtradas sobre epocas totales")
sns.violinplot(data=dfstats_wica)

estudio='General'
graphicsViolinplot(1,4,2,datosFT,f'Final threshold- {estudio}')
graphicsViolinplot(1,2,3,dataPercentageFT,f'Percentages: final threshold- {estudio}')
graphicsViolinplot(1,2,3,dataPercentageIT,f'Percentages: Initial threshold- {estudio}')