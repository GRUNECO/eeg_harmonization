'''Code used to filter the BIOMARCADORES database by components of the G1 and G2 groups.
They have the same number of visits and correspond to the same visits.
The ICC is calculated with these data '''

from tokenize import group
import numpy as np
import pandas as pd 
import collections
import scipy.io
import pingouin as pg

datos1=pd.read_feather(r"E:\Academico\Universidad\Posgrado\Tesis\Paquetes\eeg_harmonization\sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_components.feather") 
datos2=pd.read_feather(r"E:\Academico\Universidad\Posgrado\Tesis\Paquetes\eeg_harmonization\sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_norm_components.feather")
datos=pd.concat((datos1,datos2))#Original Data


datos=datos.drop(datos[datos['Session']=='V4P'].index)#Borrar datos
components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25']
datos=datos[datos.Components.isin(components) ] #Solo los datos de las componentes seleccionadas

sessions=datos['Session'].unique() #sesiones 
print(sessions)
Grupos=['G1','G2','CTR','DCL','DTA']
G=['G1','G2']

for i in G:
    g=datos[datos['Group']==i]
    visitas=g['Session'].unique()
    sujetos=g['Subject'].unique()
    print('Cantidad de sujetos de '+i+': ', len(sujetos))
    k=0
    for j in sujetos:
        s=g[g['Subject']==j]
        if (collections.Counter(s['Session'].unique()) == collections.Counter(visitas)):
            None
        else:
            k=k+1
            datos=datos.drop(datos[datos['Subject']==j].index)
            #print(j) #Sujeto sin todas 
            #print(s['Session'].unique())
    print('Sujetos a borrar:', k)
    print('Sujetos a analizar con todas las visitas: ',len(sujetos)-k)

#Verificación
G=['G1','G2']
for i in G:
    g=datos[datos['Group']==i]
    print('Cantidad de sujetos al filtrar '+ i+': ',len(g['Subject'].unique()))


#datos es el archivo filtrado de sujetos para g1 y g2
#son 8 componentes
#G1 #FILAS:152, #COLUMNAS: 4 
#G2 #FILAS:200, #COLUMNAS: 4 

visitas=['V0','V1','V2','V3','V4']
bandas=datos['Bands'].unique()
Stage=datos['Stage'].unique()

icc_value = pd.DataFrame(columns=['Description','ICC','F','df1','df2','pval','CI95%'])
for st in Stage:
    d_stage=datos[datos['Stage']==st] 
    for g in G:
        d_group=d_stage[d_stage['Group']==g]
        dic={}
        icc_comp=[]
        for comp in components:
            d_comp=d_group[d_group['Components']==comp]
            visits=list(d_comp['Session'].unique())
            matrix_c=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage']) #Se le asigna a un dataframe los datos d elas columnas
            subjects=d_comp['Subject'].unique() 
            for vis in visits:
                matrix_s=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage'])
                power=d_comp[d_comp['Session']==vis]['Powers'].tolist()
                n_vis=[vis]*len(power)
                matrix_s['Session']=n_vis
                matrix_s['Power']=power  
                matrix_s['Group']=d_comp[d_comp['Session']==vis]['Group'].tolist()
                matrix_s['Bands']=d_comp[d_comp['Session']==vis]['Bands'].tolist()
                matrix_s['Stage']=d_comp[d_comp['Session']==vis]['Stage'].tolist()

                matrix_c=matrix_c.append(matrix_s, ignore_index = True)            
            
            index=list(np.arange(0,len(subjects)*len(bandas),1))*len(visits)
            matrix_c['index']=index

        
            #print('\n Matriz componente '+g+' '+st+' ',comp)
            for i,ban in enumerate(bandas):
                fil_bands=matrix_c['Bands']==ban
                filter=matrix_c[fil_bands]
                icc=pg.intraclass_corr(data=filter, targets='index', raters='Session', ratings='Power').round(6)
                icc3 = icc[icc['Type']=='ICC3k']
                icc3 = icc3.set_index('Type')
               # print(filter['Stage'])
                icc3['Stage']=filter['Stage'][i]
                icc3['Group']=filter['Group'][i]
                icc3['Bands']=ban
                icc3['Components']=comp
                icc_value=icc_value.append(icc3,ignore_index=True)
        icc_value.append(icc_value)
    icc_value.append(icc_value)
icc_value.to_csv(r'E:\Academico\Universidad\Posgrado\Tesis\Paquetes\eeg_harmonization\sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_Components_G1-G2.csv',sep=';')
