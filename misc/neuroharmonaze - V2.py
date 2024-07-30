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
#from paired_tests import MatchIt_R_Propensity_5_1,MatchIt_R_Propensity_10_1, MatchIt_R_15, MatchIt_R_10
from paired_tests_2 import match_and_optimize
from funtionsHarmonize import organizarDataFrame
from funtionsHarmonize import graf, graf_DB
from funtionsHarmonize import save_complete
import tkinter as tk
from tkinter.filedialog import askdirectory
import os
tk.Tk().withdraw() # part of the import if you are not using other tkinter functions

# ratio es la cantidad de valores de G1 esperado para cumplir con el matching 2:1, 5:1, 10:1, por defecto 2:1 para 2 controles por cada G1 teniendo 158 controles
def neurosovaHarmonize(m,b,bm,s,ica,group1,group2,path_feather,path_input,path_graph,new_name,Gen=False,ratio=79):
    group1 = A
    group2 = B
    if ratio == 79:
        str_ratio = '2to1'
    elif ratio == 31:
        str_ratio = '5to1'
    elif ratio == 15:
        str_ratio = '10to1'
    else:
        str_ratio = str(ratio)
    
    os.makedirs(path_feather + fr'\sovaharmony\complete'+str_ratio,exist_ok=True)
    os.makedirs(path_feather + fr'\neuroHarmonize\complete'+str_ratio,exist_ok=True)
    os.makedirs(path_feather+fr'\sovaharmony\complete'+str_ratio,exist_ok=True)


    for space in s:
        for allm in m:  
            data_in = pd.read_feather(path_input+space+'.feather')
            #data = MatchIt_R_15(data_in,A,B)
            #data = MatchIt_R_Propensity_5_1(data_in,A,B)
            data = match_and_optimize(data_in, group1, group2, ratio)
            dd = data.copy()
            data = mapsDrop(data)
            if Gen == True:
                '''
                En la armonización de grupos entre los que tienen mutación y los que no, 
                sólo se agregan factores que hagan que cambien la adquisición, 
                asumiendo que debería ser similar, estos pueden ser: equipo de adquisición, 
                ciudad, tipo de gorro, tipo de referencia… 
                ESTE IF ES SOLO PARTE DE UNA PRUEBA
                '''
                dataAll,covarsAll = covarsGen(data)
            else: 
                dataAll,covarsAll = covars(data)
            #title,dataAll = select(dataAll,allm,OneBand=None,WithoutBand=None,Gamma=None,space=space)
            title,dataAll = select(dataAll,allm,OneBand=None,WithoutBand=None,Gamma='power',space=space)
            
            ######### eeg_harmonization ##########
            def procesar_data(data):
                noGene, Gene = renameModel(data)
                BS, DS, SS, CS = renameDatabases(data)
                columns_to_drop = ['database', 'visit_x', 'visit_y']
                noGene = noGene.drop(columns=columns_to_drop)
                nnoGene = negativeTest(np.array(noGene))
                Gene = Gene.drop(columns=columns_to_drop)
                nGene = negativeTest(np.array(Gene))
                return nnoGene, nGene

            if all(col in dataAll.columns for col in ['visit', 'visit_x', 'visit_y']):
                print("Todas las columnas existen")
                nnoGene, nGene = procesar_data(dataAll)
            elif any(col in dataAll.columns for col in ['visit', 'visit_x', 'visit_y']):
                print("Alguna de las columnas existe, pero no todas")
                nnoGene, nGene = procesar_data(dataAll)
            else:
                print("Ninguna de las columnas existe")

            ##
            covarsAll = pd.DataFrame(covarsAll)  
            database_database = np.array(dataAll['database'])
            dataAll.drop(['database'],axis=1,inplace=True)
            #dataAll = delcolumn(data,'crossfreq',em=None)
            columnasAll = dataAll.columns
            if space == 'ic':
                #dataAll = delcolumn(data,'Gamma',bm='Mgamma')
                #dataAll = delcolumn(data,'crossfreq',em=None)
                if ica == '54x10':
                    components=['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']
                elif ica == '58x25':
                    components=['C14', 'C15','C18', 'C20', 'C22','C23', 'C24', 'C25' ]
                else:
                    print('Error ICA')
                
                dataAll=extract_components_interes(dataAll,components)
                columnasAll = dataAll.columns
            else:
                pass
            
            #save sovaharmony
            sovaeeg = dataAll.copy()

            data_sovaeeg = organizarDataFrame(sovaeeg,database_database,allm,dd,space,ica)
            os.makedirs(path_feather + fr'\sovaharmony\complete'+str_ratio,exist_ok=True)
            os.makedirs(path_feather+fr'\sovaharmony\complete'+str_ratio+rf'\{space}\{A}',exist_ok=True)
            save_complete(new_name+'_'+space+rf'_sovaharmony_{A}_'+allm,data_sovaeeg,dd,path_feather+fr'\sovaharmony\complete'+str_ratio+rf'\{space}\{A}',B,A)
            
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
            datacol = organizarDataFrame(new_dataAll,database_database,allm,dd,space,ica) 
            os.makedirs(path_feather + fr'\neuroHarmonize\complete'+str_ratio,exist_ok=True)
            os.makedirs(path_feather+fr'\neuroHarmonize\complete'+str_ratio+rf'\{space}\{A}',exist_ok=True)
            save_complete(new_name+'_'+space+rf'_neuroHarmonize_{A}_'+allm,datacol,dd,path_feather+fr'\neuroHarmonize\complete'+str_ratio+rf'\{space}\{A}',B,A)


            #noGene_h,Gene_h = renameModel(new_All)
            noGene_ht,Gene_ht = renameModel(new_dataAll)
            BH,DH,SH,CH = renameDatabases(new_dataAll)
            #graf(path_graph+ fr'\Gauss',columnasAll,noGene,Gene,noGene_ht,Gene_ht,nnoGene,nGene,nmy_dataAll,nmy_data_adjdataAll,title,space)
            #graf_DB(path_graph+ fr'\Gauss',columnasAll,BS,DS,SS,CS,BH,DH,SH,CH,title,space)
## Lists
m = ['power','sl','cohfreq','entropy','crossfreq'] 
b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma'] 
bm = ['Mdelta','Mtheta','Malpha-1','Malpha-2','Mbeta1','Mbeta2','Mbeta3','Mgamma']  
#s=['roi','ic']
s=['ic']
ica = '58x25' #54x10

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
#path = askdirectory()
#path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_Paper_V2'
#path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_54x10\Datosparaorganizardataframes/'
path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_Correcciones_Evaluador\Datosparaorganizardataframes/11092023'
#print("user chose", path, "for read feather")
path_feather = path + r'\dataframes'
path_input = path + r'\dataframes\Data_complete_'
path_graph = path + r'\graphics'
os.makedirs(path_feather,exist_ok=True)
os.makedirs(path_graph,exist_ok=True)

new_name = 'Data_complete'
neurosovaHarmonize(m,b,bm,s,ica,A,B,path_feather,path_input,path_graph,new_name,Gen=False,ratio=79) #2:1
#neurosovaHarmonize(m,b,bm,s,ica,A,B,path_feather,path_input,path_graph,new_name,Gen=False,ratio=31) #5:1
#neurosovaHarmonize(m,b,bm,s,ica,A,B,path_feather,path_input,path_graph,new_name,Gen=False, ratio=15) #10:1
