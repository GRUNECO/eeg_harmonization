'''Code used to filter the BIOMARCADORES database by components of the G2 and CTR groups.
They have the same number of visits but do not correspond to the same visits.
The ICC is calculated with these data '''

import numpy as np
import pandas as pd 
import collections
import scipy.io
from tokenize import group
import pingouin as pg

datos1=pd.read_feather(r"sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_components.feather") 
datos2=pd.read_feather(r"sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_norm_components.feather")
datos=pd.concat((datos1, datos2))#Original Data
print(len(datos1))
print(len(datos2))

def pair_data(datos,components):
    #datos=datos.drop(datos[datos['Session']=='V4P'].index)#Borrar datos
    datos['Session']=datos['Session'].replace({'VO':'V0','V4P':'V4'})
    groups=['CTR','G2'] # Pair groups 
    datos=datos[datos.Components.isin(components) ] # Only data of components select
    datos=datos[datos.Group.isin(groups) ] #Only data of CTR y G2
    visitas=['V0','V1','V2','V3']
    #Script for drop subjects without four sessions select
    for i in groups:
        g=datos[datos['Group']==i]
        sujetos=g['Subject'].unique()
        print('Cantidad de sujetos de '+i+': ', len(sujetos))
        k=0
        for j in sujetos:
            s=g[g['Subject']==j]
            if len(s['Session'].unique()) !=4:
                k=k+1
                datos=datos.drop(datos[datos['Subject']==j].index)
            if len(s['Session'].unique()) ==4:
                v=s['Session'].unique()
                for vis in range(len(visitas)):
                    datos.loc[(datos.Subject==j)&(datos.Session==v[vis]),'Session']=visitas[vis]     
        print('Sujetos a borrar:', k)
        print('Sujetos a analizar con 4 visitas: ',len(sujetos)-k)
    for i in groups:
        g=datos[datos['Group']==i]
        print('Cantidad de sujetos al filtrar '+ i+': ',len(g['Subject'].unique()))
    #datos['Group']=datos['Group'].replace({'CTR':'Control','G2':'Control'})
    print('Visitas de los sujetos: ',datos['Session'].unique())
    return datos

components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ] #Neuronal components
datos=pair_data(datos,components) #Datos filtrados

bandas=datos['Bands'].unique()
Stage=datos['Stage'].unique()
icc_value = pd.DataFrame(columns=['ICC','F','df1','df2','pval','CI95%'])
G=['CTR','G2']
for st in Stage:
    d_stage=datos[datos['Stage']==st] 
    for g in G:
        d_group=d_stage[d_stage['Group']==g]
        dic={}
        icc_comp=[]
        for comp in components:
            d_comp=d_group[d_group['Components']==comp]
            visits=list(d_comp['Session'].unique())
            matrix_c=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage','Subject']) #Se le asigna a un dataframe los datos d elas columnas
            subjects=d_comp['Subject'].unique() 
            for vis in visits:
                matrix_s=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage','Subject'])
                power=d_comp[d_comp['Session']==vis]['Powers'].tolist()
                n_vis=[vis]*len(power)
                #print(len(n_vis))
                matrix_s['Session']=n_vis
                matrix_s['Power']=power  
                matrix_s['Group']=d_comp[d_comp['Session']==vis]['Group'].tolist()
                matrix_s['Bands']=d_comp[d_comp['Session']==vis]['Bands'].tolist()
                matrix_s['Stage']=d_comp[d_comp['Session']==vis]['Stage'].tolist()
                matrix_s['Subject']=d_comp[d_comp['Session']==vis]['Subject'].tolist()

                matrix_c=matrix_c.append(matrix_s, ignore_index = True)            
            
            index=list(np.arange(0,len(n_vis),1))*len(visits)
            matrix_c['index']=index

            for i,ban in enumerate(bandas):
                fil_bands=matrix_c['Bands']==ban
                filter=matrix_c[fil_bands]
                icc=pg.intraclass_corr(data=filter, targets='index', raters='Session', ratings='Power').round(6)
                #icc3=icc
                icc3 = icc[icc['Type']=='ICC3k']
                icc3 = icc3.set_index('Type')
                # print(filter['Stage'])
                icc3['Stage']=st #filter['Stage'][i]
                icc3['Group']=g #filter['Group'][i]
                icc3['Bands']=ban
                icc3['Components']=comp
                icc_value=icc_value.append(icc3,ignore_index=True)

        icc_value.append(icc_value)
    icc_value.append(icc_value)
#print(icc_value)
icc_value.to_csv(r'sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_Components_G2-CTR.csv',sep=';')
#matrix_c.to_csv(r'sovaharmony\Reproducibilidad\icc_values_G2-CTR_test.csv',sep=';') #
