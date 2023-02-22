import numpy as np
import pandas as pd


def mapsDrop(data):
    databases = {label:float(idx) for idx,label in enumerate(np.unique(data['database']))}
    print(databases)
    group = {label:float(idx) for idx,label in enumerate(np.unique(data['group']))}
    print(group)
    gender = {label:float(idx) for idx,label in enumerate(np.unique(data['sex']))}
    print(gender)

    data.loc[:,'group'] = data.loc[:,'group'].map(group)
    data.loc[:,'sex'] = data.loc[:,'sex'].map(gender)
    data = data[data['group'] == 0.0]
    database = data['database']
    data.loc[:,'database'] = data.loc[:,'database'].map(databases) 
    covars = {'SITE':data['database'].to_numpy(),
          'gender':data['sex'].to_numpy(),
          'age':data['age'].to_numpy()}
    data.drop(['participant_id','visit','condition','group','sex','age'],axis=1,inplace=True)
    data.drop(['MM_total','FAS_F','FAS_S','FAS_A','education'],axis=1,inplace=True)
    return data,covars


def negativeTest(model):
    positivos = []
    negativos = []
    for row in model:
        positivos.extend(x for x in row if float(x) >= 0)
        negativos.extend(x for x in row if float(x) < 0)
    return len(negativos)

def delcol(data,m,b,roi,bm=None):
    for metrici in m:
        for bandi in b:
            for ri in roi:
                if metrici != 'crossfreq':
                    data.drop([metrici+'_'+ri+'_'+bandi],axis=1,inplace=True)
                else:
                    for modul in bm:
                        data.drop([metrici+'_'+ri+'_'+modul+'_'+bandi],axis=1,inplace=True)
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


def select(data,metric,OneBand=None,WithoutBand=None):
    m = ['power','sl','cohfreq','entropy','crossfreq'] # Pongo las que voy a eliminar
    b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']  # Pongo las que voy a eliminar
    Beta = ['Beta1','Beta2','Beta3']
    Alpha = ['Alpha-1','Alpha-2']
    roi = ['F','C','T','PO']
    bm = ['Mdelta','Mtheta','Malpha-1','Malpha-2','Mbeta1','Mbeta2','Mbeta3','Mgamma']  # Pongo las que voy a eliminar
    if metric == 'All':
        if OneBand == None and WithoutBand == None:
            title = f'All_metrics_and_all_bands'
            return title,data
        elif OneBand == 'Beta' and WithoutBand == None:
            title = f'All_metrics_and_only_the_Beta_band'
            for beta in Beta:
                b.remove(beta)
            data = delcol(data,m,b,roi,bm)
            return title,data
        elif OneBand == 'Alpha' and WithoutBand == None:
            title = f'All_metrics_and_only_the_Alpha_band'
            for alpha in Alpha:
                b.remove(alpha)
            data = delcol(data,m,b,roi,bm)
            return title,data
        elif OneBand != None and WithoutBand == None:
            title = f'All_metrics_and_only_the_{OneBand}_band'
            b.remove(OneBand)
            data = delcol(data,m,b,roi,bm)
            return title,data
        elif OneBand == None and WithoutBand != None:
            title = f'All_metrics_and_without_the_{WithoutBand}_band'
            bp = [WithoutBand]
            roi = ['F','C','T','PO']
            bm = ['M'+WithoutBand[0]+WithoutBand[1:].swapcase()]  # Pongo las que voy a eliminar
            data = delcol(data,m,bp,roi,bm)
            return title,data
    elif metric != 'All':
        if OneBand == 'Beta' and WithoutBand == None:
            title = f'Only_{metric}_metric_and_only_the_{OneBand}_band'
            m.remove(metric)
            data = delcol(data,m,b,roi,bm)
            for beta in Beta:
                b.remove(beta)
            data = delcol(data,[metric],b,roi,bm)
            return title, data
        elif OneBand == 'Alpha' and WithoutBand == None:
            title = f'Only_{metric}_metric_and_only_the_{OneBand}_band'
            m.remove(metric)
            data = delcol(data,m,b,roi,bm)
            for alpha in Alpha:
                b.remove(alpha)
            data = delcol(data,[metric],b,roi,bm)
            return title, data
        elif OneBand == None and WithoutBand == None:
            title = f'Only_{metric}_metric'
            m.remove(metric)
            data = delcol(data,m,b,roi,bm)
            return title, data
        elif OneBand != None and WithoutBand == None:
            title = f'Only_{metric}_metric_and_only_the_{OneBand}_band'
            m.remove(metric)
            data = delcol(data,m,b,roi,bm)
            b.remove(OneBand)
            data = delcol(data,[metric],b,roi,bm)
            return title, data
        elif OneBand == None and WithoutBand != None:
            title = f'All_metrics_and_without_the_{WithoutBand}_band'
            bp = [WithoutBand]
            roi = ['F','C','T','PO']
            bmp = ['M'+WithoutBand[0]+WithoutBand[1:].swapcase()]  # Pongo las que voy a eliminar
            data = delcol(data,m,b,roi,bm)
            data = delcol(data,[metric],bp,roi,bmp)
            return title,data
    else:
        print('Error')


def renameDatabases(data):
    Biomarcadores = data[data['database'] == 0.0]
    Duque = data[data['database'] == 2.0]
    SRM = data[data['database'] == 3.0]
    CHBMP = data[data['database'] == 1.0]
    return Biomarcadores,Duque,SRM,CHBMP
def sumNegatives(Biomarcadores,Duque,SRM,CHBMP):
    nb=negativeTest(np.array(Biomarcadores))
    nd=negativeTest(np.array(Duque))
    ns=negativeTest(np.array(SRM))
    nc=negativeTest(np.array(CHBMP))
    n = nb+nd+ns+nc
    return n