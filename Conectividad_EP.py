#importacion de librerias 
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
import math
from numpy.lib.stride_tricks import sliding_window_view
from scipy.stats import rankdata
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
import csv


def entropia_permutacion(eeg_signal, d=5, t=1):

  '''
  Inicialmente, se utilizó una función de Numpy que crea una ventana deslizante
  sobre la señal, la cuál va tener un ancho d y un paso t. Es necesario 
  realizar una transposición de la matriz puesto que se organiza normalmente
  como filas. Posteriormente, se hallaron los patrones ordinales agrupados
  igualmente en el mimso eje con la función argsort() del
  paquete de Numpy. Seguidamente, se hallaron las frecuencias relativas para
  cada ranking y se obtuvieron los conteos para el cálculo de la frecuencia 
  relativa con respecto al número de columnas que se obtuvieron del
  ordenamiento con la ventana deslizante. Finalmente, se utiliza la
  definición de entropía de Shannon  para cada una de las probabilidades.

  Esta función tiene como entrada un vector de dimensiones
  (número de muestras, ) es decir, 1 canal, 1 época
  '''

  # Función de ventana deslizante (modulo de Numpy)
  sorted_matrix = sliding_window_view(eeg_signal, d, axis=0).T[:, ::t]

  # Patrones ordinales y ranking
  index_matrix = np.argsort(sorted_matrix, axis=0)


  # Se busca los arreglos diferentes y se cuentas el número de veces en que 
  # se repite cada uno
  _ , counts = np.unique(index_matrix, axis=1, return_counts=True)
 
  # Número de columnas del arreglo de la ventana deslizante
  num_columns = len(eeg_signal) - (d-1) * t
  # Frecuencia relativa para cada ranking
  relative_freq = counts / num_columns
  # Se calcula la entropia de permutación a través de la entropía de Shannon
  pe = np.sum(- relative_freq * np.log2(relative_freq))
  # Se retorna el valor de la entropia de permutación y la matriz de 
  # valores organizados
  return pe, sorted_matrix

# Se probó la función en una señal 
data = sio.loadmat(archivos_control[0])['data'];
signal = data[0,:,0] # un canal una época
mn = round(entropia_permutacion(signal)[0], 4) # Redondeo a 4 cifras decimales
print(f'La entropía de permutación de la señal es {mn}')

def pe_multiples_epocas(eeg_signal, d=5, t=1):

  '''
  la función recibe una señal EEG de la forma (# de muestras, épocas) y
  para cada época aplica la funciónde entropia de permutación, lo cual 
  genera un valor para cada época. Finalmente, se promedian todos los resultados
  '''
  entropy, _ = np.apply_along_axis(lambda x: entropia_permutacion(x, d=d, t=t),
                                0,
                                eeg_signal)

  return round(np.mean(entropy), 4)

# Se prueba la función con una señal
data = sio.loadmat(archivos_control[0])['data']
data1= data[0,:,:] # un canal, múltiples épocas
mn_epocas = pe_multiples_epocas(data1)
print(f'La media de la entropía de permutación sobre las épocas es {mn_epocas}')

