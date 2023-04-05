import pandas as pd
import numpy as np
from functools import reduce
from sovaharmony.datasets import Estudiantes_CE
from sovaharmony.datasets import Estudiantes_OE
from sovaharmony.datasets import Estudiantes_T2
from sovaharmony.datasets import Estudiantes_T3
from sovaharmony.datasets import Residentes_CE
from sovaharmony.datasets import Residentes_OE
from sovaharmony.datasets import Residentes_T1
from sovaharmony.datasets import Residentes_T2
from sovaharmony.datasets import Residentes_T3
from sovaharmony.datasets import Estudiantes2021_OE
from sovaharmony.datasets import Estudiantes2021_CE
from sovaharmony.datasets import Estudiantes2021_T1
from sovaharmony.datasets import Estudiantes2021_T2



THE_DATASETS=[
              Estudiantes2021_OE,
              Estudiantes2021_CE,
              Estudiantes2021_T1,
              Estudiantes2021_T2,
              Estudiantes_CE,
              Estudiantes_OE,
              #Estudiantes_T1,# no da
              Estudiantes_T2,
              Estudiantes_T3,
              Residentes_CE,
              Residentes_OE,
              Residentes_T1,
              Residentes_T2,
              Residentes_T3,
              ]

#m = ['cohfreq','entropy','power','sl','crossfreq']
m = ['Coherence','Entropy','Power','SL','Cross Frequency']
s = ['IC']
pd_task=[]     
# for dataset in THE_DATASETS:
#     for space in s:
#         list_data=[]
#         for met in m:
#             path_='{path}/derivatives/data_long/{space}/data_long_{task}_{metric}_{name_db}_roi.feather'.format(path=dataset['input_path'],space=space,task=dataset['layout']['task'],metric=met,name_db=dataset['name']).replace('\\','/')
#             data=pd.read_feather(path_)
#             list_data.append(data[met])
#             #print(len(data['participant_id']))
#         list_data.insert(0,data)
#         pd_task.append(pd.concat(list_data[:-1],axis=1))

# path_save=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena'
# new_name='data_long_features_roi'
# data_concat=pd.concat(pd_task,axis=0)
# data_concat.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_save,name=new_name))

paths=[]
pd_task=[] 
m = ['cohfreq','entropy','power','sl','crossfreq']
s = ['IC']
cont_row=0
cont_columns=0

# for dataset in THE_DATASETS:
#     for space in s:
#         list_data=[]
#         for met in m:
#             path_='{path}/derivatives/data_columns/{space}/data_{task}_{metric}_columns_components_{name_db}.feather'.format(path=dataset['input_path'],space=space,task=dataset['layout']['task'],metric=met,name_db=dataset['name']).replace('\\','/')
#             paths.append(path_)
#             data=pd.read_feather(path_)
#             list_data.append(data)
#         merged_data = reduce(lambda left, right: pd.merge(left, right, on=['participant_id','visit','condition','group','database']), list_data)
#     pd_task.append(merged_data)
# data_concat=pd.concat(pd_task,axis=0)
# path_save=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena'
# new_name='data_columns_features_ic'
# print(data_concat)
# data_concat.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_save,name=new_name))
# print(data_concat.shape)
