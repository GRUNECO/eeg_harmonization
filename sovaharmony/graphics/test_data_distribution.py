from graphics_QA import distribution_graphics
import pandas as pd 
import os
import errno

path=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena' #Cambia dependieron de quien lo corra

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
for b in bands:
    for met in m:
        for f in filters:
            for id in ids:
                if id=='ROI':
                    data=data_roi[data_roi['Band']==b]
                elif id=='Component':
                    data=data_ic[data_ic['Band']==b]
                filter=f
                metric=met
                name_img='{path}/distribution/{id}/{filter}/{metric}'.format(id=id,path=path,filter=filter,metric=metric)
                try:
                    os.makedirs(name_img)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
                name_img='{name_img}/{band}_{metric}_{id}.png'.format(name_img=name_img,band=b,id=id,metric=metric)
                title='{metric} in {b} for each {id}'.format(metric=metric,b=b, id=id)
                distribution_graphics(data,name_img,title,id=id,metric=metric ,filter=filter)