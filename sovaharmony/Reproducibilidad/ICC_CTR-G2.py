'''Codigo usado para filtrar los datos de biomarcadores de los grupos G2 y CTR.
Quedan con la misma cantidad de visitas pero no corresponden a las mismas visitas
Se calcula el ICC con estos datos  '''

import numpy as np
import pandas as pd 
import collections
import scipy.io
from tokenize import group
import pingouin as pg

datos1=pd.read_excel('sovaharmony\Reproducibilidad\longitudinal_data_powers_long_components_norm.xlsx') 
datos2=pd.read_excel('sovaharmony\Reproducibilidad\longitudinal_data_powers_long_components.xlsx')
datos=pd.concat((datos1,datos2))
datos=datos.drop(datos[datos['Session']=='V4P'].index)#Borrar datos
datos['Session']=datos['Session'].replace({'VO':'V0','V4P':'V4'})
components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]
groups=['CTR','G2']
datos=datos[datos.Components.isin(components) ] #Solo los datos de las componentes seleccionadas
datos=datos[datos.Group.isin(groups) ] #Solo los datos de CTR y G2
visitas=['V0','V1','V2','V3']
#Codigo para eliminar los sujetos sin 4 visitas
for i in groups:
    g=datos[datos['Group']==i]
    #visitas=g['Session'].unique()
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

                #datos[datos['Subject']==j]['Session'].replace({v[vis]:visitas[vis]})        
    print('Sujetos a borrar:', k)
    print('Sujetos a analizar con 4 visitas: ',len(sujetos)-k)

for i in groups:
    g=datos[datos['Group']==i]
    print('Cantidad de sujetos al filtrar '+ i+': ',len(g['Subject'].unique()))


print(datos['Session'].unique())



visitas=['V0','V1','V2','V3']
bandas=datos['Bands'].unique()
Stage=datos['Stage'].unique()
datos['Group']=datos['Group'].replace({'CTR':'Control','G2':'Control'})
icc_value = pd.DataFrame(columns=['Description','ICC','F','df1','df2','pval','CI95%'])
G=['Control']
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
icc_value.to_csv(r'sovaharmony\Reproducibilidad\icc_values_G2-CTR.csv',sep=';')

