'''Code used to filter the BIOMARCADORES database by components of the G2 and CTR groups.
They have the same number of visits but do not correspond to the same visits.
The ICC is calculated with these data '''

import numpy as np
import pandas as pd 
import collections
import scipy.io
from tokenize import group
import pingouin as pg
from scipy import stats

datos1=pd.read_feather(r"eeg_harmonization\sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_components.feather") 
datos2=pd.read_feather(r"eeg_harmonization\sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_CE_norm_components.feather")
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

# ANOVA mix
# print('Anova mix')
# aov = pg.mixed_anova(data = datos, dv = 'Powers', between = 'Group', within = 'Session',subject = 'Subject',correction=True)
# pg.print_table(aov)

#U test
print('Test U')
ap=pg.mwu(datos[datos['Group']=='CTR']['Powers'],datos[datos['Group']=='G2']['Powers'])
pg.print_table(ap)
