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
from funtionsHarmonize import renameDatabases
from funtionsHarmonize import sumNegatives
from funtionsHarmonize import descrive
from funtionsHarmonize import renameModel
from funtionsHarmonize import covars
from funtionsHarmonize import add_Gamma
from funtionsHarmonize import return_col
from funtionsHarmonize import extract_components_interes
from funtionsHarmonize import rename_cols
from funtionsHarmonize import graf
from funtionsHarmonize import delcolumn

#m = ['power'] 
#b = ['Gamma']
#space='roi'
space='ic'
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
for allm in m:  
#    for allb in b:  
    #Tab
    path_feather = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes/' 
    data = pd.read_feather(path_feather+r'\Data_complete_'+space+'.feather')
    data = data[(data['age'] >= 24) | (data['age'] <= 38)] # (Controles 44) - (G1G2 24) # (Controles 57) - (G1G2 38)
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
    new_dataAll['database'] = database_database
    new_dataAll = return_col(new_dataAll,dd,fist=False)
    if allm == 'power':
        new_dataAll = add_Gamma(new_dataAll,space)
    ##
    dataCTR = mapsDrop(new_dataAll,0.0,'V0','t1')
    dataCTR = dataCTR[(dataCTR['database'] == 3.0) | (dataCTR['database'] == 1.0)]
    dataCTR['database']=dataCTR.database.replace([1.0,3.0],0.0)
    dataG1 = mapsDrop(new_dataAll,3.0,'V0') #Portadores
    dataG1['database']=dataG1.database.replace([0.0,2.0],1.0)
    dataG2 = mapsDrop(new_dataAll,4.0,'V0') #No portadores
    dataG2['database']=dataG2.database.replace([0.0,2.0],0.0)
    dataCTRG2 = pd.concat([dataCTR, dataG2])
    datacol = pd.concat([dataCTRG2, dataG1])
    ##

    data_eeg_dataAll = datacol.reset_index(drop=True) 
    data_eeg_dataAll = rename_cols(data_eeg_dataAll,'BIOMARCADORES','CHBMP+SRM+BIOMARCADORES','Control','G1')
    new_name = 'Data_complete_'+space+'_neuroHarmonize_'+allm
    data_eeg_dataAll.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_feather,name=new_name))
    #noGene_h,Gene_h = renameModel(new_All)
    noGene_ht,Gene_ht = renameModel(new_dataAll)
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