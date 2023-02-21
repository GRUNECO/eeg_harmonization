import numpy as np
import pandas as pd


def negativeTest(model):
    positivos = []
    negativos = []
    for row in model:
        positivos.extend(x for x in row if float(x) >= 0)
        negativos.extend(x for x in row if float(x) < 0)
    print('negativos: ',len(negativos))

def delcol(data,m,b,bm,roi):
    for metric in m:
        for band in b:
            for r in roi:
                if metric != 'crossfreq':
                    data.drop([metric+'_'+r+'_'+band],axis=1,inplace=True)
                else:
                    for modul in bm:
                        data.drop([metric+'_'+r+'_'+modul+'_'+band],axis=1,inplace=True)
    return data

def createModel(path,drop,control=None,replace=None):
    data = pd.read_feather(path)
    if not replace == None:
        data = data.replace({replace:'V0'})
    data= data[data['visit']=='V0']
    data= data[data['group']==control]
    data = data.drop(drop, axis=1)
    model = np.array(data)
    return model,data.columns