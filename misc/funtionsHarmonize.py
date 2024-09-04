#@autor: Verónica Henao Isaza, Universidad de Antioquia
#@autor: Luisa María Zapata Saldarriaga, Universidad de Antioquia, luisazapatasaldarriaga@gmail.com

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def remove_columns_with_c10(df):
    '''
    Para la matriz ICA 54x10 no no se debe considerar el C10 porque no es neuronal
    pero en las etapas previas no se considero, para evitar que se armonize o 
    entre al modelo de ML se va a eliminar en este codigo de neuroHarmonze
    utilizando esta funcion que busca las columnas que contienen esta componente
    y las elimina del dataframe.
    '''
    columns_to_drop = [col for col in df.columns if 'C10' in col]
    df = df.drop(columns=columns_to_drop)
    return df


def covars(data):
    """
    Extract and store selected covariates from the input DataFrame.

    Parameters:
    - data (pd.DataFrame): Input DataFrame containing covariate information.

    Returns:
    - pd.DataFrame: The input DataFrame with specified columns dropped.
    - dict: Dictionary containing covariates extracted from the DataFrame.
    """
    # Create a dictionary to store selected covariates
    covars_dict = {
        'SITE': data['database'].to_numpy(),
        'gender': data['sex'].to_numpy(),
        'age': data['age'].to_numpy()
    }

    # Drop specified columns from the DataFrame
    columns_to_remove = ['participant_id', 'visit', 'condition', 'group', 'sex', 'age', 'MM_total', 'FAS_F', 'FAS_S', 'FAS_A', 'education']

    # Iterar sobre las columnas y eliminarlas si existen
    for column in columns_to_remove:
        if column in data.columns:
            data.drop(column, axis=1, inplace=True)
        else:
            print(f"La columna {column} no existe en el DataFrame.")

    # Return the modified DataFrame and the covariates dictionary
    return data, covars_dict

def covarsGen(data):
    """
    Extract selected covariates from the input DataFrame and drop specified columns.

    Parameters:
    - data (pd.DataFrame): Input DataFrame containing covariate information.

    Returns:
    - pd.DataFrame: The input DataFrame with specified columns dropped.
    - dict: Dictionary containing extracted covariates from the DataFrame.
    """
    # Create a dictionary to store selected covariates
    covars = {
        'SITE': data['database'].to_numpy(),
        'gender': data['sex'].to_numpy(),
        'age': data['age'].to_numpy(),
        'group': data['group'].to_numpy()
    }

    # Drop specified columns from the DataFrame
    data.drop(['participant_id', 'visit', 'condition', 'group', 'sex', 'age'], axis=1, inplace=True)
    data.drop(['MM_total', 'FAS_F', 'FAS_S', 'FAS_A', 'education'], axis=1, inplace=True)

    # Return the modified DataFrame and the covariates dictionary
    return data, covars


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
    """
    Count the number of negative values in a 2D list (model).

    Parameters:
    - model (list): 2D list containing numerical values.

    Returns:
    - int: The count of negative values.
    """
    positive_values = []
    negative_values = []
    for row in model:
        positive_values.extend(x for x in row if float(x) >= 0)
        negative_values.extend(x for x in row if float(x) < 0)
    print(f"Number of negative values: {len(negative_values)}")
    return len(negative_values)

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


def select(data,metric,OneBand=None,WithoutBand=None,Gamma=None,space='roi',spatial_matrix='54x10'):
    m = ['power','sl','cohfreq','entropy','crossfreq'] # Pongo las que voy a eliminar
    b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']  # Pongo las que voy a eliminar
    Beta = ['Beta1','Beta2','Beta3']
    Alpha = ['Alpha-1','Alpha-2']
    if space == 'roi':
        roi = ['F','C','T','PO']
    elif space == 'ic':
        if spatial_matrix=='54x10':
            roi = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
        if spatial_matrix=='58x25':
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

def add_Gamma(new_All,space,ica):
    if space == 'roi':
        s = ['F','C','T','PO']
        for roi in s:
            new_All['power_'+roi+'_Gamma']=1-(new_All['power_'+roi+'_Delta']+new_All['power_'+roi+'_Theta']+new_All['power_'+roi+'_Alpha-1']+new_All['power_'+roi+'_Alpha-2']+new_All['power_'+roi+'_Beta1']+new_All['power_'+roi+'_Beta2']+new_All['power_'+roi+'_Beta3'])
    elif space == 'ic':
        if ica == '54x10':
            s=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
        elif ica == '58x25':
            s=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]
        else:
            print('Error ICA')
        for ic in s:
            new_All['power_'+ic+'_Gamma']=1-(new_All['power_'+ic+'_Delta']+new_All['power_'+ic+'_Theta']+new_All['power_'+ic+'_Alpha-1']+new_All['power_'+ic+'_Alpha-2']+new_All['power_'+ic+'_Beta1']+new_All['power_'+ic+'_Beta2']+new_All['power_'+ic+'_Beta3'])
    return new_All

def return_col(data1,data2,fist=True):
    '''
    data1: 340 rows , 381 columns  : database [0,1] : group Nan
    if fist == True: data2: data2: 695 rows , 396 columns  : database {'BIOMARCADORES': 0.0, 'CHBMP': 1.0, 'DUQUE': 2.0, 'SRM': 3.0} : group {'Control': 0.0, 'DCL': 1.0, 'DTA': 2.0, 'G1': 3.0, 'G2': 4.0}
    data2: 340 rows , 381 columns  : database [0,1] : group ['Control', 'G1']
    '''
    ### REVISAR
    data1 = data1.reset_index(drop=True)
    data2 = data2.reset_index(drop=True)
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

