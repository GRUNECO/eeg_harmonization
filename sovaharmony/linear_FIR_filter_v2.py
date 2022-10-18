# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 10:22:45 2018

@author: John Fredy Ochoa - Marcos Lorenzo Usuga
"""

# %%
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def firws(m, f , w , t = None):
    """
    Designs windowed sinc type I linear phase FIR filter.

    Parameters:
        
        m: scalar or int
            filter order.
        
        f: scalar or numpy.ndarray
            cutoff frequency/ies (-6 dB;pi rad / sample).
                
        w: numpy.ndarray
            vector of length m + 1 defining window. 
            
        t: string (opcional)
            'high' for highpass, 'stop' for bandstop filter. {default low-/bandpass}
                
    Returns:
        
        b: numpy.ndarray
            filter coefficients 
    """
    
    try:
        m = int(m)
        if  (m%2 != 0) or (m<2):
            print(type(m))
            print('Filter order must be a real, even, positive integer.')
            return False
    except (ValueError, TypeError):
        print('Filter order must be a real, even, positive integer.')
        return False
    
    if (not type(f) is np.ndarray):
        print('the variable f must be ndarray type.')
        return False
    
    f = np.squeeze(f)
    if (f.ndim > 1) or (f.size > 2):
        print('the variable f must be scalar or vector of two values.')
        return False
    f = f / 2; 
    
    if np.any(f <= 0) or np.any(f >= 0.5):
        print('Frequencies must fall in range between 0 and 1.')
        return False
    
    w = np.squeeze(w)
    if (f.ndim == 0):
        b = fkernel(m, f, w)
    else:
        b = fkernel(m, f[0], w)
    if (f.ndim == 0) and (t == 'high'):
        b = fspecinv(b)
    elif (f.size == 2):
        b = b + fspecinv(fkernel(m, f[1], w))
        if t == None or (t != 'stop'):
            b = fspecinv(b)        
    return b

# Compute filter kernel
def fkernel(m, f, w):
    m = np.arange(-m/2, (m/2)+1)
    b = np.zeros((m.shape[0]))
    b[m==0] = 2*np.pi*f # No division by zero
    b[m!=0] = np.sin(2*np.pi*f*m[m!=0]) / m[m!=0] # Sinc
    b = b * w # Window
    b = b / np.sum(b) # Normalization to unity gain at DC
    return b

## Spectral inversion
def fspecinv(b):
    b = -b
    b[int((b.shape[0]-1)/2)] = b[int((b.shape[0]-1)/2)]+1
    return b

def mfreqz(b,a,order,nyq_rate = 1):
    
    """
    Plot the impulse response of the filter in the frequency domain

    Parameters:
        
        b: numerator values of the transfer function (coefficients of the filter)
        a: denominator values of the transfer function (coefficients of the filter)
        
        order: order of the filter 
                
        nyq_rate = nyquist frequency
    """
    
    w,h = signal.freqz(b,a);
    h_dB = 20 * np.log10 (abs(h));
    
    plt.figure();
    plt.subplot(311);
    plt.plot((w/max(w))*nyq_rate,abs(h));
    plt.ylabel('Magnitude');
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)');
    plt.title(r'Frequency response. Order: ' + str(order));
    [xmin, xmax, ymin, ymax] = plt.axis();
    plt.grid(True);
    
    plt.subplot(312);
    plt.plot((w/max(w))*nyq_rate,h_dB);
    plt.ylabel('Magnitude (db)');
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)');
    plt.title(r'Frequency response. Order: ' + str(order));
    plt.grid(True)
    plt.grid(True)
    
    
    plt.subplot(313);
    h_Phase = np.unwrap(np.arctan2(np.imag(h),np.real(h)));
    plt.plot((w/max(w))*nyq_rate,h_Phase);
    plt.ylabel('Phase (radians)');
    plt.xlabel(r'Normalized Frequency (x$\pi$rad/sample)');
    plt.title(r'Phase response. Order: ' + str(order));
    plt.subplots_adjust(hspace=0.5);
    plt.grid(True)
    plt.show()

# %%
def eegfiltnew(senal, srate, locutoff = 0, hicutoff = 0, revfilt = 0):
    #Constants
    TRANSWIDTHRATIO = 0.25;
    fNyquist = srate/2;   
    
    if hicutoff == 0: #Convert highpass to inverted lowpass
        hicutoff = locutoff
        locutoff = 0
        revfilt = 1 #este valor se cambia para notch y tambien se debe cambiar en este caso
    if locutoff > 0 and hicutoff > 0:
        edgeArray = np.array([locutoff , hicutoff])
    else:
        edgeArray = np.array([hicutoff]);
    
    if np.any(edgeArray<0) or np.any(edgeArray >= fNyquist):
        print('Cutoff frequency out of range')
        return False    
    
    # Max stop-band width
    maxTBWArray = edgeArray.copy() # Band-/highpass
    if revfilt == 0: # Band-/lowpass
        maxTBWArray[-1] = fNyquist - edgeArray[-1];
    elif len(edgeArray) == 2: # Bandstop
        maxTBWArray = np.diff(edgeArray) / 2;
    maxDf = np.min(maxTBWArray);
    
    # Default filter order heuristic
    if revfilt == 1: # Highpass and bandstop
        df = np.min([np.max([maxDf * TRANSWIDTHRATIO, 2]) , maxDf]);
    else: # Lowpass and bandpass
        df = np.min([np.max([edgeArray[0] * TRANSWIDTHRATIO, 2]) , maxDf]);
        
    filtorder = 3.3 / (df / srate); # Hamming window
    filtorder = np.ceil(filtorder / 2) * 2; # Filter order must be even.
    
    
    print('pop_eegfiltnew() - performing ' + str(filtorder + 1) + ' point filtering.');
    print('pop_eegfiltnew() - transition band width: ' + str(df) + ' Hz');
    print('pop_eegfiltnew() - passband edge(s): ' + str(edgeArray) + ' Hz', )
    # Passband edge to cutoff (transition band center; -6 dB)
    dfArray = [[df, [-df, df]] , [-df, [df, -df]]];
    cutoffArray = edgeArray + np.array(dfArray[revfilt][len(edgeArray) - 1]) / 2;
    print('pop_eegfiltnew() - cutoff frequency(ies) (-6 dB): '+str(cutoffArray)+' Hz\n');
    # Window
    winArray = signal.hamming(int(filtorder) + 1);
    # Filter coefficients
    if revfilt == 1:
        filterTypeArray = ['high', 'stop'];
        b = firws(filtorder, cutoffArray / fNyquist, winArray, filterTypeArray[len(edgeArray) - 1]);
    else:
        b = firws(filtorder, cutoffArray / fNyquist, winArray);
    print('pop_eegfiltnew() - filtering the data (zero-phase)');
    
    mfreqz(b,1,filtorder, fNyquist);
    
    signal_filtered = signal.filtfilt(b, 1, senal);#
    return signal_filtered;

#%%
#    
#import scipy.io as sio;
#import matplotlib.pyplot as plt
##loading data
#mat_contents = sio.loadmat('C:\\Users\\JohnFredyOchoa\\Google Drive\\mis_exposiciones\\filtrado_senales_biologicas\\senal.mat')
##los datos se cargan como un diccionario, se puede evaluar los campos que contiene
#print("Los campos cargados son: " + str(mat_contents.keys()));
##la senal esta en el campo data
#senal_org = mat_contents['data'];
#
#senal = senal_org[0,:]
#longitud_original = senal.shape[0];
##pasa bajas
#senal_filtrada = eegfiltnew(senal, 1000, 0 , 10, 0);
##plt.plot(senal_filtrada[0,:])
#plt.plot(senal_filtrada[0:2000]);
#plt.plot(senal[0:2000]);
#plt.show()