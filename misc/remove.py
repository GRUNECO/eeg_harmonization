import os
import glob

'''
Code used to delete unwanted processed files

Uncomment lines 67 and 96 (os.remove(i[j])) only if you are sure they are the files to be deleted.

'''
def path_to_remove_without_visits(path,sub,name,ext):   
    '''
    Function created to return the path to be deleted in databases without visits

    Inputs:
        path: path where all the files of all the subjects are processed 
        sub: name of a subject folder
        name: ending of the desired file to be deleted
        ext: file extension to be deleted
    
    Output:
        icpowers_json_files: path to delete

    '''
    path_def = path+'\\'+sub+'\\eeg\\'+name+ext 
    if name in path_def:
        icpowers_json_files = glob.glob(path+'\\'+sub+'\\eeg\\*'+name+ext)    
    return icpowers_json_files

def path_to_remove_visits(path,sub,v,name,ext):    
    '''
    function created to return the path to be deleted in databases with visits

    Inputs:
        path: path where all the files of all the subjects are processed 
        name: ending of the desired file to be deleted
        sub: name of a subject folder
        v: name of the visit folder
        ext: file extension to be deleted
    
    Output:
        icpowers_json_files: path to delete
    '''
    path_def = path+'\\'+sub+'\\'+v+'\\eeg\\'+name+ext
    if name in path_def:
        icpowers_json_files = glob.glob(path+'\\'+sub+'\\'+v+'\\eeg\\*'+name+ext) 
    return icpowers_json_files

def remove_data_without_visits(path,name,ext):
    '''
    function created to remove the paths to be deleted in databases without visits
    Inputs:
        path: path where all the files of all the subjects are processed 
        name: ending of the desired file to be deleted
        ext: file extension to be deleted
    
    '''
    subjects = os.listdir(path)
    json_remove=[]
    for sub in subjects:
        suffix = "sub"
        if sub.endswith(suffix,0,3) == True:
            json_remove.append(path_to_remove_without_visits(path,sub,name,ext))
    for i in json_remove:
        for j in range(0,2):
            try:
                print(i[j])
                #os.remove(i[j])
            except:
                continue


def remove_data_visits(path,name,ext):
    '''
    function created to remove the paths to be deleted in databases with visits

    Inputs:
        path: path where all the files of all the subjects are processed 
        name: ending of the desired file to be deleted
        ext: file extension to be deleted
    
    Output:
        icpowers_json_files: path to delete
    '''
    subjects = os.listdir(path)
    json_remove=[]    
    for sub in subjects:
        suffix = "sub"
        if sub.endswith(suffix,0,3) == True:
            ses = os.listdir(path+'/'+sub)
            for v in ses:
                json_remove.append(path_to_remove_visits(path,sub,v,name,ext))
    for i in json_remove:
        for j in range(0,2):
            try:
                print(i[j])
                #os.remove(i[j])
            except:
                continue
    

path = r'D:\BASESDEDATOS\biomarcadoresprueba\derivatives\sovaharmony'
name = [']_eeg',']_stats','_powers','norm_eeg','powers_norm']
ext = ['.fif','.json','.txt']


remove_data_without_visits(path,name[4],ext[2])
remove_data_visits(path,name[0],ext[0])