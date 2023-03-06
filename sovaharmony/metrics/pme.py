#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Marcos L. David Usuga
"""
####################### External libraries ####################################
import scipy.signal as signal
import scipy.io as sio
import numpy as np
import pandas as pd
import os
from sovaflow.utils import createRaw

####################### Internal libraries #####################################
#import sovaharmony.linear_FIR_filter_v2 as lfir
import mne

########################## My exception classes ###############################
class Error(Exception):
    pass

class DoingError(Error):
    def __init__(self, mensaje):
        self.mensaje = mensaje

############################## Functions ######################################
def Order_Hamming_Window(Cutoff_Hz, Fs):
    """
    Calcula el orden minimo para un filtro pasa-bandas de tipo FIR de ventana Hamming, 
    con respecto a la frecuencia de muestreo y frecuencias de corte.

    Parámetros:
        Cutoff_Hz: tipo tuple
                Una tupla que contiene las frecuencias de corte para un filtro pasa bandas.
                
        Fs: tipo int 
                Valor de la frecuencia de muestreo de la señal a filtrar. 
                
    Devuelve:
        Order: tipo int
                Valor del orden minimo para el filtro FIR de ventana Hamming (valor par). 
    """
    Nyq_Rate = Fs/2; 
    Order = round( 4 / ((Cutoff_Hz[1]-Cutoff_Hz[0])/Nyq_Rate) )
    if (Order%2 != 0):
        Order += 1
    return Order

def BandPass_Filter_Hamming_Window(Signal, Cutoff_Hz, Fs, Order):
    """
    Calcula y aplica un filtro pasabanda tipo FIR de ventana Hamming a una señal de entrada.

    Parámetros:
        Signal: tipo numpy.ndarray
                Arreglo con los datos de la señal a filtrar. 
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                
        Cutoff_Hz: tipo tuple
                Una tupla que contiene las frecuencias de corte para un filtro pasa bandas.
                
        Fs: tipo int 
                Valor de la frecuencia de muestreo de la señal a filtrar.
                
        Order: tipo int
                Valor del orden para el filtro FIR de ventana Hamming.

    Devuelve:
        Filtered_Signal: tipo numpy.ndarray
                Vector con los datos de la señal filtrada.
                Nota: Retorna False cuando se ingresa una señal fuera de las dimensiones 
                aceptables (1 o 2).
    """
    if (type(Signal) == np.ndarray):
        Nyq_Rate = Fs/2  
        Cutoff_Norm = [Cutoff_Hz[0]/Nyq_Rate, Cutoff_Hz[1]/Nyq_Rate]
        a = signal.firwin(Order, Cutoff_Norm, window = 'hamming', pass_zero = False)
        Delay = int(round(0.5 * (Order-1))) 
        if (Signal.ndim == 2): 
            Filtered_Signal = signal.filtfilt(a,1,Signal)[:,Delay:]
        elif (Signal.ndim == 1):
            Filtered_Signal = signal.filtfilt(a,1,Signal)[Delay:]
        else:
            raise DoingError('The signal variable can only have 1 or 2 dimensions!!')
        return Filtered_Signal
    else:
        raise DoingError('The signal variable is not an array!!')
    
def SubBands_Decomposition(Signal, Fs, Bands=[[1.5,6],[6,8.5],[8.5,10.5],[10.5,12.5],[12.5,18.5],[18.5,21],[21,30],[30,45]], Filt='FIR_filter'):
    """
    Descompone una señal en sub-bandas.

    Parámetros:
        Signal: tipo numpy.ndarray
                Arreglo con los datos de la señal a descomponer en las sub-bandas.
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                -> 3 dimensiones (Señales, Muestras, Epocas)
                
        Fs: tipo int 
                Valor de la frecuencia de muestreo de la señal a filtrar.
        
        Opcionales:
            
        Bands: tipo list
                Una lista con las tuplas de cada una de las bandas que contienen 
                las frecuencias inicial y final.
                
        Filt: tipo str
                Un string que indica el tipo de filtro a utilizar para la descomposicion.
                -> 'FIR_filter': Filtro FIR 
                -> 'Hamming': filtro tipo FIR de ventana Hamming
                
    Devuelve:
        SubBand_Signal: tipo numpy.ndarray
                Matriz que contiene la señal descompuesta en las sub-bandas. 
                En el formato:
                -> 1 dimension (Bandas, Muestras) - por defecto (5, Muestras)
                -> 2 dimensiones (Señales, Bandas, Muestras) - por defecto (Señales, 5, Muestras)
                -> 3 dimensiones (Señales, Bandas, Muestras, Epocas) - por defecto (Señales, 5, Muestras, Epocas)
    """
    if (type(Signal) == np.ndarray) and (type(Filt) == str):
        Num_Bands = len(Bands)
        if (Filt  == 'FIR_filter'):
            if (Signal.ndim == 2):
                Signal_raw = createRaw(Signal,Fs)
                Num_Signals, Values = Signal.shape
                SubBand_Signal = np.zeros((Num_Signals, Num_Bands, Values))
                for j, Band in enumerate(Bands):
                    SubBand_Signal[:,j,:] = mne.filter.filter_data(Signal, Fs, Band[0],Band[1])
            elif (Signal.ndim == 1): 
                 
                SubBand_Signal = np.zeros((Num_Bands, Signal.shape[0]))
                for i, Band in enumerate(Bands):
                    SubBand_Signal[i] = mne.filter.filter_data(Signal, Fs, Band[0],Band[1])
            elif (Signal.ndim == 3):
                
                Num_Signals, Values, Epochs = Signal.shape
                Temp_Signal = np.reshape(Signal, (Num_Signals,Values*Epochs), order='F')
                SubBand_Signal = np.zeros((Num_Signals, Num_Bands, Values, Epochs))
                for j, Band in enumerate(Bands):
                    SubBand_Signal[:,j,:,:] = np.reshape(mne.filter.filter_data(Temp_Signal, Fs, Band[0],Band[1]),
                                           (Num_Signals, Values, Epochs), order='F')
            else:
                raise DoingError('The signal variable can only have 1, 2 or 3 dimensions!!')
        elif (Filt  == 'Hamming'):
            Order = 0
            for Band in Bands:
                New_Order = Order_Hamming_Window(Band, Fs)
                if New_Order > Order:
                    Order = New_Order
            if (Order>120): ### OJO!!! Solo era para prueba
                Order = 120
            Delay = int(round(0.5 * (Order-1))) 
            if (Signal.ndim == 2):
                Num_Signals, Values = Signal.shape
                SubBand_Signal = np.zeros((Num_Signals, Num_Bands, Values-Delay))
                for j, Band in enumerate(Bands):
                    SubBand_Signal[:,j,:] = BandPass_Filter_Hamming_Window(Signal, Band, Fs, Order)
            elif (Signal.ndim == 1):  
                SubBand_Signal = np.zeros((Num_Bands, int(Signal.shape[0]-Delay)))
                for i, Band in enumerate(Bands):
                    SubBand_Signal[i] = BandPass_Filter_Hamming_Window(Signal, Band, Fs, Order)
            elif (Signal.ndim == 3):
                Num_Signals, Values, Epochs = Signal.shape
                Temp_Signal = np.reshape(Signal, (Num_Signals,Values*Epochs), order='F')
                Reject = int(np.ceil(Delay/Values))
                New_Epochs = Epochs - Reject
                SubBand_Signal = np.zeros((Num_Signals, Num_Bands, Values, New_Epochs)) 
                for j, Band in enumerate(Bands):
                    SubBand_Signal[:,j,:,:] = np.reshape(BandPass_Filter_Hamming_Window(Temp_Signal, Band, Fs, Order)[:,(Reject*Values)-Delay:],
                                           (Num_Signals, Values, New_Epochs), order='F')
            else:
                raise DoingError('The signal variable can only have 1, 2 or 3 dimensions!!')
        else:
            raise DoingError('Unknown filter!!')
        return SubBand_Signal
    else:
        raise DoingError('The signal variable is not an array or filter is not a string!!')
    
def Temporal_Envelopes(Signal):
    """
    Extrae las envolventes temporales (e) ó modulaciones de amplitud de una señal, 
    utilizando Transformada de Hilbert.

    Parámetros:
        Signal: tipo numpy.ndarray
                Arreglo con los datos de la señal a la cual se va a calcular e.
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                -> 3 dimensiones (Señales, Muestras, Epocas)
                -> 4 dimensiones (Señales, Bandas, Muestras, Epocas)
                
    Devuelve:
        Envelope: tipo numpy.ndarray
                Arreglo que contiene la envolvente temporal de la señal.
                -> 1 dimension (Muestras) 
                -> 2 dimensiones (Señales, Muestras) 
                -> 3 dimensiones (Señales, Muestras, Epocas)
                -> 4 dimensiones (Señales, Bandas, Muestras, Epocas)
    """
    if (type(Signal) == np.ndarray):
        if (Signal.ndim == 2) or (Signal.ndim == 3):
            Envelope = np.absolute(signal.hilbert(Signal, axis=1))
        elif (Signal.ndim == 1):
            Envelope = np.absolute(signal.hilbert(Signal, axis=0))
        elif (Signal.ndim == 4):
            Envelope = np.absolute(signal.hilbert(Signal, axis=2))
        else:
            raise DoingError('The signal variable can only have 1, 2, 3 or 4 dimensions!!')
        return Envelope
    else:
        raise DoingError('The signal variable is not an array!!')
#bands =[[1.5,6],[6,8.5],[8.5,10.5],[10.5,12.5],[12.5,18.5],[18.5,21],[21,30],[30,45]] #UDEA por defecto
#M_Bands = [(0.5,4),(4,8),(8,12),(12,30),(30,100)] #Marcos por defecto
def Modulation_Bands_Decomposition(SubBand_Signal, Fs, M_Bands = [[1.5,6],[6,8.5],[8.5,10.5],[10.5,12.5],[12.5,18.5],[18.5,21],[21,30],[30,45]], Filt='FIR_filter'):
    """
    Descompone en bandas de modulacion a una señal previamente descompuesta en sub-bandas.
    Esta funcion asume que las m-bandas son equivalentes a las sub-bandas y van de la menor a mayor frecuencia.
    Por lo tanto desde las propiedades de la transformada de Hilbert y siguiendo el teorema de Bedrosian, 
    la señal envolvente solo puede contener frecuencias (es decir, frecuencias de modulación) hasta el 
    ancho de banda de su señal de origen. Todas las m-bandas mayores a la sub-banda no se calculan y se deja 
    con valores iguales a cero.

    Parámetros:
        SubBand_Signal: tipo numpy.ndarray
                Matriz de m_bandas con el formato (M_bandas, Muestras) 
                -> 2 dimension (Bandas, Muestras) 
                -> 3 dimensiones (Señales, Bandas, Muestras) 
                -> 4 dimensiones (Señales, Bandas, Muestras, Epocas) 
                
        Fs: tipo int 
                Valor de la frecuencia de muestreo de la señal a filtrar.
                
        Opcionales:
            
        M_Bands: tipo list
                Una lista con las tuplas de cada una de las bandas que contienen 
                las frecuencias inicial y final.
            
        Filt: tipo str
                Un string que indica el tipo de filtro a utilizar para la descomposicion.
                -> 'FIR_filter': Filtro FIR 
                -> 'Hamming': filtro tipo FIR de ventana Hamming
                
    Devuelve:
        MBand_Signal: tipo numpy.ndarray
                Matriz con las señales resultado de las descomposiciones, 
                en formato:
                -> 2 dimension (M_Bandas, Bandas, Muestras) 
                -> 3 dimensiones (Señales, M_Bandas, Bandas, Muestras) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas, Muestras, Epocas) 
    """
    if (type(SubBand_Signal) == np.ndarray) and (type(Filt) == str):
        Num_M_Bands = len(M_Bands)
        if (Filt  == 'FIR_filter'):
            if (SubBand_Signal.ndim == 2):
                Num_Bands, Values = SubBand_Signal.shape
                MBand_Signal = np.zeros((Num_M_Bands, Num_Bands, Values))
                for i, M_Band in enumerate(M_Bands):
                    for j in range(0,i+1):
                        MBand_Signal[i,j,:] = mne.filter.filter_data(SubBand_Signal[j], Fs, M_Band[0],M_Band[1])
            elif (SubBand_Signal.ndim == 3):
                Num_Signals, Num_Bands, Values = SubBand_Signal.shape
                MBand_Signal = np.zeros((Num_Signals, Num_M_Bands, Num_Bands, Values))
                for i, M_Band in enumerate(M_Bands):
                    for j in range(0,i+1):
                        MBand_Signal[:,i,j,:] = mne.filter.filter_data(SubBand_Signal[:,j,:], Fs, M_Band[0],M_Band[1])
            elif (SubBand_Signal.ndim == 4):
                Num_Signals, Num_Bands, Values, Epochs = SubBand_Signal.shape
                Temp_Signal = np.reshape(SubBand_Signal, (Num_Signals, Num_Bands, Values*Epochs), order='F')
                MBand_Signal = np.zeros((Num_Signals, Num_M_Bands, Num_Bands, Values, Epochs))
                for i, M_Band in enumerate(M_Bands):
                    for j in range(0,i+1):
                        MBand_Signal[:,i,j,:,:] = np.reshape(mne.filter.filter_data(Temp_Signal[:,j,:], Fs, M_Band[0],M_Band[1]), 
                                    (Num_Signals, Values, Epochs), order='F')
            else:
                raise DoingError('The signal variable can only have 2, 3 or 4 dimensions!!')
        elif (Filt  == 'Hamming'):
            Order = 0
            for M_Band in M_Bands:
                New_Order = Order_Hamming_Window(M_Band, Fs)
                if New_Order > Order:
                    Order = New_Order
            if (Order>120): ### OJO!!! Solo era para prueba
                Order = 120
            Delay = int(round(0.5 * (Order-1))) 
            if (SubBand_Signal.ndim == 2):
                Num_Bands, Values = SubBand_Signal.shape
                MBand_Signal = np.zeros((Num_M_Bands, Num_Bands, Values-Delay))
                for i, M_Band in enumerate(M_Bands):
                    for j in range(0,i+1):
                        MBand_Signal[i,j,:] = BandPass_Filter_Hamming_Window(SubBand_Signal[j], M_Band, Fs, Order)
            elif (SubBand_Signal.ndim == 3):
                Num_Signals, Num_Bands, Values = SubBand_Signal.shape
                MBand_Signal = np.zeros((Num_Signals, Num_M_Bands, Num_Bands, Values-Delay))
                for i, M_Band in enumerate(M_Bands):
                    for j in range(0,i+1):
                        MBand_Signal[:,i,j,:] =  BandPass_Filter_Hamming_Window(SubBand_Signal[:,j,:], M_Band, Fs, Order)
            elif (SubBand_Signal.ndim == 4):
                Num_Signals, Num_Bands, Values, Epochs = SubBand_Signal.shape
                Temp_Signal = np.reshape(SubBand_Signal, (Num_Signals, Num_Bands, Values*Epochs), order='F')
                Reject = int(np.ceil(Delay/Values))
                New_Epochs = Epochs - Reject
                MBand_Signal = np.zeros((Num_Signals, Num_M_Bands, Num_Bands, Values, New_Epochs))
                for i, M_Band in enumerate(M_Bands):
                    for j in range(0,i+1):
                        MBand_Signal[:,i,j,:,:] = np.reshape(BandPass_Filter_Hamming_Window(Temp_Signal[:,j,:], M_Band, Fs, Order)[:,(Reject*Values)-Delay:], 
                                      (Num_Signals, Values, New_Epochs), order='F')
            else:
                raise DoingError('The signal variable can only have 2, 3 or 4 dimensions!!')
        else:
            raise DoingError('Unknown filter!!')
        return MBand_Signal
    else:
        raise DoingError('The signal variable is not an array or filter is not a string!!')

def Modulation_Bands_Decomposition_Hamming(SubBand_Signal, Fs, M_Bands = [[1.5,6],[6,8.5],[8.5,10.5],[10.5,12.5],[12.5,18.5],[18.5,21],[21,30],[30,45]]):
    """
    Descompone en bandas de modulacion (por ventana deslizante tipo Hamming) a una señal previamente 
    descompuesta en sub-bandas.
    Esta funcion asume que las m-bandas son equivalentes a las sub-bandas y van de la menor a mayor frecuencia.
    Por lo tanto desde las propiedades de la transformada de Hilbert y siguiendo el teorema de Bedrosian, 
    la señal envolvente solo puede contener frecuencias (es decir, frecuencias de modulación) hasta el 
    ancho de banda de su señal de origen. Todas las m-bandas mayores a la sub-banda no se calculan y se deja 
    con valores iguales a cero.

    Parámetros:
        SubBand_Signal: tipo numpy.ndarray
                Matriz de m_bandas con el formato (M_bandas, Muestras) 
                -> 2 dimension (Bandas, Muestras) 
                -> 3 dimensiones (Señales, Bandas, Muestras) 
                -> 4 dimensiones (Señales, Bandas, Muestras, Epocas) 
                
        Fs: tipo int 
                Valor de la frecuencia de muestreo de la señal a filtrar.
                
        Opcionales:
            
        M_Bands: tipo list
                Una lista con las tuplas de cada una de las bandas que contienen 
                las frecuencias inicial y final.
                
    Devuelve:
        Energy: tipo numpy.ndarray
                Arreglo con los valores obtenidos de energia.
                -> 2 dimension (M_Bandas, Bandas) 
                -> 3 dimensiones (Señales, M_Bandas, Bandas) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas, Epocas)
    """
    if (type(SubBand_Signal) == np.ndarray):
        if (SubBand_Signal.ndim == 4):
            Num_Signals, Num_Bands, Values, Epochs = SubBand_Signal.shape
            frec_res = Fs/Values
            SubBand_Signal = SubBand_Signal * np.tile(np.reshape(np.hamming(Values), (1, 1, Values, 1)),(Num_Signals,  Num_Bands, 1, Epochs))
            i_mod_j =  np.absolute(np.fft.fft(SubBand_Signal, axis=2))
            Eij = np.zeros((Num_Signals, len(M_Bands), Num_Bands, Epochs))
            for i, M_Band in enumerate(M_Bands):
                for j in range(0,i+1):
                    Eij[:,i,j,:] = np.mean(i_mod_j[:, j, int(M_Band[0]/frec_res):int(M_Band[1]/frec_res)+1, :], axis=1)
        else:
            raise DoingError('The signal variable can only have 2, 3 or 4 dimensions!!')
        return Eij
    else:
        raise DoingError('The signal variable is not an array!!')
    
def Signal_Spectrum(Signal):
    """
    Calcula el espectro de la señal utilizando la transformada de Fourier.
    
    Parámetros:
        Signal: tipo numpy.ndarray
                Arreglo de señales a calcular el espectro, en formato:
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                -> 3 dimensiones (Señales, Muestras, Epocas)
              
    Devuelve:
        FFT_Absolute: tipo numpy.ndarray
                Arreglo con el spectro de la señal.
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                -> 3 dimensiones (Señales, Muestras, Epocas)
    """
    if (type(Signal) == np.ndarray):
        if (Signal.ndim == 2) or (Signal.ndim == 3):
            if (Signal.shape[1] == 297428): # fft Presente problemas con esta cantidad de numeros (con otros se vulve muy lento)
                FFT_Absolute = np.absolute(np.fft.fft(Signal[:,0:-1,:], axis=1))
            else:
                FFT_Absolute = np.absolute(np.fft.fft(Signal, axis=1))
        elif (Signal.ndim == 1):
            if (Signal.size == 297428):
                FFT_Absolute = np.absolute(np.fft.fft(Signal[0:-1], axis=0))
            else:
                FFT_Absolute = np.absolute(np.fft.fft(Signal, axis=0))
        else:
            raise DoingError('The signal variable can only have 1, 2 or 3 dimensions!!')
        return FFT_Absolute
    else:
        raise DoingError('The signal variable is not an array!!')

def Modulation_Bands_Spectrum(Signal):
    """
    Calcula el espectro de las descomposiciones en las m_bandas, 
    utilizando la transformada de Fourier.

    Parámetros:
        Signal: tipo numpy.ndarray
                Matriz de las descomposiciones de las m_bandas, en formato:
                -> 3 dimension (M_Bandas, Bandas, Muestras) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas, Muestras) 
                -> 5 dimensiones (Señales, M_Bandas, Bandas, Muestras, Epocas)
                
    Devuelve:
        Spectrum: tipo numpy.ndarray
                matriz con los espectros de cada una de las descomposiciones de las 
                m_bandas, en formato:
                -> 3 dimension (M_Bandas, Bandas, Muestras) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas, Muestras) 
                -> 5 dimensiones (Señales, M_Bandas, Bandas, Muestras, Epocas)
    """
    if (type(Signal) == np.ndarray):
        if (Signal.ndim == 3):
            M_Bands, Bands, Values = Signal.shape
            if (Values == 297428):
                Spectrum = np.zeros((M_Bands, Bands, Values-1))
            else:
                Spectrum = np.zeros((M_Bands, Bands, Values))
            for M_Band in range(0, M_Bands):
                for Band in range(0, M_Band+1):
                    Spectrum[M_Band, Band, :] = Signal_Spectrum(Signal[M_Band, Band, :])
        elif (Signal.ndim == 4):
            Num_Signals, M_Bands, Bands, Values = Signal.shape
            if (Values == 297428):
                Spectrum = np.zeros((Num_Signals, M_Bands, Bands, Values-1))
            else:
                Spectrum = np.zeros((Num_Signals, M_Bands, Bands, Values))
            for M_Band in range(0, M_Bands):
                for Band in range(0, M_Band+1):
                    Spectrum[:, M_Band, Band, :] = Signal_Spectrum(Signal[:, M_Band, Band, :])
        elif (Signal.ndim == 5):
            Num_Signals, M_Bands, Bands, Values, Epochs = Signal.shape
            if (Values == 297428):
                Spectrum = np.zeros((Num_Signals, M_Bands, Bands, Values-1, Epochs))
            else:
                Spectrum = np.zeros((Num_Signals, M_Bands, Bands, Values, Epochs))
            for M_Band in range(0, M_Bands):
                for Band in range(0, M_Band+1):
                    Spectrum[:, M_Band, Band, :, :] = Signal_Spectrum(Signal[:, M_Band, Band, :, :])
        else:
            raise DoingError('The signal variable can only have 3, 4 or 5 dimensions!!')
        return Spectrum
    else:
        raise DoingError('The signal variable is not an array!!')

def Parseval_Theorem(Spectrum):
    """
    Aplica el teorema de Parseval al espectro de una señal.

    Parámetros:
        Spectrum: tipo numpy.ndarray
                Arreglo de espectros, en formato:
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                -> 3 dimensiones (Señales, Muestras, Epocas)
                
    Devuelve:
        Energy: tipo numpy.ndarray
                Arreglo de energias.
                -> 1 dimension Energia (es un escalar)
                -> 2 dimensiones (Energias)
                -> 3 dimensiones (Señales, Energias)
    """
    if (type(Spectrum) == np.ndarray):
        if (Spectrum.ndim == 2) or (Spectrum.ndim == 3):
            Energy = np.sum(Spectrum**2, axis=1) / Spectrum.shape[1]
        elif (Spectrum.ndim == 1):
            Energy = np.sum(Spectrum**2, axis=0) / Spectrum.size
        else:
            raise DoingError('The signal variable can only have 1, 2 or 3 dimensions!!')
        return Energy
    else:
        raise DoingError('The signal variable is not an array!!')

def Parseval_Theorem_Modulation_Bands(Spectrum):
    """
    Aplica el teorema de Parseval a una matriz con los espectros de las descomposiciones de las m_bandas.

    Parámetros:
        Spectrum: tipo numpy.ndarray
                Arreglo con los espectros de cada una de las descomposiciones de las m_bandas, 
                en formato:
                -> 3 dimension (M_Bandas, Bandas, Muestras) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas, Muestras) 
                -> 5 dimensiones (Señales, M_Bandas, Bandas, Muestras, Epocas)
                
    Devuelve:
        Energy: tipo numpy.ndarray
                Arreglo con los valores obtenidos de aplicar el teorema de parseval.
                -> 3 dimension (M_Bandas, Bandas) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas) 
                -> 5 dimensiones (Señales, M_Bandas, Bandas, Epocas)
    """
    if (type(Spectrum) == np.ndarray):
        if (Spectrum.ndim == 3):
            M_Bands, Bands, Values = Spectrum.shape
            Energy = np.zeros((M_Bands, Bands))
            for M_Band in range(0, M_Bands):
                for Band in range(0, M_Band+1):
                    Energy[M_Band, Band] = Parseval_Theorem(Spectrum[M_Band, Band, :]) 
        elif (Spectrum.ndim == 4):
            Num_Signals, M_Bands, Bands, Values = Spectrum.shape
            Energy = np.zeros((Num_Signals, M_Bands, Bands))
            for M_Band in range(0, M_Bands):
                for Band in range(0, M_Band+1):
                    Energy[:, M_Band, Band] = Parseval_Theorem(Spectrum[:, M_Band, Band, :]) 
        elif (Spectrum.ndim == 5):
            Num_Signals, M_Bands, Bands, Values, Epochs = Spectrum.shape
            Energy = np.zeros((Num_Signals, M_Bands, Bands, Epochs))
            for M_Band in range(0, M_Bands):
                for Band in range(0, M_Band+1):
                    Energy[:, M_Band, Band, :] = Parseval_Theorem(Spectrum[:, M_Band, Band, :, :]) 
        else:
            raise DoingError('The signal variable can only have 3, 4 or 5 dimensions!!')
        return Energy
    else:
        raise DoingError('The signal variable is not an array!!')
    
def Percentage_Modulation_Energy(Energy):
    """
    Calcular el PME (porcentaje de modulacion de energia) de cada una de las descomposiciones 
    de las m_bandas.

    Parámetros:
        Energy_Average: tipo numpy.ndarray
                Arreglo con los valores de energia de cada una de las descomposiciones de las m_bandas,
                en formato:
                -> 2 dimension (M_Bandas, Bandas) 
                -> 3 dimensiones (Señales, M_Bandas, Bandas) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas, Epocas)
            
    Devuelve:
        pme: tipo numpy.ndarray
                Arreglo con los valores obtenidos de PME. 
                -> 2 dimension (M_Bandas, Bandas) 
                -> 3 dimensiones (Señales, M_Bandas, Bandas) 
                -> 4 dimensiones (Señales, M_Bandas, Bandas)
    """
    if (type(Energy) == np.ndarray):
        if (Energy.ndim == 2):
            pme = (Energy*100) / Energy.sum()
        elif (Energy.ndim == 3):
            pme = np.zeros(Energy.shape)
            for Signal in range(0, Energy.shape[0]):
                pme[Signal,:,:] = (Energy[Signal, :, :]*100) / Energy[Signal, :, :].sum()
        elif (Energy.ndim == 4):
            Energy = np.mean(Energy, axis=3)
            pme = np.zeros(Energy.shape)
            for Signal in range(0, Energy.shape[0]):
                pme[Signal,:,:] = (Energy[Signal, :, :]*100) / Energy[Signal, :, :].sum()
        else:
            raise DoingError('The signal variable can only have 2, 3 or 4 dimensions!!')
        return pme
    else:
        raise DoingError('The signal variable is not an array!!')
    
def Amplitude_Modulation_Analysis(Signal, Fs, Bands=[[1.5,6],[6,8.5],[8.5,10.5],[10.5,12.5],[12.5,18.5],[18.5,21],[21,30],[30,45]], Method='filter' , Filt='FIR_filter'):
    """
    Aplica el analisis de modulacion de amplitud a una señal
    (por defecto a Delta, Theta, Alpha, Beta, Gamma).
    
    Parámetros:
         Signal: tipo numpy.ndarray
                Arreglo con los datos de la señal. En formato:
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                -> 3 dimensiones (Señales, Muestras, Epocas)
        
        Fs: tipo int 
                Valor de la frecuencia de muestreo de la señal.
        
        Opcionales:
            
        Bands: tipo list
                Una lista con las tuplas de cada una de las bandas que contienen 
                las frecuencias inicial y final. Por defecto se utiliza [(0.5,4),(4,8),(8,12),(12,30),(30,100)]
                
        Method: tipo str
                Un string que indica el tipo de metodo para la segunda descomposicion de las m-bandas.
                -> 'filter': Aplicando filtros. 
                -> 'hamming': Aplicando ventana Hamming.
        
        Filt: tipo str
                Un string que indica el tipo de filtro a utilizar para la descomposicion.
                -> 'FIR_filter': Filtro FIR 
                -> 'Hamming': filtro tipo FIR de ventana Hamming
                
    Devuelve:
        pme: tipo numpy.ndarray
                Arreglo con los valores obtenidos de PME.
                -> 1 dimension (M_Bandas, Bandas) 
                -> 2 dimensiones (Señales, M_Bandas, Bandas) 
                -> 3 dimensiones (Señales, M_Bandas, Bandas) 
    """
    if (type(Signal) == np.ndarray):
        if ((Signal.ndim == 1) or (Signal.ndim == 2) or (Signal.ndim == 3)):
            SubBands_Signal = SubBands_Decomposition(Signal, Fs, Bands=Bands, Filt=Filt)
            del Signal
            Envelope = Temporal_Envelopes(SubBands_Signal)
            del SubBands_Signal
            if Method == 'filter':
                MBands_Signal = Modulation_Bands_Decomposition(Envelope, Fs, M_Bands=Bands, Filt=Filt)
                del Envelope
                Spectrum = Modulation_Bands_Spectrum(MBands_Signal)
                del MBands_Signal
                Energy = Parseval_Theorem_Modulation_Bands(Spectrum)
                del Spectrum
            elif Method == 'hamming':
                Energy = Modulation_Bands_Decomposition_Hamming(Envelope, Fs, M_Bands=Bands)
                del Envelope
            else:
                raise DoingError('Unknown Method!!')
            pme = Percentage_Modulation_Energy(Energy)
            del Energy
            return pme
        else:
            raise DoingError('The signal variable can only have 1, 2 or 3 dimensions, or unknown filter!!') 
    else:
        raise DoingError('The signal variable is not an array!!')  

def Algorithm_Amplitude_Modulation_Analysis(Signal, Fs, Channels = True, Epochs = True, Bands=[(0.5,4),(4,8),(8,12),(12,30),(30,100)], Method='filter', Filt='FIR_filter'):
    """
    Aplica el Algoritmo de analasis de modulacion de amplitud a una señal.
    
    Parámetros:
         Signal: tipo numpy.ndarray
                Arreglo con los datos de la señal a aplicar el analisis de modulacion 
                de amplitud, en formato:  
                -> 1 dimension (Muestras)
                -> 2 dimensiones (Señales, Muestras)
                -> 3 dimensiones (Señales, Muestras, Epocas)
        
        Fs: tipo float
                Valor de la frecuencia de muestreo de la señal, en Hz.
        
        Opcionales:
            
        Channels: tipo int o tuple  
                Un numero entero, o una tupla que contiene los indices de los canales a 
                que se tomaran de la señal.
                Si no se especifica, por defecto se toman todos.
                
        Epochs: tipo int o tuple 
                Un numero entero, o una tupla que contiene los indices de las epocas 
                que se tomaran de los canales.
                Si no se especifican, por defecto se toman todas.
                
        Bands: tipo list
                Una lista con las tuplas de cada una de las bandas que contienen 
                las frecuencias inicial y final. Por defecto se utiliza [(0.5,4),(4,8),(8,12),(12,30),(30,100)]
         
        Method: tipo str
                Un string que indica el tipo de metodo para la segunda descomposicion de las m-bandas.
                -> 'filter': Aplicando filtros. 
                -> 'hamming': Aplicando ventana Hamming.
                
        Filt: tipo str
                Un string que indica el tipo de filtro a utilizar para la descomposicion.
                -> 'FIR_filter': Filtro FIR 
                -> 'Hamming': filtro tipo FIR de ventana Hamming
            
    Devuelve:
        pme: tipo numpy.ndarray
                Arreglo con los valores obtenidos de PME, en formato:
                -> (M_Bandas, Bandas) 
                -> (Señales, M_Bandas, Bandas)  
    """
    if (type(Signal) == np.ndarray) and ((type(Bands) == np.ndarray) or (type(Bands) == list)):
        if (Signal.ndim == 3):
            Num_Channels, Values, Num_Epochs = Signal.shape
            if (type(Epochs) == int):
                if (type(Channels) == int) or (type(Channels) == tuple):
                    pme = Amplitude_Modulation_Analysis(Signal[Channels,:,Epochs], Fs, Bands=Bands, Method=Method, Filt=Filt)
                elif ((type(Channels) == bool) and (Channels == True)):
                    pme = Amplitude_Modulation_Analysis(Signal[:,:,Epochs], Fs, Bands=Bands, Method=Method, Filt=Filt)
                else:
                    raise DoingError('The channels variable has an inappropriate type or value!!')
            elif ((type(Epochs) == bool) and (Epochs == True)):
                if (type(Channels) == int):
                    pme = Amplitude_Modulation_Analysis(np.reshape(Signal[Channels,:,:], (1, Values, Num_Epochs), order='F'), 
                                                        Fs, Bands=Bands, Method=Method, Filt=Filt)
                elif ((type(Channels) == bool) and (Channels == True)):
                    pme = Amplitude_Modulation_Analysis(Signal, Fs, Bands=Bands, Method=Method, Filt=Filt)
                elif (type(Channels) == tuple):
                    pme = Amplitude_Modulation_Analysis(Signal[Channels,:,:], Fs, Bands=Bands, Method=Method, Filt=Filt)
                else:
                    raise DoingError('The channels variable has an inappropriate type or value!!')
            elif (type(Epochs) == tuple):
                if (type(Channels) == int): 
                    pme = Amplitude_Modulation_Analysis(np.reshape(Signal[Channels,:,:][:,Epochs], (1, Values,len(Epochs)), order='F'), 
                                                        Fs, Bands=Bands, Method=Method, Filt=Filt)
                elif ((type(Channels) == bool) and (Channels == True)):
                    pme = Amplitude_Modulation_Analysis(Signal[:,:,Epochs], Fs, Bands=Bands, Method=Method, Filt=Filt)
                elif (type(Channels) == tuple):
                    pme = Amplitude_Modulation_Analysis(Signal[Channels,:,:][:,:,Epochs], Fs, Bands=Bands, Method=Method, Filt=Filt)
                else:
                    raise DoingError('The channels variable has an inappropriate type or value!!')
            else:
                raise DoingError('The epochs variable has an inappropriate type or value!!')
        elif (Signal.ndim == 2):
            Num_Channels, Values = Signal.shape
            if (type(Channels) == int) or (type(Channels) == tuple):
                pme = Amplitude_Modulation_Analysis(Signal[Channels,:], Fs, Bands=Bands, Method=Method, Filt=Filt)
            elif ((type(Channels) == bool) and (Channels == True)):
                pme = Amplitude_Modulation_Analysis(Signal, Fs, Bands=Bands, Method=Method, Filt=Filt)
            else:
                raise DoingError('The channels variable has an inappropriate type or value!!')
        elif (Signal.ndim == 1):
            pme = Amplitude_Modulation_Analysis(Signal, Fs, Bands=Bands, Method=Method, Filt=Filt)
        else:
            raise DoingError('The signal variable can only have 1, 2 or 3 dimensions!!') 
        return pme
    else:
        raise DoingError('The signal variable is not an array, and Bands variable is not a list or an array!!')

def Save_PME(pme, Channels = True, Path_Name_File = "", 
             Name_Bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'],
             Name_Channels = True):
    """
    Guarda el PME obtenido del algoritmo de analasis de modulacion de amplitud,
    en archivos .csv.
    
    Parámetros:
         pme: tipo numpy.ndarray
                Matriz con los valores obtenidos de PME en formato: 
                -> 2 dimensiones (M_Bandas, Bandas) 
                -> 3 dimensiones (Señales, M_Bandas, Bandas)  
        
        Opcionales:
                
        Channels: tipo int o tuple  
                Un numero entero, o una tupla que contiene los indices de los canales a 
                que se tomaran.
                Si no se especifica, por defecto se toman todos.
        
        Path_Name_File: tipo str
                Un string que indica la direccion donde se guardaran y el nombre para los archivos. 
                El formato del nombre del archivo guardado es:
                    Path_Name_File_PME_Channel_Canal.csv
                Si no se especifican, por defecto se deja vacio.
                
        Name_Bands: tipo list
                Una lista con los nombres (tipo str) de las bandas utilizadas para el calculo de PME.
                Por defecto se utiliza: ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
        
        Name_Channels: tipo list
                Una lista con los nombres (tipo str) de los canales que se van a guardar, deben
                estar en el mismo orden que los canales especificados.
                Por defecto los canales se nombran con el numeros de su indice.
        
    Devuelve:
        Done: tipo bool
                Es True si se guardo correctamente el archivo, de no ser asi retorna False.  
        
    """
    try:
        if(pme.ndim == 3):
            if((type(Name_Channels) == bool) and (Name_Channels == True)):
                if(type(Channels) == int):
                    File_pme = pd.DataFrame(pme[Channels,:,:],
                                            columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                            index = Name_Bands)
                    File_pme.to_csv(Path_Name_File+"_PME_Channel_"+str(Channels)+".csv")
                elif((type(Channels) == bool) and (Channels == True)):
                    for Channel in range(0, pme.shape[0]):
                        File_pme = pd.DataFrame(pme[Channel,:,:],
                                                columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                                index = Name_Bands)
                        File_pme.to_csv(Path_Name_File+"_PME_Channel_"+str(Channel)+".csv")
                elif(type(Channels) == tuple):
                    for Channel in Channels:
                        File_pme = pd.DataFrame(pme[Channel,:,:],
                                                columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                                index = Name_Bands)
                        File_pme.to_csv(Path_Name_File+"_PME_Channel_"+str(Channel)+".csv")
                else:
                    raise DoingError('The Channels variable has an inappropriate type or value!!')
                return True
            elif (type(Name_Channels) == list):
                if(type(Channels) == int):
                    File_pme = pd.DataFrame(pme[Channels,:,:],
                                            columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                            index = Name_Bands)
                    File_pme.to_csv(Path_Name_File+"_PME_Channel_"+Name_Channels[0]+".csv")
                elif((type(Channels) == bool) and (Channels == True)):
                    for Channel in range(0, pme.shape[0]):
                        File_pme = pd.DataFrame(pme[Channel,:,:],
                                                columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                                index = Name_Bands)
                        File_pme.to_csv(Path_Name_File+"_PME_Channel_"+Name_Channels[Channel]+".csv")
                elif(type(Channels) == tuple):
                    for i, Channel in enumerate(Channels):
                        File_pme = pd.DataFrame(pme[Channel,:,:],
                                                columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                                index = Name_Bands)
                        File_pme.to_csv(Path_Name_File+"_PME_Channel_"+Name_Channels[i]+".csv")
                else:
                    raise DoingError('The Channels variable has an inappropriate type or value!!')
                return True
            else:
                raise DoingError('The Name_Channels variable has an inappropriate type or value!!')            
        elif(pme.ndim == 2):
            if((type(Name_Channels) == bool) and (Name_Channels == True)):
                File_pme = pd.DataFrame(pme, columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                        index = Name_Bands)
                File_pme.to_csv(Path_Name_File+"_PME_Channel_"+str(0)+".csv")
            elif (type(Name_Channels) == list):
                File_pme = pd.DataFrame(pme, columns = list(map(lambda Band : 'M_'+Band, Name_Bands)), 
                                        index = Name_Bands)
                File_pme.to_csv(Path_Name_File+"_PME_Channel_"+Name_Channels[0]+".csv")
            else:
                raise DoingError('The Name_Channels variable has an inappropriate type or value!!')  
        else:
            raise DoingError('The signal variable can only have 2 or 3 dimensions!!') 
    except:
        return False
                                
def Load_PME(Path_Name_File, Name_Bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']):
    """
    Carga un archivo (formato .csv) que contine el PME.
    
    Parámetros:
        Path_Name_File: tipo str
                Un string que indica la direccion y nombre para los archivos. 
                Si no se especifican, por defecto se deja vacio.
             
        Opcionales:
                
        Name_Bands: tipo list
                Una lista con los nombres (tipo str) de las bandas utilizadas para el calculo de PME.
                Por defecto se utiliza: ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
            
    Devuelve:
        pme: tipo numpy.ndarray
                Matriz con los valores obtenidos de PME, en formato (M_Bandas, Bandas).
        
    """
    try:
        pme = pd.read_csv(Path_Name_File,
                          usecols = tuple(map(lambda Band : 'M_'+Band, Name_Bands)))
        return pme
    except:
        raise DoingError('Error loading the file '+Path_Name_File+' !!') 

def Load_Signal_Files_Save_PME(Paths_Files, Fs = True, Save_Paths = True, Channels = True, 
                               Epochs = True, Bands = [(0.5,4),(4,8),(8,12),(12,30),(30,100)], 
                               Name_Bands = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'],
                               Name_Channels = True, Method='filter', Filt='FIR_filter'):
    """
    Carga varios archivos en formato .mat que se encuentran en una misma carpeta, los 
    archivos contienen señales bajo el nombre de 'data'. Se calculan sus 
    respectivos PME y por ultimo guarda los PME en archivos de formato .csv.
    
    Parámetros:
        Paths_Files: tipo list
                Una lista con las direcciones (tipo str) de las carpetas donde se 
                encuentran los archivos .mat.
                
        Opcionales:
            
        Fs: tipo int 
                Valor de la frecuencia de muestreo de la señal (en Hz). Si no se especifica 
                se asume que el archivo .mat contiene la frecuencia bajo el nombre de 'srate'.
                
        Save_Paths: tipo list
                Una lista con las direcciones (tipo str) de las carpetas donde se guardaran los archivos.
                Por defecto se toma la misma ruta respectiva de los archivos .mat.
                
        Channels: tipo int o tuple  
                Un numero entero, o una tupla que contiene los indices de los canales a 
                que se tomaran de la señal.
                Si no se especifica, por defecto se toman todos.
                
        Epochs: tipo int o tuple 
                Un numero entero, o una tupla que contiene los indices de las epocas 
                que se tomaran de los canales.
                Si no se especifican, por defecto se toman todas.
                
        Bands: tipo list
                Una lista con las tuplas de cada una de las bandas que contienen 
                las frecuencias inicial y final. Por defecto se utiliza [(0.5,4),(4,8),(8,12),(12,30),(30,100)]
        
        Name_Bands: tipo list
                Una lista con los nombres (tipo str) de las bandas utilizadas para el calculo de PME.
                Por defecto se utiliza: ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']
        
        Name_Channels: tipo list
                Una lista con los nombres (tipo str) de los canales que se van a guardar, deben
                estar en el mismo orden que los canales especificados.
                Por defecto los canales se nombran con el numeros de su indice.
                
        Method: tipo str
                Un string que indica el tipo de metodo para la segunda descomposicion de las m-bandas.
                -> 'filter': Aplicando filtros. 
                -> 'hamming': Aplicando ventana Hamming.
                
        Filt: tipo str
                Un string que indica el tipo de filtro a utilizar para la descomposicion.
                -> 'FIR_filter': Filtro FIR 
                -> 'Hamming': filtro tipo FIR de ventana Hamming
                
    Devuelve:
        No retorna ningun valor
        
    """
    if((type(Save_Paths) == bool) and (Save_Paths == True)):
        Save_Paths = Paths_Files[:]
    for i in range(0,len(Paths_Files)):
        Path = Paths_Files[i]
        Save_Path = Save_Paths[i]
        for root, dirs, files in os.walk(Path):  
            if files:
                for file in files:
                    if os.path.splitext(file)[1] == '.mat':
                        File_Name = os.path.splitext(file)[0]
                        Signal = np.squeeze(sio.loadmat(root+file)['data'])
                        if Fs == True:
                            Fs = float(np.squeeze(sio.loadmat(root+file)['srate']))
                        pme = Algorithm_Amplitude_Modulation_Analysis(Signal,
                                Fs, Channels = Channels, Epochs = Epochs, 
                                Bands = Bands, Method=Method, Filt = Filt)
                        del Signal
                        Save_PME(pme, Channels = Channels, 
                                 Path_Name_File = Save_Path+File_Name, Name_Bands = Name_Bands,
                                 Name_Channels = Name_Channels)
                        del pme 
                        print("\nFinish with "+File_Name)
                        
def Load_Table_PME(Path_Files, Name_Channels, Name_Files=True, Name_Bands=['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma']):
    """
    Carga varios archivos (formato .csv) que continen matrices de PME, y genera una matriz
    que contiene todos los PME.
    
    Parámetros:
         Dir: tipo str
                String con la direccion de la carpeta donde se encuentran los archivos.
                
        Num_Files: tipo int 
                Numero de archivos a cargar.
            
        Canal: tipo int 
                Numero de canales a cargar.
             
        Opcionales:
                
        Epoca: tipo int 
                Numero de Epocas a cargar.
                Si es 0, se asume que el nombre de los archivos no especifican epocas.
                
        Name1: tipo str
                Un string que indica el nombre comun de los archivos. Primera parte 
                entre los numeros que diferencia los archivos.
                Si no se especifican, por defecto es "C0".
                
        Name2: tipo str
                Un string que indica el nombre comun de los archivos. Segunda parte 
                entre los numeros que diferencia los archivos.
                Si no se especifican, por defecto es "_".
            
    Devuelve:
        Table_pme: tipo numpy.ndarray
                Matriz con todos las matrices de PME cargadas (Files x Canales x Bandas x M_Bandas)
        
    """
    Path = Path_Files
    Signals_List = []
    for root, dirs, files in os.walk(Path):  
        if files:
            for file in files:
                File_Name, ext = os.path.splitext(file)
                Name_Signal = File_Name.split("_Channel_")[0]
                if((ext == '.csv') and (not Name_Signal in Signals_List)):
                    Signals_List.append(Name_Signal)
    Table_pme = np.zeros((len(Signals_List), len(Name_Channels) ,len(Name_Bands), len(Name_Bands)))
    num_errors = 0
    for File, Name_Signal in enumerate(Signals_List):
        for Channel, Name_Channel in enumerate(Name_Channels):
            try:
                pme = Load_PME(Path_Name_File = Path+Name_Signal+"_Channel_"+Name_Channel+'.csv', Name_Bands=Name_Bands)
                Table_pme[File,Channel,:,:] = pme.values 
            except:
                num_errors += 1
                print('\nError with: '+Path+Name_Signal+"_Channel_"+Name_Channel+'.csv\n')
    print('\nTotal Errores: '+str(num_errors)+'\n')
    return Table_pme, Signals_List   

             