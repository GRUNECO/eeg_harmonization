import numpy as np
import pandas as pd

def covars(data):
    covars = {'SITE':data['database'].to_numpy(),
        'gender':data['sex'].to_numpy(),
        'age':data['age'].to_numpy()}
    data.drop(['participant_id','visit','condition','group','sex','age'],axis=1,inplace=True)
    data.drop(['MM_total','FAS_F','FAS_S','FAS_A','education'],axis=1,inplace=True)
    return data,covars

def labels(data):
    databases = {label:float(idx) for idx,label in enumerate(np.unique(data['database']))}
    print(databases)
    group = {label:float(idx) for idx,label in enumerate(np.unique(data['group']))}
    print(group)
    gender = {label:float(idx) for idx,label in enumerate(np.unique(data['sex']))}
    print(gender)
    return databases,group,gender

def mapsDrop(data,filtGroup,visit1,visit2=None):
    databases,group,gender = labels(data)

    data.loc[:,'group'] = data.loc[:,'group'].map(group)
    data.loc[:,'sex'] = data.loc[:,'sex'].map(gender)
    data = data[data['group'] == filtGroup]
    data = data[(data['visit'] == visit1) | (data['visit'] == visit2)]
    data.loc[:,'database'] = data.loc[:,'database'].map(databases) 
    return data


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


def select(data,metric,OneBand=None,WithoutBand=None,Gamma=None,space='roi'):
    m = ['power','sl','cohfreq','entropy','crossfreq'] # Pongo las que voy a eliminar
    b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']  # Pongo las que voy a eliminar
    Beta = ['Beta1','Beta2','Beta3']
    Alpha = ['Alpha-1','Alpha-2']
    if space == 'roi':
        roi = ['F','C','T','PO']
    elif space == 'ic':
        roi = ['C14','C15','C18','C20','C22','C23','C24','C25'] #ic
    bm = ['Mdelta','Mtheta','Malpha-1','Malpha-2','Mbeta1','Mbeta2','Mbeta3','Mgamma']  # Pongo las que voy a eliminar
    if metric == 'All':
        if OneBand == None and WithoutBand == None:
            if Gamma != None:
                title = f'All_metrics_and_without_the_{WithoutBand}_band_OnlyPower'
                data = delcol(data,['power'],['Gamma'],roi,bm)
                return title, data
            else:
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
            #bm = ['M'+WithoutBand[0]+WithoutBand[1:].swapcase()]  # Pongo las que voy a eliminar
            bm = ['M'+WithoutBand[0].swapcase()+WithoutBand[1:]]
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

def renameModel(data):
    noGene = data[data['database'] == 0.0]
    Gene = data[data['database'] == 1.0]
    return noGene,Gene

def sumNegatives(Biomarcadores,Duque,SRM,CHBMP):
    nb=negativeTest(np.array(Biomarcadores))
    nd=negativeTest(np.array(Duque))
    ns=negativeTest(np.array(SRM))
    nc=negativeTest(np.array(CHBMP))
    n = nb+nd+ns+nc
    return n

def descrive(data,new_data):
    df = pd.DataFrame()
    dz = []
    negd = []
    ndz = []
    negnd = []
    df['Std_sovaharmony'] = np.std(data)
    df['Var_sovaharmony'] = np.var(data)
    df['Mean_sovaharmony'] = np.mean(data)
    df['Max_sovaharmony'] = np.max(data)
    df['Min_sovaharmony'] = np.min(data)
    df['Std_neuroHarmonize'] = np.std(new_data)
    df['Var_neuroHarmonize'] = np.var(new_data)
    df['Mean_neuroHarmonize'] = np.mean(new_data)
    df['Max_neuroHarmonize'] = np.max(new_data)
    df['Min_neuroHarmonize'] = np.min(new_data)
    for d in data:
        for v in data[d]:
            if v <= 0.005 and v >= 0.00:
                dz.append(v)
            if v < 0:
                negd.append(v)
    for nd in data:
        for nv in new_data[nd]:
            if nv <= 0.005 and nv >= 0.00:
                ndz.append(nv)
            if nv < 0:
                negnd.append(nv)
    df['Values_close_to_zero_sovaharmony'] = len(dz)
    df['Values_close_to_zero_neuroHarmonize'] = len(ndz)
    df['Negative_sovaharmony'] = len(negd)
    df['Negative__neuroHarmonize'] = len(negnd)
    df_stats = df.reset_index()
                
    return df_stats

def to_save_df(new_data,df):
    df = df.append(new_data, ignore_index=False)
    #df = df.reset_index()
                
    return df

