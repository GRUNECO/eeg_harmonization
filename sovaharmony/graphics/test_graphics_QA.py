import pandas as pd 
from graphics_QA import create_check
from graphics_QA import stats_pair
from graphics_QA import graphics
from graphics_QA import table_groups_DB

from sovaharmony.utils import concat_df
import matplotlib.pyplot as plt

path=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena' #Cambia dependieron de quien lo corra
database='Estudiantes2021'
save_path=r'D:\XIMENA\BIDS\{database}\derivatives'.format(database=database).replace('\\','/')



#data loading
data_ic=pd.read_feather(r'{path}\data_long_features_ic.feather'.format(path=path))
data_roi=pd.read_feather(r'{path}\data_long_features_roi.feather'.format(path=path))

m = ['Coherence','Entropy','Power','SL']
colors=["#FF784F","#2FE6DE","#31B86B"]
#colors=["#FF784F","#FDAE61", "#FEE08B","#2FE6DE","#31B86B"]
filters=['visit', 'condition']
data_roi=data_roi.dropna(axis=0)
bands=list(data_roi.Band.unique())
ids=['Component','ROI']


# QA in pre-processing 
data_prep=concat_df(save_path+'/*PREP.feather')
type='Metric_value'
x='State'
sessions=list(data_prep.Session.unique())
for i,visit in enumerate(sessions):
        try:
            data=data_prep[data_prep['Session']==visit]
            fig_prep=graphics(data,
                    type,
                    path,
                    name_band=None,
                    id='Metric',
                    id_cross=None,
                    num_columns=3,
                    save=False,
                    plot=False,
                    kind='box',
                    palette=colors,
                    hue='task',
                    x=x,
                    col_legend=len(list(data_prep.task.unique())),
                    title='Quality analisis in PREP stage'
                    )
            fig_prep.savefig(path+'/QA/{database}/QA_S{i}_{database}_PREP.png'.format(database=database,i=i+1))
        except:
            print('la visita no existe'+visit)

data_wica=concat_df(save_path+'/*WICA.feather')
type='Components'
x='task'
fig_wica=graphics(data_wica,
         type,
         path,
         name_band=None,
         id='Session',
         id_cross=None,
         num_columns=4,
         save=False,
         plot=False,
         kind='box',
         palette=colors,
         hue=None,
         x=x,
         col_legend=len(list(data_wica.task.unique())),
         title='Quality analisis in wICA stage'
         )
fig_wica.savefig(path+'/QA/{database}/QA_{database}_WICA.png'.format(database=database))

data_reject=concat_df(save_path+'/*reject.feather')
import numpy as np
list_metrics=list(data_reject.Metric.unique())
for element in list_metrics:
    if element[0]=='i':
        data_reject.drop(data_reject[data_reject['Metric']==element].index,inplace=True)
data_reject.drop(data_reject[data_reject['Metric']=='f_spectrum_min'].index,inplace=True)
data_reject.drop(data_reject[data_reject['Metric']=='f_spectrum_max'].index,inplace=True)
type='Metric_Value'
x='Session'
sessions=list(data_reject.Session.unique())
for i,visit in enumerate(sessions):
        data=data_reject[data_reject['Session']==visit]
        fig_reject=graphics(data,
                type,
                path,
                name_band=None,
                id='Metric',
                id_cross=None,
                num_columns=4,
                save=False,
                plot=False,
                kind='box',
                palette=colors,
                hue='task',
                x=x,
                col_legend=len(list(data_reject.task.unique())),
                title='Quality analisis in the reject epochs stage'
                )
        fig_reject.savefig(path+'/QA/{database}/QA_S{i}_{database}_reject.png'.format(database=database,i=i+1))