"""
@autor: Valeria Cadavid Castro, Universidad de Antioquia, 
@autor: Verónica Henao Isaza, Universidad de Antioquia, 
@autor: Luisa María Zapata Saldarriaga, Universidad de Antioquia, luisazapatasaldarriaga@gmail.com

"""

import numpy as np
import json
import pandas as pd
import warnings
import collections
import seaborn as sns
import matplotlib.pyplot as plt
import os
import errno
import glob 
def load_txt(file):
  '''
  Function that reads txt files

  Parameters
  ----------
    file: extend .txt 

  Returns
  -------
    data: 
      Contains the information that was stored in the txt file
  '''
  with open(file, 'r') as f:
    data=json.load(f)
  return data

def load_feather(path):
    '''
    Function to upload files with feather format

    Parameters
    ----------
        path:str
            Directory where the file with the extension .feather

    Returns 
    -------
        data: dataframe
            Data in dataframe format
    '''
    data=pd.read_feather(os.path.join(path).replace("\\","/"))
    return data

def concat_df(path):
    path_df=glob.glob(path)
    data=[]
    for df in path_df:
        d=load_feather(df)
        
        data.append(d)
    data_concat=pd.concat((data))
    return data_concat

def _verify_epochs_axes(epochs_spaces_times,spaces_times_epochs,max_epochs=None):
    """
    """
    epochs,spaces,times = epochs_spaces_times.shape
    if max_epochs is None:
        max_epochs = epochs
    for e in range(np.max([epochs,max_epochs])):
        for c in range(spaces):
            assert np.all(epochs_spaces_times[e,c,:] == spaces_times_epochs[c,:,e])
    return True

def _verify_epoch_continuous(data,spaces_times,data_axes,max_epochs=None):
    epochs_idx = data_axes.index('epochs')
    spaces_idx = data_axes.index('spaces')
    times_idx = data_axes.index('times')
    epochs,spaces,times = data.shape[epochs_idx],data.shape[spaces_idx],data.shape[times_idx]
    if not epochs_idx in [0,2]:
        raise ValueError('Axes should be either epochs,spaces,times or spaces,times,epochs')
    if max_epochs is None:
        max_epochs = epochs
    for e in range(np.max([epochs,max_epochs])):
        for c in range(spaces):
            if epochs_idx==0:
                assert np.all(data[e,c,:] == spaces_times[c,e*times:(e+1)*times])
            elif epochs_idx==2:
                assert np.all(data[c,:,e] == spaces_times[c,e*times:(e+1)*times])
    return True



"Functions to save dataframes for graphics"

def dataframe_long_sensors(data,type,columns,name,path,roi=False,norm=False):
    '''Function used to convert a dataframe to be used for graphing by ROIs'''
    #demographic data and neuropsychological test columns
    #data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database']
    if roi:
        columns_df=data_dem+[type, 'Band', 'ROI']
    else:
        columns_df=data_dem+[type, 'Band', 'Sensors']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands
    bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
    #ROIs 
    if roi:
        spaces=['F', 'C','PO', 'T']
    else:
        spaces=['FP1','FP2','C3','C4','P7','P8','O2','O1']
    
    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                band=j
        for space in spaces:
            if space in i:
                if roi:
                    d_sep['ROI']=[space]*len(d_sep)
                else:
                     d_sep['Sensors']=[space]*len(d_sep)
                try:
                    if band: 
                        d_sep['Band']=[band]*len(d_sep)
                except:
                    pass
                d_sep= d_sep.rename(columns={i:type})
                data_new=pd.concat((data_new,d_sep),ignore_index = True)
               
    if roi:
        try:
            path="{input_path}\data_long\ROI".format(input_path=path).replace('\\','/')
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        data_new.reset_index(drop=True).to_feather('{path}\data_long_{task}_{metric}_{name}_{norm}_roi.feather'.format(path=path,name=data['database'].unique()[0],task=data_new['condition'].unique()[0],metric=type,norm=norm))
    else:
        try:
            path="{input_path}\data_long\SENSORS".format(input_path=path).replace('\\','/')
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        data_new.reset_index(drop=True).to_feather('{path}\data_long_{task}_{metric}_{name}_{norm}_sensors.feather'.format(path=path,name=data['database'].unique()[0],task=data_new['condition'].unique()[0],metric=type,norm=norm))
    print('Dataframe para graficos de {type} guardado: {name}'.format(type=type,name=name))

