"""
@author: Brayan Hoyos Madera, Universidad de Antioquia, leobahm72@gmail.com

"""

from scipy.io import loadmat

'''
Para la comparación de las rutinas en Python y MATLAB, se procedió a cargar los
datos "CARLOS-N400.cnt" para Python y "CARLOS-N400.mat" para MATLAB. EL archivo
"CARLOS-N400.mat" fue creado a partir de los datos leidos de "CARLOS-N400.cnt", 
con lo cual se garantiza que los datos procesados por ambas rutinas son 
exactamente los mismos. La función utilizada para esto se muestra a continuación.
'''

def segment_signal(signal, fs):
    #Get the size of input data.
    (channels, samples) = signal.shape
    #Get the residue using the module.
    residue = samples%(fs*2)#fs*2 because segment each two seconds
    time = samples//fs #Get the time of register
    #Segment the samples each two seconds, erasing the residue data.
    data = array(split(signal[:, 0:(samples-int(residue))], int(time//2),1))
    #Config the data to samples*channels*trials
    data = data.transpose((2,1,0))
    return data 

#Dados obtenidos de ejecutando la rutina en MATLAB
#Tiempo de ejecución 24854.39 segundos
data_mat = loadmat("Resultado_SL_MATLAB.mat")
data_mat = data_mat["SL_data"]

#Dados obtenidos de ejecutando la rutina en python
#Tiempo de ejecución 688.17 segundos
data_pyt = loadmat("Resultado_SL_Python.mat")
data_pyt = data_mat["SL_data"]

#COMPARACIÓN
#Al restar los datos obenidos por la rutina en los diferentes lenguajes de 
#programación se debería obtener una matríz de ceros.
#Los datos obtenidos son del orden de 10^-17, lo que es prácticamente cero.
print(data_mat - data_pyt)

