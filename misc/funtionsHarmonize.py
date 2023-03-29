import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

def mapsDrop(data,filtGroup=None,visit1=None,visit2=None):
    #filter_dataset=filter_band[filter_band.Components.isin(components)]
    databases,group,gender = labels(data)

    data.loc[:,'group'] = data.loc[:,'group'].map(group)
    data.loc[:,'sex'] = data.loc[:,'sex'].map(gender)
    if filtGroup == None and visit1 == None and visit2 == None :
        pass
    else:
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
                        if modul == 'MGAMMA':
                            modul = modul[0]+modul[1:].swapcase()
                        else:
                            pass
                        try:
                            data.drop([metrici+'_'+ri+'_'+modul+'_'+bandi],axis=1,inplace=True)
                        except:
                            continue
    return data

def delcolumn(data,e,em=None):
    datadel = extract_components_interes(data.copy(),[e])
    if em != None:
        datadel = extract_components_interes(datadel,[em])
    datadel_col=datadel.columns
    data.drop(datadel_col,axis=1,inplace=True)
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

def add_Gamma(new_All,space):
    if space == 'roi':
        s = ['F','C','T','PO']
        for roi in s:
            new_All['power_'+roi+'_Gamma']=1-(new_All['power_'+roi+'_Delta']+new_All['power_'+roi+'_Theta']+new_All['power_'+roi+'_Alpha-1']+new_All['power_'+roi+'_Alpha-2']+new_All['power_'+roi+'_Beta1']+new_All['power_'+roi+'_Beta2']+new_All['power_'+roi+'_Beta3'])
    elif space == 'ic':
        s = ['C14','C15','C18','C20','C22','C23','C24','C25'] #ic
        for ic in s:
            new_All['power_'+ic+'_Gamma']=1-(new_All['power_'+ic+'_Delta']+new_All['power_'+ic+'_Theta']+new_All['power_'+ic+'_Alpha-1']+new_All['power_'+ic+'_Alpha-2']+new_All['power_'+ic+'_Beta1']+new_All['power_'+ic+'_Beta2']+new_All['power_'+ic+'_Beta3'])
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
    return data1

def rename_cols(data1,namebase1,namebase2,namegroup1,namegroup2):
    #rename_cols(data_eeg_dataAll,'CHBMP+SRM+BIOMARCADORES','BIOMARCADORES','Control','G1')
    for l in range(len(data1['group'])):
        if data1['group'][l] == 0.0: #Controles
            data1['group'][l] = namegroup1
    for l in range(len(data1['group'])):
        if data1['group'][l] == 4.0:
            data1['group'][l] = namegroup1
    for l in range(len(data1['group'])):
        if data1['group'][l] == 1.0: #Portadores
            data1['group'][l] = namegroup2
    for l in range(len(data1['group'])):
        if data1['group'][l] == 3.0: 
            data1['group'][l] = namegroup2
    for l in range(len(data1['database'])):
        if data1['database'][l] == 0.0: #Biomarcadores+SRM+CHBMP
            data1['database'][l] = namebase1
    for l in range(len(data1['database'])):
        if data1['database'][l] == 1.0: #Biomarcadores
            data1['database'][l] = namebase2
    return data1

def extract_components_interes(data_df, components):
    #components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]
    columns=data_df.columns

    comp_neural=[]
    for col in columns:
        for comp in components:
            if comp in col:
                comp_neural.append(col)
            
    difference_1 = set(columns).difference(set(comp_neural))
    difference_2 = set(comp_neural).difference(set(columns))

    list_difference = list(difference_1.union(difference_2))
    data_df.drop(list_difference,axis=1,inplace=True)
    return data_df

def graf(columnasAll,noGene,Gene,noGene_ht,Gene_ht,nnoGene,nGene,nmy_dataAll,nmy_data_adjdataAll,title):
    for band in columnasAll:
        sns.kdeplot(noGene[band], color='darkcyan', label='no Gene')
        sns.kdeplot(Gene[band], color='#708090', label='Gene')
        sns.kdeplot(noGene_ht[band], color='darkcyan', label='no Gene', linestyle='--')
        sns.kdeplot(Gene_ht[band], color='#708090', label='Gene', linestyle='--')
        plt.title(f'# negatives - sovaharmony(-): {nnoGene,nGene} and neuroHarmonize(--): {nmy_dataAll,nmy_data_adjdataAll}')
        plt.suptitle(title)
        plt.legend()
        plt.show()
        #plt.savefig(r'{path}\TransformadosG1G2\{name}_{title}_G1G2density.png'.format(path=path,name=band,title=title))
        plt.close()

# Debo importar LinearRegression para el calculo de las Ri
#https://profesordata.com/2020/08/22/metodos-de-seleccion-de-variables-el-factor-de-inflacion-de-la-varianza/
'''
Se dice que existe un grado de multicolinealidad si un conjunto de las características independientes 
puede ser calculado como combinación lineal del resto.
Y esto puede ser un problema y es que si se tiene un conjunto de datos que presenta multicolinealidad
tenemos el riesgo de que en el proceso de entrenamiento del modelo de Aprendizaje Automático Supervisado
se esté utilizando información «duplicada» y, debido a esta duplicidad en la información, los procesos 
de entrenamiento no pueden encontrar los parámetros adecuados para la correcta construcción de los 
modelos predictivos.
'''
from sklearn.linear_model import LinearRegression


