import numpy as np
import itertools #Usado para ver las posibles permutaciones


def Entropia_Permutacion(senal,D):
  """
  Función creada para encontrar la entropia de permutación de una serie de tiempo unidimensional de un EEG.

  Entradas:  senal> Señal EEG de tipo ndarray y de forma (puntos,).

             D> Dimension embebida que controla la longitud de cada uno de los nuevos vectores columna
             para realizar para realizar la partición del espacio de estado.
  
  Se definen como variables:
  
             tao> Retardo de tiempo de incrustación que controla el número de períodos de tiempo entre elementos
             de cada uno de los nuevos vectores de columna. Se toma el valor recomendado tao=1.

             tamano> Numero o cantidad de datos que se encuentran en la señal.

             numero_vectores> Cantidad de vectores que se deben obtener al realizar la particion del espacio estado.

             matriz> Se inicializa una matriz de ceros con la forma requerida para realizar la particion del espacio
             estado, teniendo en cuenta D y numero de vectores.

             permutations> Lista de tuplas de las posibles permutaciones que existen corresponden a D! permutaciones.

             p_i> Vector inicializado en cero, con la longitud de las posibles permutaciones, es usado para guardar
             en cada posicion (que corresponde a la posicion donde estan las permutaciones en permutations) las veces 
             que se repite cada permutacion posible en la matriz de permutaciones, esta ultima se obtiene al realizar
             la clasificacion ordinal de cada vector en matriz.

             Pis> Corresponde al vector de frecuencias relativas. 
             Como el log2 de 0 no esta definido, de este vector se borran estos valores si los hay, por tanto las frecuencias
             relativas de 0, no son tenidas en cuenta.
             np.where encuentra la posicion en el ndarray Pis donde hay un 0 y con delete se borra esa posición.

             PE> Es la entropia de permutación encontrada para la señal, con la funcion dot se realiza un producto punto entre vectores.
  
  El primer ciclo for es creado para añadir los valores adecuados en matriz, y asi realizar la partición del espacio estado,
  a partir de la señal, este ciclo permite crear la matriz con la forma deseada para un 3<=D<=7 y un tao=1, esto lo realiza hasta 
  que se completen todas las filas de la matriz.

  En el siguiente ciclo for, a cada fila obtenida en la matriz le encuentro el correspondiente vector permutación, esto 
  se realiza con la función argsort, esta permite obtener los índices de los valores de un array una vez ordenados, teniendo asi un vector permutación.
  
  ejemplo:   ages = np.array([53, 29, 33, 19])
             np.argsort(ages)
             >>> array([3, 1, 2, 0], dtype=int64)

  Posteriormente en el ciclo for, el vector permutacion (que es un ndarray) obtenido para la fila se cambia a una tupla, 
  para mirar en que posición se encuentra en el vector permutations y asi ir añadiendo en p_i cuantas veces se repite una permutación,
  ya que se sabe que cada posicion corresponde a una permutación diferente. 

  """
  tao=1
  tamano = senal.shape[0] 
  numero_vectores=tamano-(D-1)*tao 
  matriz = np.zeros((numero_vectores,D), dtype='float64') 

  for i in range(tamano):
    for j in range(D):
        if i<numero_vectores:
          matriz[i,j]=np.array([senal[i+j]]) 

  permutations = list(itertools.permutations(np.arange(0,D,1)))
  p_i=np.zeros(len(permutations),dtype=int) 
  
  for fila in matriz:
    l=tuple(np.argsort(fila)) 
    if l in permutations:  
      p_i[permutations.index(l)]=p_i[permutations.index(l)]+1 

  Pis = p_i/(numero_vectores)  
  Pis=np.delete(Pis, np.where(Pis==0))
  PE = np.dot(np.log2(Pis),-Pis) 

  return float(PE/np.log2(np.math.factorial(3))) #Normalizada



#### PRUEBA DOS ENTROPIAS
#import mne
#from sovaharmony.p_entropy import p_entropy
#
#fnameCE=r"E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_desc-norm_eeg"
#raw_data=mne.read_epochs(fnameCE + '.fif', verbose='error')
#data = raw_data.get_data()
#(e, c, t) = data.shape
#new_data = np.transpose(data.copy(),(1,2,0))
#for e in range(data.shape[0]):
#    for c in range(data.shape[1]):
#        assert np.all(data[e,c,:] == new_data[c,:,e])
#mean_channels = []
#mean_channels_vale = []
#for channel in range(data.shape[1]):
#    segment = []
#    segment_vale = []
#    for epoch in range(data.shape[0]):
#        # Por segmento
#        #entropy_segment = p_entropy(new_data[channel,:,epoch])
#        entropy_vale = Entropia_Permutacion(new_data[channel,:,epoch],D=3)
#        #segment.append(entropy_segment)
#        segment_vale.append(entropy_vale)
#        # Por canal
#    #mean_channels.append(np.mean(segment))
#    mean_channels_vale.append(np.mean(segment_vale))
##print(len(segment))
#print(len(segment_vale))
#print(len(mean_channels))
#print(len(mean_channels_vale))
##print(segment[0])
#print(segment_vale)