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
from funtionsHarmonize import renameModel
from funtionsHarmonize import covars
from funtionsHarmonize import extract_components_interes
from funtionsHarmonize import rename_cols
from paired_tests import MatchIt_R
from funtionsHarmonize import organizarDataFrame
from funtionsHarmonize import G1G2
from funtionsHarmonize import save_complete

#m = ['power'] 
#b = ['Gamma']
m = ['power','sl','cohfreq','entropy','crossfreq'] 
#m = ['crossfreq'] 
b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma'] 
path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize'
#filename = r"{path}\{m}_stats_G1G2.xlsx".format(path=path,m=m)
#writer = pd.ExcelWriter(filename)
#filename_trans = r"{path}\{m}_stats_trans.xlsx".format(path=path,m=m)
#writer_trans = pd.ExcelWriter(filename_trans)
#pd.io.formats.excel.header_style = None
#df_stats = pd.DataFrame(columns=['Std_sovaharmony','Var_sovaharmony','Mean_sovaharmony','Min_sovaharmony','Max_sovaharmony','Values_close_to_zero_sovaharmony','Negative_sovaharmony','Var_neuroHarmonize','Std_neuroHarmonize','Mean_neuroHarmonize','Min_neuroHarmonize','Max_neuroHarmonize','Values_close_to_zero_neuroHarmonize','Negative__neuroHarmonize'])
#df_stats_trans = pd.DataFrame(columns=['Std_sovaharmony','Var_sovaharmony','Mean_sovaharmony','Min_sovaharmony','Max_sovaharmony','Values_close_to_zero_sovaharmony','Negative_sovaharmony','Var_neuroHarmonize','Std_neuroHarmonize','Mean_neuroHarmonize','Min_neuroHarmonize','Max_neuroHarmonize','Values_close_to_zero_neuroHarmonize','Negative__neuroHarmonize'])

row=0
s=['roi','ic']

for space in s:
    for allm in m:  
    #    for allb in b:  
        #Tab
        path_feather = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes/' 
        data_in = pd.read_feather(path_feather+r'\Data_complete_'+space+'.feather')
        data = MatchIt_R(data_in,'DTA','Control')
        dd = data.copy()
        data = mapsDrop(data)
        dataAll,covarsAll = covars(data)
        #title,dataAll = select(dataAll,'All',OneBand=None,WithoutBand=None,Gamma='power',space=space)
        title,dataAll = select(dataAll,allm,OneBand=None,WithoutBand=None,Gamma='power',space=space)
        


        ######### eeg_harmonization ##########
        noGene,Gene = renameModel(dataAll)
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
        new_sovaname = 'Data_complete_'+space+'_sovaharmony_DTA_'+allm
        save_complete(new_sovaname,data_sovaeeg,dd,path_feather,'Control','DTA')
        
 
        #neuroHarmonize
        my_dataAll = np.array(dataAll)
        nmy_dataAll =negativeTest(my_dataAll)
        data_transformtdataAll = np.log(0.001+my_dataAll)
        # run harmonization and store the adjusted data
        my_modeldataAll, my_data_adjdataAll = harmonizationLearn(data_transformtdataAll, covarsAll) ###DUDA
        #my_modeldataAll, my_data_adjdataAll = harmonizationLearn(my_dataAll, covarsAll,smooth_terms=['gender'])
        my_data_adj_trans = np.exp(my_data_adjdataAll)-0.0009 #back-transform
        nmy_data_adjdataAll=negativeTest(my_data_adj_trans)
        datos_windex=dataAll.reset_index() 
        new_dataAll = pd.DataFrame(data=my_data_adj_trans,columns=columnasAll)  
        

        #save neuroHarmonize

        datacol = organizarDataFrame(new_dataAll,database_database,allm,dd,space) 
        new_name = 'Data_complete_'+space+'_neuroHarmonize_DTA_'+allm
        save_complete(new_name,datacol,dd,path_feather,'Control','DTA')


        #noGene_h,Gene_h = renameModel(new_All)
        #noGene_ht,Gene_ht = renameModel(new_dataAll)
        #graf(columnasAll,noGene,Gene,noGene_ht,Gene_ht,nnoGene,nGene,nmy_dataAll,nmy_data_adjdataAll,title)

        #Tab
        #df_stats.to_excel(writer, startrow=row)
        #df_stats_trans.to_excel(writer_trans, startrow=row)
        #row+=5
        #writer.save()
        #writer_trans.save()
        ## Tab
        #writer.close()
        #writer_trans.close()   