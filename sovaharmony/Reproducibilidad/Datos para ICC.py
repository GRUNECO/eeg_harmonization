import numpy as np
import pandas as pd 
import collections
import scipy.io
import pingouin as pg

datos1=pd.read_excel('longitudinal_data_powers_long_components.xlsx') 
datos2=pd.read_excel('longitudinal_data_powers_long_components_norm.xlsx')
datos=pd.concat((datos1,datos2))


datos=datos.drop(datos[datos['Session']=='V4P'].index)#Borrar datos
components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]
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

for st in Stage:
    d_stage=datos[datos['Stage']==st] 
    for g in G:
        d_group=d_stage[d_stage['Group']==g]
        dic={}
        for comp in components:
            d_comp=d_group[d_group['Components']==comp]
            visits=list(d_comp['Session'].unique())
            matrix_c=pd.DataFrame(columns=visits) #Se le asigna a un dataframe los datos d elas columnas
            subjects=d_comp['Subject'].unique() 
            for sub in subjects:
                d_sub=d_comp[d_comp['Subject']==sub] 
                matrix_s=pd.DataFrame(columns=visits)
                for vis in visits:
                    power=d_sub[d_sub['Session']==vis]['Powers'].tolist()
                    matrix_s[vis]=power
                matrix_c=matrix_c.append(matrix_s, ignore_index = True)

            #matrix_c=matrix_c.to_numpy() #Mtriz a hacer ICC 
            print('Matriz componente '+g+' '+st+' ',comp)
            icc = pg.intraclass_corr(data=matrix_c, targets=index, raters='Judge', ratings='Scores').round(3)
            icc.set_index("Type")
            
            # print('Tamaño de la matriz: ',matrix_c.shape)
            # print(matrix_c)

            dic[comp]=matrix_c
        
        if st=='Normalized data':
            st='Normalized'
        elif st=='Preprocessed data':
            st='Preprocessed'
        scipy.io.savemat(g+'_'+st+'.mat', dic)