def rename_cols(data1,data2,namegroup1,namegroup2):
    for l in range(len(data1['group'])):
        if data1['group'][l] == 0.0: #Controles
            data1['group'][l] = namegroup1
    for l in range(len(data1['group'])):
        if data1['group'][l] == 1.0: #Portadores
            data1['group'][l] = namegroup2

    try:
        for l in range(len(data1['database'])):
            if data1['database'][l] == 0.0: 
                data1['database'][l] = sorted(list(data2['database'].unique()))[0]
    except:
        pass
    try:
        for l in range(len(data1['database'])):
            if data1['database'][l] == 1.0: 
                data1['database'][l] = sorted(list(data2['database'].unique()))[1]
    except:
        pass
    try:
        for l in range(len(data1['database'])):
            if data1['database'][l] == 2.0: 
                data1['database'][l] = sorted(list(data2['database'].unique()))[2]
    except:
        pass
    try:
        for l in range(len(data1['database'])):
            if data1['database'][l] == 3.0:
                data1['database'][l] = sorted(list(data2['database'].unique()))[3]
    except:
        pass    

    return data1

def extract_components_interes(data_df, components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]):
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

def graf(path,columnasAll,noGene,Gene,noGene_ht,Gene_ht,nnoGene,nGene,nmy_dataAll,nmy_data_adjdataAll,title,space):
    for band in columnasAll:
        try: 
            sns.kdeplot(noGene[band], color='darkcyan', label='Control')
            sns.kdeplot(Gene[band], color='#708090', label='G1')
            sns.kdeplot(noGene_ht[band], color='darkcyan', linestyle='--')
            sns.kdeplot(Gene_ht[band], color='#708090', linestyle='--')
            #plt.title(f'# negatives - sovaharmony(-): {nnoGene,nGene} and neuroHarmonize(--): {nmy_dataAll,nmy_data_adjdataAll}')
            plt.title('Distribution of group effects')
            #plt.suptitle(title)
            #plt.legend()
            lines = plt.gca().get_lines()
            include = [0,1]
            legend1 = plt.legend([lines[i] for i in include],[lines[i].get_label() for i in include], loc=1)
            legend2 = plt.legend([lines[i] for i in [1,3]],['Before','After'], loc=2)
            plt.gca().add_artist(legend1)
            plt.xlabel(band.replace('-',''))
            #plt.show()
            s=band.split('_')[1]
            os.makedirs(r'{path}\{space}\{s}'.format(path=path,s=s,space=space), exist_ok=True)
            plt.savefig(r'{path}\{space}\{s}\{name}_{title}_density.png'.format(path=path,s=s,space=space,name=band,title=title))
            plt.close()
        except:
            pass

def graf_DB(path,columnasAll,B,D,S,C,BH,DH,SH,CH,title,space):
    for band in columnasAll:
        try: 
            sns.kdeplot(B[band], color='#127369', label='UdeA 1')
            sns.kdeplot(D[band], color='#10403B', label='UdeA 2')
            sns.kdeplot(S[band], color='#8AA6A3', label='SRM')
            sns.kdeplot(C[band], color='#45C4B0', label='CHBMP')
            sns.kdeplot(BH[band], color='#127369', linestyle='--')
            sns.kdeplot(DH[band], color='#10403B', linestyle='--')
            sns.kdeplot(SH[band], color='#8AA6A3', linestyle='--')
            sns.kdeplot(CH[band], color='#45C4B0', linestyle='--')
            #plt.title(f'# negatives - sovaharmony(-): {nnoGene,nGene} and neuroHarmonize(--): {nmy_dataAll,nmy_data_adjdataAll}')
            plt.title('Distribution of cohort effects')
            #plt.suptitle(title)
            #plt.legend()
            lines = plt.gca().get_lines()
            include = [0,1,2,3]
            legend1 = plt.legend([lines[i] for i in include],[lines[i].get_label() for i in include], loc=1)
            legend2 = plt.legend([lines[i] for i in [1,4]],['Before','After'], loc=2)
            plt.gca().add_artist(legend1)
            plt.xlabel(band.replace('-',''))
            #plt.show()
            s=band.split('_')[1]
            os.makedirs(r'{path}\{space}\{s}'.format(path=path,s=s,space=space), exist_ok=True)
            plt.savefig(r'{path}\{space}\{s}\{name}_{title}_BD_density.png'.format(path=path,s=s,space=space,name=band,title=title))
            plt.close()
        except:
            pass

def save_complete(new_name,data,dd,path_feather,group1,group2):
    data_eeg_dataAll = data.reset_index(drop=True) 
    data_eeg_dataAll = rename_cols(data_eeg_dataAll,dd,group1,group2)
    if not os.path.exists(path_feather):
        os.makedirs(path_feather)
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

def organizarDataFrame(new_dataAll,database_database,allm,dd,space,ica):
    new_dataAll['database'] = database_database
    new_dataAll = return_col(new_dataAll,dd,fist=False)
    if allm == 'power':
        new_dataAll = add_Gamma(new_dataAll,space,ica)
    return new_dataAll

    

def CTRG1(new_dataAll):
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

def CTRx(new_dataAll):
    #mapsDrop(data,filtGroup=None,visit1=None,visit2=None)
    dataCTR = mapsDrop(new_dataAll,0.0,'V0','t1') #CTR
    #dataCTR = dataCTR[(dataCTR['database'] == 3.0) | (dataCTR['database'] == 1.0)]
    #dataCTR['database']=dataCTR.database.replace([1.0,3.0],0.0) #Biomarcadores+SRM+CHBMP
    dataDTA = mapsDrop(new_dataAll,1.0,'V0') #DTA
    #dataDTA['database']=dataDTA.database.replace([0.0,2.0],1.0) #Biomarcadores
    datacol = pd.concat([dataCTR, dataDTA])
    return datacol