def calculateVIF(var_predictoras_df):
    var_pred_labels = list(var_predictoras_df.columns)
    num_var_pred = len(var_pred_labels)
    
    lr_model = LinearRegression()
    
    result = pd.DataFrame(index = ['VIF'], columns = var_pred_labels)
    result = result.fillna(0)
    
    for ite in range(num_var_pred):
        x_features = var_pred_labels[:]
        y_feature = var_pred_labels[ite]
        x_features.remove(y_feature)
        
        x = var_predictoras_df[x_features]
        y = var_predictoras_df[y_feature]
        
        lr_model.fit(var_predictoras_df[x_features], var_predictoras_df[y_feature])
        
        result[y_feature] = 1/(1 - lr_model.score(var_predictoras_df[x_features], var_predictoras_df[y_feature]))
    
    return result

def selectDataUsingVIF(var_predictoras_df, max_VIF = 5):
    result = var_predictoras_df.copy(deep = True)
    
    VIF = calculateVIF(result)
    
    while VIF.values.max() > max_VIF:
        col_max = np.where(VIF == VIF.values.max())[1][0]
        features = list(result.columns)
        features.remove(features[col_max])
        result = result[features]
        
        VIF = calculateVIF(result)
        
    return result

def verificarVIF(x_pred):
    VIF_orig = calculateVIF(x_pred.copy(deep = True)).columns.to_list()
    VIF_less_th_5 = calculateVIF(selectDataUsingVIF(x_pred)).columns.to_list()

    return [feat for feat in VIF_orig if feat not in VIF_less_th_5]

def save_complete(new_name,data,path_feather,database1,database2,group1,group2):
    data_eeg_dataAll = data.reset_index(drop=True) 
    data_eeg_dataAll = rename_cols(data_eeg_dataAll,database1,database2,group1,group2)
    data_eeg_dataAll.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_feather,name=new_name))

def G1G2(new_dataAll,dd=None,database_database=None,database=False):
    data = new_dataAll.copy()
    if database is False:
       pass
    else:
        data['database'] = database_database
        data = return_col(data,dd,fist=False)
    dataG1 = mapsDrop(data,1.0,'V0') #Portadores
    dataG2 = mapsDrop(data,2.0,'V0') #No portadores
    datacol = pd.concat([dataG2, dataG1])
    datacol['group'] = datacol.group.replace(2,0)
    datacol['database'] = datacol.database.replace(2,1)
    return datacol

def organizarDataFrame(new_dataAll,database_database,allm,dd,space):
    new_dataAll['database'] = database_database
    new_dataAll = return_col(new_dataAll,dd,fist=False)
    if allm == 'power':
        new_dataAll = add_Gamma(new_dataAll,space)
    new_dataAll = filter_visit_group(new_dataAll)
    return new_dataAll

    

def filter_visit_group(new_dataAll):
    dataCTR = mapsDrop(new_dataAll,0.0,'V0','t1')
    dataCTR = dataCTR[(dataCTR['database'] == 3.0) | (dataCTR['database'] == 1.0)]
    dataCTR['database']=dataCTR.database.replace([1.0,3.0],0.0) #Biomarcadores+SRM+CHBMP
    dataG1 = mapsDrop(new_dataAll,1.0,'V0') #Portadores
    dataG1['database']=dataG1.database.replace([0.0,2.0],1.0) #Biomarcadores
    dataG2 = mapsDrop(new_dataAll,2.0,'V0') #No portadores
    dataG2['database']=dataG2.database.replace([0.0,2.0],0.0) #Biomarcadores+SRM+CHBMP
    dataG2['group']=dataG2.database.replace([2.0],0.0) #Controles
    dataCTRG2 = pd.concat([dataCTR, dataG2])
    datacol = pd.concat([dataCTRG2, dataG1])
    return datacol

def filter_visit_DTA(new_dataAll):
    #mapsDrop(data,filtGroup=None,visit1=None,visit2=None)
    dataCTR = mapsDrop(new_dataAll,0.0,'V0','t1')
    dataCTR = dataCTR[(dataCTR['database'] == 3.0) | (dataCTR['database'] == 1.0)]
    dataCTR['database']=dataCTR.database.replace([1.0,3.0],0.0) #Biomarcadores+SRM+CHBMP
    dataDTA = mapsDrop(new_dataAll,1.0,'V0') #Portadores
    dataDTA['database']=dataDTA.database.replace([0.0,2.0],1.0) #Biomarcadores
    dataG2 = mapsDrop(new_dataAll,2.0,'V0') #No portadores
    dataG2['database']=dataG2.database.replace([0.0,2.0],0.0) #Biomarcadores+SRM+CHBMP
    dataG2['group']=dataG2.database.replace([2.0],0.0) #Controles
    dataCTRG2 = pd.concat([dataCTR, dataG2])
    datacol = pd.concat([dataCTRG2, dataDTA])
    return datacol

def filter_visit_DCL(new_dataAll):
    dataCTR = mapsDrop(new_dataAll,0.0,'V0','t1')
    dataCTR = dataCTR[(dataCTR['database'] == 3.0) | (dataCTR['database'] == 1.0)]
    dataCTR['database']=dataCTR.database.replace([1.0,3.0],0.0) #Biomarcadores+SRM+CHBMP
    dataG1 = mapsDrop(new_dataAll,1.0,'V0') #Portadores
    dataG1['database']=dataG1.database.replace([0.0,2.0],1.0) #Biomarcadores
    dataG2 = mapsDrop(new_dataAll,2.0,'V0') #No portadores
    dataG2['database']=dataG2.database.replace([0.0,2.0],0.0) #Biomarcadores+SRM+CHBMP
    dataG2['group']=dataG2.database.replace([2.0],0.0) #Controles
    dataCTRG2 = pd.concat([dataCTR, dataG2])
    datacol = pd.concat([dataCTRG2, dataG1])
    return datacol