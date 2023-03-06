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


#m = ['power'] 
#b = ['Gamma']

m = ['power','sl','cohfreq','entropy','crossfreq'] 
b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma'] 

path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize'
filename = r"{path}\{m}_stats_G1G2.xlsx".format(path=path,m=m)
writer = pd.ExcelWriter(filename)
#filename_trans = r"{path}\{m}_stats_trans.xlsx".format(path=path,m=m)
#writer_trans = pd.ExcelWriter(filename_trans)
#pd.io.formats.excel.header_style = None
df_stats = pd.DataFrame(columns=['Std_sovaharmony','Var_sovaharmony','Mean_sovaharmony','Min_sovaharmony','Max_sovaharmony','Values_close_to_zero_sovaharmony','Negative_sovaharmony','Var_neuroHarmonize','Std_neuroHarmonize','Mean_neuroHarmonize','Min_neuroHarmonize','Max_neuroHarmonize','Values_close_to_zero_neuroHarmonize','Negative__neuroHarmonize'])
#df_stats_trans = pd.DataFrame(columns=['Std_sovaharmony','Var_sovaharmony','Mean_sovaharmony','Min_sovaharmony','Max_sovaharmony','Values_close_to_zero_sovaharmony','Negative_sovaharmony','Var_neuroHarmonize','Std_neuroHarmonize','Mean_neuroHarmonize','Min_neuroHarmonize','Max_neuroHarmonize','Values_close_to_zero_neuroHarmonize','Negative__neuroHarmonize'])

row=0
for allm in m:  
    for allb in b:  
#Tab
        data = pd.read_feather(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\Data_complete_roi.feather')
        #data = data[data['age'] >= 24] # (Controles 44) - (G1G2 24)
        #data = data[data['age'] <= 38] # (Controles 57) - (G1G2 38)
        dataG1,covarsG1 = mapsDrop(data,3.0)
        dataG2,covarsG2 = mapsDrop(data,4.0)
        title,dataG1 = select(dataG1,allm,OneBand=allb,WithoutBand=None)
        title,dataG2 = select(dataG2,allm,OneBand=allb,WithoutBand=None)
        #title,data = select(data,'All',OneBand=None,WithoutBand='Gamma')
        ######## eeg_harmonization ##########
        #data_eeg_G1 = dataG1.reset_index(drop=True) 
        #data_eeg_G2 = dataG2.reset_index(drop=True) 
        #Biomarcadores_eeg_G1,Duque_eeg_G1,SRM_eeg_G1,CHBMP_eeg_G1 = renameDatabases(data_eeg_G1)
        #Biomarcadores_eeg_G2,Duque_eeg_G2,SRM_eeg_G2,CHBMP_eeg_G2 = renameDatabases(data_eeg_G2)
        #Biomarcadores_eeg_G1.drop(['database'],axis=1,inplace=True)
        #Duque_eeg_G1.drop(['database'],axis=1,inplace=True)
        #nG1 = sumNegatives(Biomarcadores_eeg_G1,Duque_eeg_G1)
        #Biomarcadores_eeg_G2.drop(['database'],axis=1,inplace=True)
        #Duque_eeg_G2.drop(['database'],axis=1,inplace=True)
        #nG2 = sumNegatives(Biomarcadores_eeg_G2,Duque_eeg_G2)

        ######## neuroHarmonize ###########
        database_colG1 = np.array(dataG1['database'])
        database_colG2 = np.array(dataG2['database'])
        dataG1.drop(['database'],axis=1,inplace=True)
        dataG2.drop(['database'],axis=1,inplace=True)
        columnasG1 = dataG1.columns
        columnasG2 = dataG2.columns
        covarsG1 = pd.DataFrame(covarsG1)  
        my_dataG1 = np.array(dataG1)
        covarsG2 = pd.DataFrame(covarsG2)  
        my_dataG2 = np.array(dataG2)
        negativeTest(my_dataG1)
        negativeTest(my_dataG2)
        #data_transformtG1 = np.log(0.001+my_dataG1)
        #data_transformtG2 = np.log(0.001+my_dataG2)
        # run harmonization and store the adjusted data
        my_modelG1, my_data_adjG1 = harmonizationLearn(my_dataG1, covarsG1,smooth_terms=['gender'])
        my_modelG2, my_data_adjG2 = harmonizationLearn(my_dataG2, covarsG2,smooth_terms=['gender'])
        #my_model_trans, my_data_adj_trans = harmonizationLearn(data_transformt, covars,smooth_terms=['gender'])
        #df_my_model = pd.DataFrame(columns=list(my_model.keys()))
        #for i in list(my_model.keys()):
        #    df_my_model[i] = my_model[i].tolist()
        nG1=negativeTest(my_data_adjG1)
        nG2=negativeTest(my_data_adjG2)
        #nht=negativeTest(my_data_adj_trans)
        #my_data_adj_trans = np.exp(my_data_adj_trans)-0.0009 #back-transform
        #nht_bt=negativeTest(my_data_adj_trans)
        datos_windex=data.reset_index()    
        new_dataG1 = pd.DataFrame(data=my_data_adjG1,columns=columnasG1)
        new_dataG2 = pd.DataFrame(data=my_data_adjG2,columns=columnasG2)
        new_dataG1['database'] = database_colG1
        new_dataG2['database'] = database_colG2
        #new_data_trans = pd.DataFrame(data=my_data_adj_trans,columns=columnas)
        #new_data_trans['database'] = database_col
        stats_metricsG1 = descrive(dataG1,new_dataG1)
        stats_metricsG2 = descrive(dataG2,new_dataG2)
        #stats_metrics_trans = descrive(data,new_data_trans)
        df_statsG1 = df_stats.append(stats_metricsG1,ignore_index = True)
        df_statsG2 = df_stats.append(stats_metricsG2,ignore_index = True)
        #df_stats_trans = df_stats_trans.append(stats_metrics_trans,ignore_index = True)
        BiomarcadoresG1,DuqueG1,SRMG1,CHBMPG1 = renameDatabases(new_dataG1)
        BiomarcadoresG2,DuqueG2,SRMG2,CHBMPG2 = renameDatabases(new_dataG2)
        for band in columnasG1:
            sns.kdeplot(BiomarcadoresG1[band], color='darkcyan', label='Biomarcadores G1')
            sns.kdeplot(DuqueG1[band], color='#708090', label='Duque G1')
            sns.kdeplot(BiomarcadoresG2[band], color='darkcyan', label='Biomarcadores G2', linestyle='--')
            sns.kdeplot(DuqueG2[band], color='#708090', label='Duque G2', linestyle='--')
            plt.title(f'# negatives - sovaharmony(-): {nG1} and neuroHarmonize(--): {nG2}')
            #plt.title(f'# negatives - sovaharmony(-): {npp} and neuroHarmonizeTransform(--): {nht_bt} ')
            plt.suptitle(title)
            plt.legend()
            plt.show()
            #plt.savefig(r'{path}\TransformadosG1G2\{name}_{title}_G1G2density.png'.format(path=path,name=band,title=title))
            plt.close()
#Tab
        df_stats.to_excel(writer, startrow=row)
        #df_stats_trans.to_excel(writer_trans, startrow=row)
        row+=5
        writer.save()
        #writer_trans.save()
## Tab
writer.close()
#writer_trans.close()    