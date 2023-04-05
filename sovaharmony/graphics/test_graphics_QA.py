import pandas as pd 
from graphics_QA import create_check
from graphics_QA import stats_pair
from graphics_QA import graphics
from graphics_QA import table_groups_DB
from sovaharmony.utils import concat_df
import matplotlib.pyplot as plt

path=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena' #Cambia dependieron de quien lo corra
save_path=r'D:\XIMENA\BIDS\Residentes\derivatives'.replace('\\','/')
#data loading
data_ic=pd.read_feather(r'{path}\data_long_features_roi.feather'.format(path=path))
bands=list(data_ic.Band.unique())
m = ['Coherence','Entropy','Power','SL']

colors=['#eac435', '#345995', '#e40066']
colors=['#89043D', '#2FE6DE', '#FF784F']
colors=["#FF0022","#31B86B","#2FE6DE"]
colors=['#eac000','#89043D',"#FF0000"]
colors=["#FF784F","#2FE6DE","#31B86B"]

for met in m:
    for band in bands:
        #graphics(data_ic,met,path,band,'IC',id_cross=None,num_columns=4,save=False,plot=True,kind='box',palette=colors,x='condition')
        #graphics(data_ic,met,path,band,'IC',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors,x='visit')
        graphics(data_ic,met,path,band,'ROI',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors,x='condition')
        #graphics(data_ic,met,path,band,'ROI',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors,x='visit')

# database='Residentes'
# data_prep=concat_df(save_path+'/*PREP.feather')
# type='Metric_value'
# x='State'
# sessions=list(data_prep.Session.unique())
# for i,visit in enumerate(sessions):
#         try:
#                 data=data_prep[data_prep['Session']==visit]
#                 fig_prep=graphics(data,
#                         type,
#                         path,
#                         name_band=None,
#                         id='Metric',
#                         id_cross=None,
#                         num_columns=3,
#                         save=False,
#                         plot=False,
#                         kind='violin',
#                         palette=colors,
#                         hue='task',
#                         x=x,
#                         col_legend=len(list(data_prep.task.unique()))
#                         )
#                 fig_prep.savefig(path+'/QA/QA_S{i}_{database}_PREP.png'.format(database=database,i=i+1))
#         except:
#                 print('la visita no existe'+visit)

# data_wica=concat_df(save_path+'/*WICA.feather')
# type='Components'
# x='task'
# fig_prep=graphics(data_wica,
#          type,
#          path,
#          name_band=None,
#          id='Session',
#          id_cross=None,
#          num_columns=4,
#          save=False,
#          plot=False,
#          kind='violin',
#          palette=colors,
#          hue=None,
#          x=x,
#          col_legend=len(list(data_wica.task.unique()))
#          )
# fig_prep.savefig(path+'/QA/QA_{database}_WICA.png'.format(database=database))

# data_reject=concat_df(save_path+'/*reject.feather')
# # import numpy as np
# # list_metrics=list(data_reject.Metric.unique())
# # for element in list_metrics:
# #     if element[0]=='i':
# #         data_reject.drop(data_reject[data_reject['Metric']==element].index,inplace=True)
# data_reject.drop(data_reject[data_reject['Metric']=='f_spectrum_min'].index,inplace=True)
# data_reject.drop(data_reject[data_reject['Metric']=='f_spectrum_max'].index,inplace=True)
# type='Metric_Value'
# x='Session'
# sessions=list(data_reject.Session.unique())
# for i,visit in enumerate(sessions):
#         data=data_reject[data_reject['Session']==visit]
#         fig_prep=graphics(data,
#                 type,
#                 path,
#                 name_band=None,
#                 id='Metric',
#                 id_cross=None,
#                 num_columns=4,
#                 save=False,
#                 plot=False,
#                 kind='violin',
#                 palette=colors,
#                 hue='task',
#                 x=x,
#                 col_legend=len(list(data_reject.task.unique()))
#                 )
#         fig_prep.savefig(path+'/QA/QA_S{i}_{database}_reject.png'.format(database=database,i=i+1))