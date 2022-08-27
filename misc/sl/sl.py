"""
@author: Brayan Hoyos Madera, Universidad de Antioquia, leobahm72@gmail.com

Inspired by: HERMES Toolbox 2016-01-28
    Niso G, Bruna R, Pereda E, Gutiérrez R, Bajo R., Maestú F, & del-Pozo F. 
    HERMES: towards an integrated toolbox to characterize functional and 
    effective brain connectivity. Neuroinformatics 2013, 11(4), 405-434. 
    DOI: 10.1007/s12021-013-9186-1. 
    
"""

#Import of modules
from numpy import ones
from numpy import zeros
from numpy import shape
from numpy import float64
from numpy import arange
from numpy import mean
from numpy import floor
from numpy import ceil
from numpy import logical_and
from numpy import fabs
from numpy import sum as npsum
from numpy import where
from numpy import array
from numpy import transpose
from numpy import sqrt
from numpy import sort
from numpy import dot 
from numpy import diag
from numpy import split
from math import ceil as math_ceil

#Create the funtions

def get_sl(data, fs, time_delay=None, w1=None, w2=None, pref=None):
    '''
    Function responsible for configuring and executing the calculation of the 
    synchronization likelihood of a set of signals.

    :param data: numpy array, required.
        The data that will be processed for the  sl() function.

    :param fs: int, required.
        Sampling frequency with wich the dta was obtained.

    :param time_delay: int, optional.
        Delay for the number of iterations that will be used to calculate the 
        synchronzation likelihood.
        Default is: None.

    :param w1: int, optional.
        window_1: Theiler correction for autocorrelation
        Default is: None.
        
    :param w2: int, optional.
        window_2: used to sharpen the time resolution of synchronization measure
        Default is: None
        
    :param pref: float, optional.
        Default is: None.

    :return sl_output: numpy array.
        Matrix with dimensions channels*channels that contained the average of 
        the measure of the sinchronization likelihood between each of the 
        channels of the input data.
    
    '''
    
    size = data.shape

    if len(size) != 3 and len(size) == 2:
        data = segment_signal(data, fs)
    elif len(size) == 3:
        pass
    else:
        print("The dimensions of the data vector are not supported.",
              "They must be of 2 or 3 dimensions, it was entered %i dimensions"
              %len(size))
        exit()

    #Default values.
    if time_delay == None: time_delay = 4
    
    if w1 == None: w1 = 16
    
    if w2 == None: w2 = 215
    
    if pref == None: pref = 0.05
    
    measure = "SL"
    
    config = (time_delay, 3, w1, w2, pref, measure)

    #Execute the routine.
    sl_output = sl_methods(data, config)
    
    return mean(sl_output, 2)

