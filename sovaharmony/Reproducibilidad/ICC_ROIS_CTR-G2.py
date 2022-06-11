'''Code used to filter the BIOMARCADORES database by ROIS of the G2 and CTR groups.
They have the same number of visits but do not correspond to the same visits.
The ICC is calculated with these data  '''

import numpy as np
import pandas as pd 
import collections
import scipy.io
import pingouin as pg

# datos1=pd.read_excel(r"sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_channels_norm.xlsx") 
# datos2=pd.read_excel(r"sovaharmony\Reproducibilidad\Data_csv_Powers_Componentes-Channels\longitudinal_data_powers_long_channels.xlsx")
datos2=pd.read_feather(r'F:\BIOMARCADORES\derivatives\longitudinal_data_powers_long_CE_norm_channels.feather')
datos1=pd.read_feather(r'F:\BIOMARCADORES\derivatives\longitudinal_data_powers_long_CE_channels.feather')
datos=pd.concat((datos1,datos2))

def add_ROIS_filter_data(data,groups,rois,rois_labels):
    '''Function created to add a column with the ROI corresponding to the channel,
    and filter the data to obtain only 4 visits.'''
    datos=data.copy()

    datos['Session']=datos['Session'].replace({'VO':'V0','V4P':'V4'})
    datos=datos[datos.Group.isin(groups) ] #Only data of groups selected
    for i in range(len(rois)):
        filas=datos.Channels.isin(rois[i])
        datos.loc[filas,'Roi']=rois_labels[i]#It is added in the new column Roi the corresponding Roi
    visitas=['V0','V1','V2','V3'] #4 visits selected
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
    datos['Group']=datos['Group'].replace({'CTR':'Control','G2':'Control'})
    print('Visitas de los sujetos: ',datos['Session'].unique())
    return datos



#ROIS
F = ['FP1', 'FPZ', 'FP2', 'AF3', 'AF4', 'F7', 'F5', 'F3', 'F1', 'FZ', 'F2', 'F4', 'F6', 'F8'] 
T = ['FT7', 'FC5', 'FC6', 'FT8', 'T7', 'C5', 'C6', 'T8', 'TP7', 'CP5', 'CP6', 'TP8']
C = ['FC3', 'FC1', 'FCZ', 'FC2', 'FC4', 'C3', 'C1', 'CZ', 'C2', 'C4', 'CP3', 'CP1', 'CPZ', 'CP2', 'CP4'] 
PO = ['P7', 'P5', 'P3', 'P1', 'PZ', 'P2', 'P4', 'P6', 'P8', 'PO7', 'PO5', 'PO3', 'POZ', 'PO4', 'PO6', 'PO8', 'CB1', 'O1', 'OZ', 'O2', 'CB2']
rois = [F,C,PO,T]
roi_labels = ['F','C','PO','T']
groups=['CTR','G2'] 

datos=add_ROIS_filter_data(datos,groups,rois,roi_labels)

bandas=datos['Bands'].unique()
Stage=datos['Stage'].unique()

icc_value = pd.DataFrame(columns=['Description','ICC','F','df1','df2','pval','CI95%'])
G=['Control']
for st in Stage:
    d_stage=datos[datos['Stage']==st] 
    for g in G:
        d_group=d_stage[d_stage['Group']==g]
        dic={}
        icc_roi=[]
        for roi in roi_labels:
            d_roi=d_group[d_group['Roi']==roi]
            visits=list(d_roi['Session'].unique())
            matrix_c=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage','Subject']) #Se le asigna a un dataframe los datos d elas columnas
            subjects=d_roi['Subject'].unique() 
            for vis in visits:
                matrix_s=pd.DataFrame(columns=['index','Session', 'Power','Bands','Group','Stage','Subject'])
                power=d_roi[d_roi['Session']==vis]['Powers'].tolist() #All powers for one roi and one visit 
                n_vis=[vis]*len(power)# list of the corresponding visit name for powers
                matrix_s['Session']=n_vis
                matrix_s['Power']=power  
                matrix_s['Group']=d_roi[d_roi['Session']==vis]['Group'].tolist()
                matrix_s['Bands']=d_roi[d_roi['Session']==vis]['Bands'].tolist()
                matrix_s['Stage']=d_roi[d_roi['Session']==vis]['Stage'].tolist()
                matrix_s['Subject']=d_roi[d_roi['Session']==vis]['Subject'].tolist()
                matrix_c=matrix_c.append(matrix_s, ignore_index = True)       

            index=list(np.arange(0,len(n_vis),1))*len(visits)
            matrix_c['index']=index

            #print('\n Matriz Roi '+g+' '+st+' ',roi)
            for i,ban in enumerate(bandas):
                fil_bands=matrix_c['Bands']==ban
                filter=matrix_c[fil_bands]
                icc=pg.intraclass_corr(data=filter, targets='index', raters='Session', ratings='Power').round(6)
                icc3=icc
                #icc3 = icc[icc['Type']=='ICC3k']
                
                #icc3 = icc3.set_index('Type')
               # print(filter['Stage'])
                icc3['Stage']=st
                icc3['Group']=g
                icc3['Bands']=ban
                icc3['Roi']=roi
                icc_value=icc_value.append(icc3,ignore_index=True)

        icc_value.append(icc_value)
    icc_value.append(icc_value)
#print(icc_value)
icc_value.to_csv(r'sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_ROIS_G2-CTR_w20.csv',sep=';')