def add_Gamma(new_All,space='roi'):
    if space == 'roi':
        s = ['F','C','T','PO']
    elif space == 'ic':
        s = ['C14','C15','C18','C20','C22','C23','C24','C25'] #ic
    for roi in s:
        new_All['power_'+roi+'_Gamma']=1-(new_All['power_'+roi+'_Delta']+new_All['power_'+roi+'_Theta']+new_All['power_'+roi+'_Alpha-1']+new_All['power_'+roi+'_Alpha-2']+new_All['power_'+roi+'_Beta1']+new_All['power_'+roi+'_Beta2']+new_All['power_'+roi+'_Beta3'])
    return new_All

def return_col(data1,data2,fist=True):
    '''
    data1: 340 rows , 381 columns  : database [0,1] : group Nan
    if fist == True: data2: data2: 695 rows , 396 columns  : database {'BIOMARCADORES': 0.0, 'CHBMP': 1.0, 'DUQUE': 2.0, 'SRM': 3.0} : group {'Control': 0.0, 'DCL': 1.0, 'DTA': 2.0, 'G1': 3.0, 'G2': 4.0}
    data2: 340 rows , 381 columns  : database [0,1] : group ['Control', 'G1']
    '''
    if fist == True:
        databases = {label:float(idx) for idx,label in enumerate(np.unique(data2['database']))}
        print(databases)
        group = {label:float(idx) for idx,label in enumerate(np.unique(data2['group']))}
        print(group)
        gender = {label:float(idx) for idx,label in enumerate(np.unique(data2['sex']))}
        print(gender)
        data2.loc[:,'group'] = data2.loc[:,'group'].map(group)
        data2.loc[:,'sex'] = data2.loc[:,'sex'].map(gender)
        data2.loc[:,'database'] = data2.loc[:,'database'].map(databases) 
    else:
        pass
    cols = ['participant_id','visit','condition','group','sex','age','MM_total','FAS_F','FAS_S','FAS_A','education']
    participant_id = []
    visit = []
    condition = []
    group = []
    sex = []
    age = []
    MM_total = []
    FAS_F = []
    FAS_S = []
    FAS_A = []
    education = []
    cont=1
    for f in range(data2.shape[0]):
        try:
            id1 = data1[data1.index == f].index[0]
            id2 = data2[data2.index == f].index[0]
            if id1 == id2:
                for c in cols:
                    if c == 'participant_id':
                        participant_id.append(data2.iloc[f][c])
                    elif c == 'visit':
                        visit.append(data2.iloc[f][c])
                    elif c == 'condition':
                       condition.append(data2.iloc[f][c])
                    elif c == 'group':
                       group.append(data2.iloc[f][c])
                    elif c == 'sex':
                       sex.append(data2.iloc[f][c])
                    elif c == 'age':
                       age.append(data2.iloc[f][c])
                    elif c == 'MM_total':
                       MM_total.append(data2.iloc[f][c])
                    elif c == 'FAS_F':
                       FAS_F.append(data2.iloc[f][c])
                    elif c == 'FAS_S':
                       FAS_S.append(data2.iloc[f][c])
                    elif c == 'FAS_A':
                       FAS_A.append(data2.iloc[f][c])
                    elif c == 'education':
                       education.append(data2.iloc[f][c])
            else:
                pass
        except:
            cont += 1
            continue
    print(cont)
    data1['participant_id'] = np.array(participant_id)
    data1['visit'] = np.array(visit)
    data1['condition'] = np.array(condition)
    data1['group'] = np.array(group)
    data1['sex'] = np.array(sex)
    data1['age'] = np.array(age)
    data1['MM_total'] = np.array(MM_total)
    data1['FAS_F'] = np.array(FAS_F)
    data1['FAS_S'] = np.array(FAS_S)
    data1['FAS_A'] = np.array(FAS_A)
    data1['education'] = np.array(education)
    data1 = data1.reset_index(drop=True) 
    for l in range(len(data1['group'])):
        if data1['group'][l] == 0.0:
            data1['group'][l] = 'Control'
    for l in range(len(data1['group'])):
        if data1['group'][l] == 4.0:
            data1['group'][l] = 'Control'
    for l in range(len(data1['group'])):
        if data1['group'][l] == 1.0:
            data1['group'][l] = 'G1'
    for l in range(len(data1['group'])):
        if data1['group'][l] == 3.0:
            data1['group'][l] = 'G1'
    for l in range(len(data1['database'])):
        if data1['database'][l] == 0.0:
            data1['database'][l] = 'CHBMP+SRM+BIOMARCADORES'
    for l in range(len(data1['database'])):
        if data1['database'][l] == 1.0:
            data1['database'][l] = 'BIOMARCADORES'


    return data1