def segment_signal(signal, fs):
    '''
    Function responsible of segmenting the data if they have a two dimensions.
    Generate a array of three dimensions channels*samples*trials.

    :param signal: numpy array, required.
        The data to be segmented. These must have two dimensions,
        channnels*samples.

    :param fs: int, requered.
        Sampling frequency with wich the dta was obtained.

    :retunr: numpy array with segmented data with three dimensions,
        channels*samples*trials.  
        
    '''
    #Get the size of input data.
    (channels, samples) = signal.shape
    #Get the residue using the module.
    residue = samples%(fs*2)#fs*2 because segment each two seconds
    time = samples//fs #Get the time of register
    #Segment the samples each two seconds, erasing the residue data.
    data = array(split(signal[:, 0:(samples-int(residue))], int(time//2),1))
    #Config the data to channels*samples*trials
    data = data.transpose((1,2,0))
    return data 

def sl_methods(data,config):
    '''
    Function responsible for preparing the input data to calculate the 
    sinchronization likelihood throungh the sl() function.
    
    :param data: numpy array, required.
        The data that will be processed for the  sl() function. must be  of 
        three dimensions array which contains the channels, samples and trials
        for the input data of interest.
    
    :param config: Tuple | List, required.
        It contains the configuration that will be passed  to  the sl() function.
        The fields that contains must be entered in the following order:
        config = (time_delay, dimensions, window_1, window_2, pref, measures)
        or
        config = [time_delay, dimensions, window_1, window_2, pref, measures]
        
        Default is: config = (4, 3, 16, 215, 0.05, "SL") 
        
    :returns: numpy array with the mean of the calculate of sinchronization 
        likelihood. It's a matrix of channels*channels.
                             
    '''
    #Transpose the matrix moving samples with the channels.
    data = data.transpose((1,0,2))
    #Get the size of input data.
    (samples, channels, trials) = data.shape
    
    #Check that measures contains in the data are of SL
    if config[5].upper() == 'SL':
        #Reserves the needed memory.
        sl_output = ones((channels, channels, trials), dtype=float64)

    #Iterate over trials of the data.   
    for trial in arange(0, trials, dtype=int):
        #Calculate synchronization likelihood with the sl() funtion to each matrix
        #of data.
        sl_output[:, :, trial] = sl(data[:, :, trial], config)
    #Return the average of the data.
    return sl_output
 
def sl(data, config):
    '''
    This function takes the input data and return the synchronization
    likelihood.

    :param data: numpy array
        The input data file must contain M columns and N rows of numbers. These
        numbers correspond to the N samples for each of the M channels.
    
    :param config: Tuple | List, required.
        It contains the configuration that will be passed  to  the sl() function.
        The fields that contains must be entered in the following order:
        config = (time_delay, dimensions, window_1, window_2, pref, measures)
        or
        config = [time_delay, dimensions, window_1, window_2, pref, measures]
            window_1: Theiler correction for autocorrelation
            window_2: used to sharpen the time resolution of synchronization measure
            
        Default is: config = (4, 3, 16, 215, 0.05, "SL") 
    
    :return: numpy array.
        Numpy array with synchronization likelihood to the input data. The 
        dimensions of de array are channels*channels. 
    '''
    #Get the size of the input data.
    (samples, channels) = data.shape

    #Get the information contained in the config variable.
    time_delay = config[0]
    dimensions = config[1]
    w1 = config[2]
    w2 = config[3]
    pref = config[4]

    #It works as a third resolution window when calculating the synchronization 
    #likelihood.
    SPEED = 16

    #Calculate the number of iterations.
    num_iterations = int(floor((samples - time_delay * (dimensions - 1)) / 
                               SPEED) - ceil(1 / SPEED) + 1)

    #calculate the synchronization likelihood matrix.
    hit_matrix = synchronization(data,config, num_iterations, SPEED)    

    #sum the hit matrix across time i, size (num_chan, num_chan).
    s_k1_temp = npsum(hit_matrix, 2)
    #at a (k,l) position, s_kl_temp contains the number of hits occuring at both 
    #channels k & l,cover all i & j
    #at a (k,k) position, s_kl_temp contains the number of hits at channel k, 
    #over all i & j
    hit_diag = diag(s_k1_temp)
    
    s_k1_matrix = hit_diag.transpose() * ones(
        (1,channels)) + ones((channels,1)) * hit_diag
    
    #if S(k,k) == 0 & S(l,l) == 0 then S(k,l) must also be 0.
    #this calculation protects against division by 0
    s_k1_matrix = s_k1_matrix + (s_k1_matrix == 0)
    
    s_k1_matrix = 2 * s_k1_temp / s_k1_matrix
    
    return s_k1_matrix

def synchronization(data, config, num_it, speed):
    '''
    This function takes the input data and calculate the synchronization
    likelihood. Continuation of sl() function.

    :param data: numpy array
        The input data file must contain M columns and N rows of numbers. These 
        numbers correspond to the N samples for each of the M channels.
    
    :param config: Tuple | List, required.
        It contains the configuration that will be passed  to  the sl() function.
        The fields that contains must be entered in the following order:
        config = (time_delay, dimensions, window_1, window_2, pref, measures)
        or
        config = [time_delay, dimensions, window_1, window_2, pref, measures]
        
        Default is: config = (4, 3, 16, 215, 0.05, "SL")
        
    :param num_it: numpy array.
        Is the number iterations.

    :param speed: int.
        It works as a third resolution window when calculating the synchronization
        likelihood.
    
    :return: numpy array.
        Numpy array with synchronization likelihood to the input data. The 
        dimensions of de array are channels*channels. 
    '''
    #Get the size of the input matrix
    (samples, channels) = data.shape

    #Get the information contained in the config variable.
    time_delay = config[0]
    dimensions = config[1]
    w1 = config[2]
    w2 = config[3]
    pref = config[4]

    #Reserves the needed memory.
    epsilon = ones((channels, 1), dtype=float64)
    hit_matrix = zeros((channels, channels, num_it), dtype=float64)
    counter = 0

    #Get the range of iterations.
    range = arange(1, (samples - time_delay*(dimensions - 1) + 1), dtype=int)
    
    for i in range:
        if i % speed == 0 and i!=0:
            #Calculate the vector of valid range positions
            valid_range = logical_and(fabs(i - range) > w1,
                                      fabs(i - range) < w2).astype(int)
            num_validj = npsum(valid_range)#Number of valid range positions

            #Construct compressed table of euclidean distances.
            euclid_table = zeros((channels, num_validj), dtype = float64)
            #Get positions where the valid range is 1.
            valid_values = array(where(valid_range == 1))
            #Get the size of the array valid_values
            (row, col) = valid_values.shape
            col_position = arange(0, col, dtype=int)
            
            row_data1 = array(time_delay * arange(0, dimensions, dtype=int)
                              ) + (i - 1)
            row_data2 = zeros((dimensions, col), dtype=int)
            row_data2[:, :] = valid_values[:]
            row_data2 = row_data2.transpose() + array(
                time_delay * arange(0, dimensions, dtype=int))
            k_values = arange(0, channels, dtype=int)
            for k in k_values:
                #euclid4 not explicity called; saves about 25% of time
                euclid_table[k, col_position] = sqrt(sum(((data[
                    row_data1, k]-data[row_data2, k]).transpose()) ** 2))

            
            #construct table of epsilons
            #epsilon(k): the actual threshold distance such that the fraction
            #of all distances |X_{k,i} - X_{k,j}| less than epsilon[k, i] is Pref
            for k in k_values:
                sorted_table = sort(euclid_table[k, :])                
                epsilon[k] = sorted_table[(math_ceil(pref * num_validj) - 1)]
            #construct 'hit' table, determine if
            #|X_{k,i} - X_{k,j}| <= epsilon_x for each k & i. 
            hit_table = (euclid_table <= (epsilon * 
                                           ones(1, num_validj))).astype(int)
            #Determine the number of hits occuring at both channels
            hit_table = dot(hit_table, hit_table.transpose())
            #store hit_table in a 3-D array
            hit_matrix[:, :, counter] = hit_table
            #Increase the counter.
            counter += 1
            
    return hit_matrix
                     
