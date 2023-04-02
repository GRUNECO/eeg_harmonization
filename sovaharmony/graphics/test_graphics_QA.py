import pandas as pd 
from graphics_QA import create_check
from graphics_QA import stats_pair
from graphics_QA import graphics
from graphics_QA import table_groups_DB

path=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena' #Cambia dependieron de quien lo corra

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
        #graphics(data_ic,met,path,band,'IC',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors,x='condition')
        #graphics(data_ic,met,path,band,'IC',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors,x='visit')
        graphics(data_ic,met,path,band,'ROI',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors,x='condition')
        graphics(data_ic,met,path,band,'ROI',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors,x='visit')
