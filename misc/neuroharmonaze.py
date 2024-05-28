'''
Componentes de interés
    C14, C15, C18, C20, C22, C23, C24, C25 
'''
#Armonizar y luego juntar
from neuroHarmonize import harmonizationLearn
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from funtionsHarmonize import mapsDrop
from funtionsHarmonize import negativeTest
from funtionsHarmonize import select
from funtionsHarmonize import renameModel, renameDatabases
from funtionsHarmonize import covars, covarsGen
from funtionsHarmonize import extract_components_interes
from funtionsHarmonize import rename_cols
from paired_tests import MatchIt_R
from funtionsHarmonize import organizarDataFrame
from funtionsHarmonize import graf, graf_DB
from funtionsHarmonize import save_complete
import tkinter as tk
from tkinter.filedialog import askdirectory
import os
tk.Tk().withdraw() # part of the import if you are not using other tkinter functions

def neurosovaHarmonize(m,b,bm,s,A,B,path_feather,path_input,path_graph,new_name,Gen=False):
    for space in s:
        for allm in m:  
            data_in = pd.read_feather(path_input+space+'.feather')
            data = MatchIt_R(data_in,A,B)
            dd = data.copy()
            data = mapsDrop(data)
            if Gen == True:
                '''
                En la armonización de grupos entre los que tienen mutación y los que no, 
                sólo se agregan factores que hagan que cambien la adquisición, 
                asumiendo que debería ser similar, estos pueden ser: equipo de adquisición, 
                ciudad, tipo de gorro, tipo de referencia…
                '''
                dataAll,covarsAll = covarsGen(data)
            else: 
                dataAll,covarsAll = covars(data)
            #title,dataAll = select(dataAll,allm,OneBand=None,WithoutBand=None,Gamma=None,space=space)
            title,dataAll = select(dataAll,allm,OneBand=None,WithoutBand=None,Gamma='power',space=space)
            
            ######### eeg_harmonization ##########
            noGene,Gene = renameModel(dataAll)
            BS,DS,SS,CS = renameDatabases(dataAll)
            noGene.drop(['database'],axis=1,inplace=True)
            nnoGene=negativeTest(np.array(noGene))
            Gene.drop(['database'],axis=1,inplace=True)
            nGene=negativeTest(np.array(Gene))

            ##
            covarsAll = pd.DataFrame(covarsAll)  
            database_database = np.array(dataAll['database'])
            dataAll.drop(['database'],axis=1,inplace=True)
            #dataAll = delcolumn(data,'crossfreq',em=None)
            columnasAll = dataAll.columns
            if space == 'ic':
                #dataAll = delcolumn(data,'Gamma',bm='Mgamma')
                #dataAll = delcolumn(data,'crossfreq',em=None)
                components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]
                dataAll=extract_components_interes(dataAll,components)
                columnasAll = dataAll.columns
            else:
                pass
            
            #save sovaharmony
            sovaeeg = dataAll.copy()

            data_sovaeeg = organizarDataFrame(sovaeeg,database_database,allm,dd,space)
            os.makedirs(path_feather + fr'\sovaharmony\complete',exist_ok=True)
            save_complete(new_name+space+rf'_sovaharmony_{A}_'+allm,data_sovaeeg,dd,path_feather+fr'\sovaharmony\complete'+rf'\{space}\{A}',B,A)
            
            #neuroHarmonize
            my_dataAll = np.array(dataAll)
            nmy_dataAll =negativeTest(my_dataAll)
            data_transformtdataAll = np.log(0.001+my_dataAll)
            # run harmonization and store the adjusted data
            my_modeldataAll, my_data_adjdataAll = harmonizationLearn(data_transformtdataAll, covarsAll) ###DUDA
            #my_modeldataAll, my_data_adjdataAll = harmonizationLearn(my_dataAll, covarsAll,smooth_terms=['gender'])
            my_data_adj_trans = np.exp(my_data_adjdataAll)-0.001 #back-transform
            nmy_data_adjdataAll=negativeTest(my_data_adj_trans)
            datos_windex=dataAll.reset_index() 
            new_dataAll = pd.DataFrame(data=my_data_adj_trans,columns=columnasAll)  
            

            #save neuroHarmonize
            datacol = organizarDataFrame(new_dataAll,database_database,allm,dd,space) 
            os.makedirs(path_feather + fr'\neuroHarmonize\complete',exist_ok=True)
            #save_complete(new_name+space+rf'_neuroHarmonize_{A}_'+allm,datacol,dd,path_feather+fr'\neuroHarmonize\complete'+rf'\{space}\{A}',B,A)


            #noGene_h,Gene_h = renameModel(new_All)
            noGene_ht,Gene_ht = renameModel(new_dataAll)
            BH,DH,SH,CH = renameDatabases(new_dataAll)
            #graf(path_graph+ fr'\Gauss',columnasAll,noGene,Gene,noGene_ht,Gene_ht,nnoGene,nGene,nmy_dataAll,nmy_data_adjdataAll,title,space)
            #graf_DB(path_graph+ fr'\Gauss',columnasAll,BS,DS,SS,CS,BH,DH,SH,CH,title,space)

## Lists
m = ['power'] #['power','sl','cohfreq','entropy','crossfreq'] 
b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma'] 
bm = ['Mdelta','Mtheta','Malpha-1','Malpha-2','Mbeta1','Mbeta2','Mbeta3','Mgamma']  
#s=['roi','ic']
s=['ic']

## Groups
#Portadores vs Controles
A = 'G1'
B= 'Control'

##Sintomaticos vs Controles
#A = 'DTA'
#B= 'Control'
#
##Portadores vs No Portadores
#A = 'G1'
#B= 'G2'

## Paths
path = askdirectory()
print("user chose", path, "for read feather")
path_feather = path + r'\dataframes'
os.makedirs(path_feather,exist_ok=True)
path_input = path + r'\dataframes\Data_complete_'
os.makedirs(path_input,exist_ok=True)
path_graph = path + r'\graphics'
os.makedirs(path_graph,exist_ok=True)

## Names
new_name = 'Data_complete_'


neurosovaHarmonize(m,b,bm,s,A,B,path_feather,path_input,path_graph,new_name,Gen=False)