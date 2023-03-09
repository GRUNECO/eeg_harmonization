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


#m = ['crossfreq'] 
#b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']

m = ['power','sl','cohfreq','entropy','crossfreq'] 
b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma'] 

path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize'
filename = r"{path}\{m}_stats.xlsx".format(path=path,m=m)
writer = pd.ExcelWriter(filename)
filename_trans = r"{path}\{m}_stats_trans.xlsx".format(path=path,m=m)
writer_trans = pd.ExcelWriter(filename_trans)
pd.io.formats.excel.header_style = None
df_stats = pd.DataFrame(columns=['Std_sovaharmony','Var_sovaharmony','Mean_sovaharmony','Min_sovaharmony','Max_sovaharmony','Values_close_to_zero_sovaharmony','Negative_sovaharmony','Var_neuroHarmonize','Std_neuroHarmonize','Mean_neuroHarmonize','Min_neuroHarmonize','Max_neuroHarmonize','Values_close_to_zero_neuroHarmonize','Negative__neuroHarmonize'])
df_stats_trans = pd.DataFrame(columns=['Std_sovaharmony','Var_sovaharmony','Mean_sovaharmony','Min_sovaharmony','Max_sovaharmony','Values_close_to_zero_sovaharmony','Negative_sovaharmony','Var_neuroHarmonize','Std_neuroHarmonize','Mean_neuroHarmonize','Min_neuroHarmonize','Max_neuroHarmonize','Values_close_to_zero_neuroHarmonize','Negative__neuroHarmonize'])

row=0
#for allm in m:  
#    for allb in b:  
#Tab
path_feather = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes/' 
data = pd.read_feather(path_feather+r'Data_complete_roi.feather')
datavo,covars = mapsDrop(data,0.0,'V0')
datat1,covars = mapsDrop(data,0.0,'t1')
#title,data = select(data,allm,OneBand=allb,WithoutBand=None)
title,data = select(data,'All',OneBand=None,WithoutBand=None)
######## eeg_harmonization ##########
data_eeg = data.reset_index(drop=True) 
Biomarcadores_eeg,Duque_eeg,SRM_eeg,CHBMP_eeg = renameDatabases(data_eeg)
Biomarcadores_eeg.drop(['database'],axis=1,inplace=True)
Duque_eeg.drop(['database'],axis=1,inplace=True)
SRM_eeg.drop(['database'],axis=1,inplace=True)
CHBMP_eeg.drop(['database'],axis=1,inplace=True)
npp = sumNegatives(Biomarcadores_eeg,Duque_eeg,SRM_eeg,CHBMP_eeg)

######## neuroHarmonize ###########
database_col = np.array(data['database'])
data.drop(['database'],axis=1,inplace=True)
columnas = data.columns
covars = pd.DataFrame(covars)  
my_data = np.array(data)
negativeTest(my_data)
data_transformt = np.log(0.001+my_data)
# run harmonization and store the adjusted data
my_model, my_data_adj = harmonizationLearn(my_data, covars,smooth_terms=['gender'])
my_model_trans, my_data_adj_trans = harmonizationLearn(data_transformt, covars,smooth_terms=['gender'])
#df_my_model = pd.DataFrame(columns=list(my_model.keys()))
#for i in list(my_model.keys()):
#    df_my_model[i] = my_model[i].tolist()
print(my_data_adj)
nh=negativeTest(my_data_adj)
nht=negativeTest(my_data_adj_trans)
my_data_adj_trans = np.exp(my_data_adj_trans)-0.0009 #back-transform
nht_bt=negativeTest(my_data_adj_trans)
datos_windex=data.reset_index()    
new_data = pd.DataFrame(data=my_data_adj,columns=columnas)
new_data['database'] = database_col
new_data_trans = pd.DataFrame(data=my_data_adj_trans,columns=columnas)
new_data_trans['database'] = database_col
stats_metrics = descrive(data,new_data)
stats_metrics_trans = descrive(data,new_data_trans)
df_stats = df_stats.append(stats_metrics,ignore_index = True)
df_stats_trans = df_stats_trans.append(stats_metrics_trans,ignore_index = True)
new_name = 'Data_complete_roi_neuroHarmonize'
new_data.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_feather,name=new_name))
new_name_trans = 'Data_complete_roi_neuroHarmonize_trans'
new_data_trans.reset_index(drop=True).to_feather('{path}\{name}.feather'.format(path=path_feather,name=new_name_trans))
Biomarcadores,Duque,SRM,CHBMP = renameDatabases(new_data_trans)
for band in columnas:
    sns.kdeplot(Biomarcadores_eeg[band], color='darkcyan', label='Biomarcadores')
    sns.kdeplot(Duque_eeg[band], color='#708090', label='Duque')
    sns.kdeplot(SRM_eeg[band], color='lightgreen', label='SRM')
    sns.kdeplot(CHBMP_eeg[band], color='mediumblue', label='CHBMP')
    sns.kdeplot(Biomarcadores[band], color='darkcyan', label='Biomarcadores', linestyle='--')
    sns.kdeplot(Duque[band], color='#708090', label='Duque', linestyle='--')
    sns.kdeplot(SRM[band], color='lightgreen', label='SRM', linestyle='--')
    sns.kdeplot(CHBMP[band], color='mediumblue', label='CHBMP', linestyle='--')
    #plt.title(f'# negatives - sovaharmony(-): {npp} and neuroHarmonize(--): {nh}')
    plt.title(f'# negatives - sovaharmony(-): {npp} and neuroHarmonizeTransform(--): {nht_bt} ')
    plt.suptitle(title)
    plt.legend()
    plt.show()
    #plt.savefig(r'{path}\Transformados\{name}_{title}_density.png'.format(path=path,name=band,title=title))
    plt.close()
    #if nh==0: 
    #    plt.savefig(r'{path}\SinNegativos\{name}_{title}_density.png'.format(path=path,name=band,title=title))
    #    plt.close()
    #elif nh!=0:
    #    plt.savefig(r'{path}\ConNegativos\{name}_{title}_density.png'.format(name=band,title=title))
    #    plt.close()
#Tab
df_stats.to_excel(writer, startrow=row)
df_stats_trans.to_excel(writer_trans, startrow=row)
row+=5
writer.save()
writer_trans.save()
## Tab
writer.close()
writer_trans.close()    