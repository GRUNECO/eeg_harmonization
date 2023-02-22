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


m = ['power','sl','cohfreq','entropy','crossfreq'] # Pongo las que voy a eliminar
b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']  # Pongo las que voy a eliminar
for allm in m:  
    for allb in b:  
        data = pd.read_feather(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\Data_complete_roi.feather')
        data,covars = mapsDrop(data)
        title,data = select(data,allm,OneBand=allb,WithoutBand=None)
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
        # run harmonization and store the adjusted data
        my_model, my_data_adj = harmonizationLearn(my_data, covars)
        print(my_data_adj)
        nh=negativeTest(my_data_adj)
        datos_windex=data.reset_index()    
        new_data = pd.DataFrame(data=my_data_adj,columns=columnas)
        new_data['database']=database_col
        Biomarcadores,Duque,SRM,CHBMP = renameDatabases(new_data)

        for band in columnas:
            sns.kdeplot(Biomarcadores_eeg[band], color='darkcyan', label='Biomarcadores')
            sns.kdeplot(Duque_eeg[band], color='#708090', label='Duque')
            sns.kdeplot(SRM_eeg[band], color='lightgreen', label='SRM')
            sns.kdeplot(CHBMP_eeg[band], color='mediumblue', label='CHBMP')
            sns.kdeplot(Biomarcadores[band], color='darkcyan', label='Biomarcadores', linestyle='--')
            sns.kdeplot(Duque[band], color='#708090', label='Duque', linestyle='--')
            sns.kdeplot(SRM[band], color='lightgreen', label='SRM', linestyle='--')
            sns.kdeplot(CHBMP[band], color='mediumblue', label='CHBMP', linestyle='--')
            plt.title(f'# negatives - sovaharmony(-): {npp} and neuroHarmonize(--): {nh} ')
            plt.suptitle(title)
            plt.legend()
            #plt.show()
            if nh==0: 
                plt.savefig(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize\\SinNegativos\{name}_{title}_density.png'.format(name=band,title=title))
                plt.close()
            elif nh!=0:
                plt.savefig(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize\ConNegativos\{name}_{title}_density.png'.format(name=band,title=title))
                plt.close()