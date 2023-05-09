from graphics_QA import graphics
import pandas as pd 

path=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena' #Cambia dependieron de quien lo corra

#data loading
data_ic=pd.read_feather(r'{path}\data_long_features_ic.feather'.format(path=path))
data_roi=pd.read_feather(r'{path}\data_long_features_roi.feather'.format(path=path))
# graphics connectivity and power in IC and ROI

m = ['Coherence','Entropy','Power','SL']
bands=list(data_roi.Band.unique())
filters=['visit', 'condition']

for met in m:
    for band in bands:
        for f in filters:
            graphics(data_ic,met,path,band,'IC',id_cross=None,num_columns=4,save=False,plot=False,kind='box',palette=colors,x=f)
            graphics(data_roi,met,path,band,'ROI',id_cross=None,num_columns=2,save=True,plot=False,kind='box',palette=colors,x=f)
