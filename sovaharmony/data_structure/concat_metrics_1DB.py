import pandas as pd
import numpy as np
from functools import reduce
import pandas as pd 
import tkinter as tk
from tkinter.filedialog import askdirectory
from sovaharmony.datasets import Estudiantes2021_OE

THE_DATASETS=[
             Estudiantes2021_OE,
             ]

#m = ['coherence','entropy','power','sl','crossfreq']
m = ['Power']
s = ['roi','ic']
t = ['harmonized','sova']
g = ['DTAControl','G1Control','G1G2']
tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
path = askdirectory() 
print("user chose", path, "for open files")
path_save=askdirectory() 
print("user chose", path, "for save file")
pd_task=[]
format_long=False
if format_long:  
    for type in t:
        for space in s:
            for group in g:   
                list_data=[]
                for met in m:
                    path_='{path}/{space}/data_long_{metric}_{space}_{type}_{name_db}.feather'.format(path=path,space=space,type=type,metric=met,name_db=group).replace('\\','/')
                    data=pd.read_feather(path_)
                    if met == 'sl':
                        list_data.append(data[met.upper()])
                    elif met == 'crossfreq':
                        list_data.append(data['Cross Frequency'])
                    else:
                        list_data.append(data[met.capitalize()])
                list_data.insert(0,data)
                pd_task.append(pd.concat(list_data[:-1],axis=1))
            new_name='data_long_features_{type}_{space}'.format(type=type,space=space)
            data_concat=pd.concat(pd_task,axis=0)
            data_concat.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_save,name=new_name))
else:
    for dataset in THE_DATASETS:
        for space in s:
            list_data=[]
            for met in m:
                path_='{path}/derivatives/data_columns/{space}/data_{task}_{metric}_columns_components_{name_db}.feather'.format(path=dataset['input_path'],space=space,task=dataset['layout']['task'],metric=met,name_db=dataset['name']).replace('\\','/')
                data=pd.read_feather(path_)
                list_data.append(data)
            merged_data = reduce(lambda left, right: pd.merge(left, right, on=['participant_id','visit','condition','group','database']), list_data)
        pd_task.append(merged_data)
    data_concat=pd.concat(pd_task,axis=0)
    path_save=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena'
    new_name='data_columns_features_ic'
    print(data_concat)
    data_concat.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_save,name=new_name))
    print(data_concat.shape)