def lpe_entropia (eeg_signal, h,  d=5 , t=1):


  '''
  Función para calular la entropía de permutación agrupada en una señal de
  EEG de la forma (número de muestras, ). Inicialmente, se realiza el cálculo
  para las dimensiones como en los otros casos (N). Se llama a la función
  entropia de permutación y se obtiene la matriz de valores organizados.
  Seguidamente, se crea la matriz donde se guardarán los rankings finales
  de la permutación agrupada (r) con iguales dimensiones de la matriz
  de valores organizados. Seguidamente, se rankea la matriz de valores
  organizados (es necesario el uso de scipy.stats puesto que en este caso
  es estrictamente necesario el orden de la matriz ordinal de valores).

  Finalmente se hace uso de 3 ciclos for los cuales no pudieron ser remplazados 
  debido a las siguientes aclaraciones:

  *El primer for se utiliza con el objetivo de recorrer cada columna del arreglo
  matricial. Es necesario y no justificable con Numpy puesto que para recorrer
  las columnas es ncesario la comparación la matriz de valores ordinales y 
  su orden directo.

  *El segundo for se implementa para recorrer el arreglo invertido de cada
  vector de la matriz, con el fin de realizar la operación correspodiente desde
  el mayor valor (j+1) hasta el siguiente valor (j+2, j+3 ...). No fue posible
  con Numpy debido a que la sumatoria no dependia de la posición de los valores
  relacionados con los indices de la misma matriz, sino con los valores signados
  en la matriz de ranking ordinales

  *El tercer for permite recorrer cada elemento del vector rank creado
  y asignarle su respectivo valor siguiendo las condiciones de la entropia
  agrupada.

  '''
  # Se calcula el numero de columnas
  N = len(eeg_signal) - (d-1) * t 
  
  #Se utiliza la función de entropia_permutacion con el fin de obtener la matriz de vectores de columnas superpuestas
  _, sorted_matrix = entropia_permutacion(eeg_signal, d=d, t=t)

  # Se genera la matriz donde se guardará el ranking final
  r = np.zeros(sorted_matrix.shape) 

  # Se genera los patrones ordinales 
  ranked_data = np.apply_along_axis(lambda x: (rankdata(x, method='ordinal')-1).astype(int),
                                    1,
                    np.array(np.hsplit(sorted_matrix, sorted_matrix.shape[1])))

  # Eliminación de una dimensión sobrante y transposición
  ranked_data = np.squeeze(ranked_data).T

  for c in range(N): 

     #Se organiza los elementos de cada columna 
     columns_org = sorted((sorted_matrix[:,c]))

     #Se obtiene cada columna del ranked_data     
     arreglo = ranked_data[:,c]

     count = len(arreglo)
     #Se establece un arreglo para las dimensiones del rank final
     rank1_ = np.array(arreglo.copy())
      
     for j in range(count - 1):
      #Se genera el valor de v
       v = abs(columns_org[j]-columns_org[j+1])
      # Se establece un condicional que permite hacer la resta de los valores del rank según la lógica de la entropia agrupada
       if v < h:

         indice = columns_org.index(columns_org[j + 1])

         for k1 in range(count):

           rank1_[k1] = np.where(arreglo[k1] == indice or arreglo[k1] > indice,
                                 rank1_[k1] - 1,
                                 rank1_[k1])

       elif v > h:

         rank1_ = rank1_
    
    #Se genera la matriz con los correspondientes vectores del rank_  
     r[:,c]=rank1_
  
  #Se calcula la frecuencia relativa con el fin de obtener la entropia de permutación 
  _ , counts = np.unique(r, axis=1, return_counts=True)
  relative_freq = counts / N
  pe = np.sum(- relative_freq * np.log2(relative_freq))
 
  return round(pe, 4)

# Se prueba la función con el arreglo [4,7,9,10,6,11,3] con un h = 3
epa = lpe_entropia([4,7,9,10,6,11,3], h=3)
print(f' la entropia de permutación agrupada es de {epa}')

def lpe_multiples_epocas(eeg_signal, h, d=5, t=1):

  '''
  la función recibe una señal EEG de la forma (# de muestras, épocas) y
  para cada época aplica la función de entropia de permutación agrupada, lo cual 
  genera un valor para cada época. Finalmente, se promedian todos los resultados
  '''

  entropy = np.apply_along_axis(lambda x: lpe_entropia(x, h, d=d, t=t),
                                0,
                                eeg_signal)

# Se obtiene el promedio de la entropia de permutación agrupada
# calculado sobre cada epoca

  return round(np.mean(entropy), 4)
  
def df_entropias(h, path, d=5, t=1):

  # Para los nombres, que serán utilizados como indice

  names_control = [ i[17:21] for i in archivos_control]
  names_sujetos = [ i[19:23] for i in archivos_sujetos]
  names = names_control + names_sujetos

  # Para la clasificación 

  estado = ['Parkinson' if nombre[0] == 'P' else 'Control' for nombre in names]

  # Para los canales

  electrodes = ['Entropia_Canal_' + str(x) for x in range(1,9)]


  # Para recorrer los archivos que se tienen

  archivos = archivos_control + archivos_sujetos

  # Para guardar los datos generados por las funciones
  datos = []

  # Recorre los archivos

  for data in archivos:

    #Se carga la señal
    signal = sio.loadmat(data)["data"]

    # Se aplica la función de LPE a cada archivo

    sujeto_lpe = [lpe_multiples_epocas(signal[canales,:,:], h, d=d, t=t) for canales in range(signal.shape[0])]

    # Se añade a los datos cada sujeto con el promedio por épocas de cada canal

    datos.append(sujeto_lpe)

  # Se crea el dataframe con los datos, el indice como los sujetos y 
  # las columnas como los electrodos o canales
  data_frame_entropia = pd.DataFrame(datos, index=names, columns=electrodes)
  data_frame_entropia.index.name = 'Sujeto'
  # Se inserta la columna del estado
  data_frame_entropia.insert(0, 'Estado', estado)

  # Se guarda en una archivo de .csv
  data_frame_entropia.to_csv(path, sep=',')

  return data_frame_entropia