def dataframe_long_components(data,type,columns,name,path,spatial_matrix='54x10',norm=False):
    '''Function used to convert a wide dataframe into a long one to be used for graphing by IC'''
    #demographic data and neuropsychological test columns
    #data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database']
    columns_df=data_dem+[type, 'Band', 'Component']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands
    bandas=['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
    fit_params=["Intercept", "Slope","R^2","std(osc)"]
    #Components
    if spatial_matrix=='58x25':
        componentes =['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
    elif spatial_matrix=='54x10':
        componentes =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
    elif spatial_matrix=='cresta' or spatial_matrix=='openBCI' or spatial_matrix=='paper':
        componentes =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    
    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                
                band=j
        for params in fit_params:
            if params in i:
                fparams=params
        for c in componentes:
            if c in i:
                componente=c
                d_sep['Component']=[componente]*len(d_sep)
                try:
                    if band: 
                        d_sep['Band']=[band]*len(d_sep)
                except:
                    pass
                
                try:
                    if fparams:
                        d_sep['Fit_params']=[fparams]*len(d_sep)
                except:
                    pass

                d_sep= d_sep.rename(columns={i:type})
                data_new=pd.concat((data_new,d_sep),ignore_index = True)
        #data_new=data_new.append(d_sep,ignore_index = True) #Uno el dataframe 
    try:
        path="{input_path}\data_long\IC".format(input_path=path).replace('\\','/')
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    print(data_new['Band'].isnull().sum())
    if data_new['Band'].isnull().sum()!=0 or data_new['Band'].isna().sum()!=0:
        data_new.drop(['Band'],axis=1,inplace=True)
        type='ape_fit_params'
    data_new.reset_index(drop=True).to_feather('{path}\data_{task}_{metric}_long_{name}_{spatial_matrix}_{norm}_components.feather'.format(path=path,name=data_new['database'].unique()[0],task=data_new['condition'].unique()[0],metric=type,spatial_matrix=spatial_matrix,norm=norm).replace('\\','/'))
    print('Dataframe para graficos de {type} guardado: {name}'.format(type=type,name=name))

def dataframe_long_cross_roi(data,type,columns,name,path):
    '''Function used to convert a dataframe to be used for graphing by ROIs'''
    #demographic data and neuropsychological test columns
    #data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database']
    columns_df=data_dem+[type, 'Band', 'ROI']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands 
    bandas=['_Delta','_Theta','_Alpha-1','_Alpha-2','_Beta1','_Beta2','_Beta3','_Gamma']
    m_bandas=['Mdelta','Mtheta','Malpha-1','Malpha-2','Mbeta1','Mbeta2','Mbeta3','Mgamma']
    #ROIs 
    roi=['F', 'C','PO', 'T_']
    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                band=j
        for m in m_bandas:
            if m in i:
                bandm=m
        for c in roi:
            if c in i:
                r=c
        d_sep['Band']=[band]*len(d_sep)
        d_sep['ROI']=[r]*len(d_sep)
        d_sep['M_Band']=[bandm]*len(d_sep)
        d_sep= d_sep.rename(columns={i:type})
        data_new=data_new.append(d_sep,ignore_index = True) #Uno el dataframe 
    data_new['ROI']=data_new['ROI'].replace({'T_':'T'}, regex=True)#Quito el _ y lo reemplazo con '' 
    data_new['Band']=data_new['Band'].replace({'_':''}, regex=True)#Quito el _ y lo reemplazo con ''
    try:
        path="{input_path}\data_long\ROI".format(input_path=path).replace('\\','/')
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    data_new.reset_index(drop=True).to_feather('{path}\data_{name}_{task}_long_{metric}_ROI.feather'.format(path=path,name=data['database'].unique()[0],task=data_new['condition'].unique()[0],metric=type))
    print('Dataframe para graficos de {type} guardado: {name}'.format(type=type,name=name))

def dataframe_long_cross_ic(data,type='Cross Frequency',columns=None,name=None,path=None,spatial_matrix='54x10'):
    '''Function used to convert a dataframe to be used for graphing.'''
    #demographic data and neuropsychological test columns
    #data_dem=['participant_id', 'visit', 'group', 'condition', 'database','age', 'sex', 'education', 'MM_total', 'FAS_F', 'FAS_A', 'FAS_S']
    data_dem=['participant_id', 'visit', 'group', 'condition', 'database']
    columns_df=data_dem+[type, 'Band','M_Band', 'Component']
    data_new=pd.DataFrame(columns=columns_df)
    #Frequency bands
    bandas=['_Delta','_Theta','_Alpha-1','_Alpha-2','_Beta1','_Beta2','_Beta3','_Gamma']
    m_bandas=['Mdelta','Mtheta','Malpha-1','Malpha-2','Mbeta1','Mbeta2','Mbeta3','Mgamma']
    if spatial_matrix=='58x25':
        componentes =['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
    elif spatial_matrix=='54x10':
        componentes =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']
    elif spatial_matrix=='cresta' or spatial_matrix=='openBCI' or spatial_matrix=='paper':
        componentes =['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    for i in columns:
        '''The column of interest is taken with its respective demographic data and added to the new dataframe'''
        data_x=data_dem.copy()
        data_x.append(i)
        d_sep=data.loc[:,data_x] 
        for j in bandas:
            if j in i:
                band=j 
        for m in m_bandas:
            if m in i:
                bandm=m
        for c in componentes:
            if c in i:
                componente=c

        d_sep['Band']=[band]*len(d_sep)
        d_sep['M_Band']=[bandm]*len(d_sep)
        d_sep['Component']=[componente]*len(d_sep)
        d_sep= d_sep.rename(columns={i:type})
        data_new=data_new._append(d_sep,ignore_index = True) #Uno el dataframe 
    data_new['Band']=data_new['Band'].replace({'_':''}, regex=True)#Quito el _ y lo reemplazo con ''
    try:
        path="{input_path}\data_long\IC".format(input_path=path).replace('\\','/')
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    data_new.reset_index(drop=True).to_feather('{path}\data_{task}_{metric}_long_{name}_{spatial_matrix}_components.feather'.format(path=path,name=data_new['database'].unique()[0],task=data_new['condition'].unique()[0],metric=type,spatial_matrix=spatial_matrix).replace('\\','/'))
    print('Dataframe para graficos de {type} guardado: {name}'.format(type=type,name=name))

def dataframe_componentes_deseadas(data,columnas):
    """Function that returns a dataframe with the desired columns, only having data with the independent components of interest
    columnas=list of columns to be retained
    """
    columnas_deseadas=[*columnas,'C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25'] #columns of interest
    col_completas=list(data.columns)
    columnas=[]
    for i in range(len(columnas_deseadas)):
        for j in range(len(col_completas)):
            if columnas_deseadas[i] in col_completas[j]:
                columnas.append(col_completas[j])
    data_new=data.loc[:,columnas] #Dataframe with columns of interest
    return data_new


def removing_outliers(data,columns):
    '''
    Function used to return a dataframe without outliers, where it is verified that no more than 5$%$ of the data is lost per database.
    '''
    data['index'] = data.index #It was necessary to create a column labeled "index" to take the indexes in an easy way
    data_copy=data.copy()
    databases=data['database'].unique()
    for db in databases:
        datos_db=data[data['database']==db] 
        indices_db=[]
        for com in columns:
            Q1 = np.percentile(datos_db[com], 25, interpolation = 'midpoint')
            Q3 = np.percentile(datos_db[com], 75,interpolation = 'midpoint')
            IQR = Q3 - Q1 
            dataupper=datos_db[datos_db[com] >= (Q3+1.5*IQR)]#Valores atipicos superiores
            if dataupper.empty:
                upper=[]
            else:
                upper=dataupper.index.tolist() #lista de indices del dataframe que son valores atipicos
            datalower=datos_db[datos_db[com] <= (Q1-1.5*IQR)]#Valores atipicos inferiores
            if datalower.empty:
                lower=[]
            else:
                lower=datalower.index.tolist()#lista de indices del dataframe que son valores atipicos
            indices=upper+lower #union de upper y lower de indices del dataframe que son valores atipicos
            indices_db.extend(indices) #Se tiene una lista de indices por cada base de datos
    
        repeticiones=collections.Counter(indices_db) #Diccionario que contiene cuantas veces un indice(sujeto) tiene un dato atipico, en una banda de una componente
        bandera=True
        
        i=2
        while(bandera):#Mientras no se encuentre el porcentaje de perdida requerido
            i+=1 #se aumenta cada que se entra al while
            data_prueba=data.copy()#  copia de data frame para no borrar datos del dataframe original,se crea cada que se entra al while
            index_to_delete=list(dict(filter(lambda x: x[1] > i, repeticiones.items())).keys()) # se crea una lista de los indices cuyas repeticiones de datos atipicos es mayor a i
            data_prueba.drop(index_to_delete, inplace = True)#Se borran los indices del dataframe de prueba para saber el porcentaje de datos borrados
            porcentaje=100-data_prueba[data_prueba['database']==db].shape[0]*100/data[data['database']==db].shape[0]#porcentaje de datos borrados
            if porcentaje<=5:
                #Si el procentaje borrado por primera vez es menor o igual a 5, se borra del dataframe copia los indices que dan el resultado deseado
                data_copy.drop(index_to_delete, inplace = True)
                bandera=False #se cambia la bandera para que no entre mas al while
                #print(porcentaje)
    data_copy=data_copy.drop(columns='index')
    #Para observar un resumen de los datos antes y despues de eliminar sujetos con mayor cantidad de datos atipicos
    for db in databases:
        print('\nBase de datos '+db)
        print('Original')
        print(data[data['database']==db].shape)
        print('Despues de eliminar datos atipicos')
        print(data_copy[data_copy['database']==db].shape)
        print('Porcentaje que se elimino %',100-data_copy[data_copy['database']==db].shape[0]*100/data[data['database']==db].shape[0])
    data_copy=data_copy.reset_index(drop=True)
    return data_copy

#Amount of empty data from demographic data after merging with powers
def ver_datos_vacios(d_B):
    df=pd.DataFrame()
    databases=d_B['database'].unique()
    for i in databases:
        dx=d_B[d_B['database']==i][['age', 'sex', 'education', 'MM_total', 'FAS_F','FAS_S','FAS_A']].isnull().sum()
        df[i]=dx
        print('\n', i)
        print('Numero de sujetos:',len(d_B[d_B['database']==i]['participant_id'].unique()))
        print('Numero de datos:',len(d_B[d_B['database']==i]))
    print('\nCantidad de datos vacios')
    print(df)
    return None

def estadisticos_demograficos(data,name,path):
    """
    Function that exports tables of general description of age, gender and sex of the data.

    link de ayuda
    https://pandas.pydata.org/docs/user_guide/indexing.html
    https://kanoki.org/2022/07/25/pandas-select-slice-rows-columns-multiindex-dataframe/

    """
    
    # import dataframe_image as dfi
    # datos_estadisticos=data.groupby(['group']).describe(include='all')
    # table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
    # dfi.export(table,'{path}\Tablas_datos\Tabla_edad_escolaridad_sexo_todasBD_{name}.png'.format(path=path,name=name))
    # #Por cada base de datos
    # datos_estadisticos=data.groupby(['database','group']).describe(include='all')
    # table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
    # dfi.export(table, '{path}\Tablas_datos\Tabla_edad_escolaridad_sexo_separadoBD_{name}.png'.format(path=path,name=name))
    writer = pd.ExcelWriter('{path}\Tablas_datos\Tabla_edad_escolaridad_sexo_{name}.xlsx'.format(path=path,name=name))
    datos_estadisticos=data.groupby(['group']).describe(include='all')
    table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
    table.to_excel(writer,startrow=0)
    #Por cada base de datos
    datos_estadisticos=data.groupby(['database','group']).describe(include='all')
    table=datos_estadisticos.loc[:,[('age','count'),('age','mean'),('age','std'),('education','count'),('education','mean'),('education','std'),('sex','count'),('sex','top'),('sex','freq')]]
    table.to_excel(writer,startrow=11)
    writer.save()
    writer.close()   


'''manejo de pandas: https://joserzapata.github.io/courses/python-ciencia-datos/pandas/'''

