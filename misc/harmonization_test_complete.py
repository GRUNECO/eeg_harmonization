import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from funtionsHarmonize import delcol 
from funtionsHarmonize import negativeTest
from funtionsHarmonize import createModel

# path
data = pd.read_feather(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\Data_complete_roi.feather')
databases = {label:float(idx) for idx,label in enumerate(np.unique(data['database']))}
print(databases)
group = {label:float(idx) for idx,label in enumerate(np.unique(data['group']))}
print(group)
gender = {label:float(idx) for idx,label in enumerate(np.unique(data['sex']))}
print(gender)

data.loc[:,'group'] = data.loc[:,'group'].map(group)
data.loc[:,'sex'] = data.loc[:,'sex'].map(gender)
data = data[data['group'] == 0.0]
database = data['database']
data.loc[:,'database'] = data.loc[:,'database'].map(databases) 
data.drop(['participant_id','visit','condition','group','sex','age'],axis=1,inplace=True)
data.drop(['MM_total','FAS_F','FAS_S','FAS_A','education'],axis=1,inplace=True)

####
m = ['sl','cohfreq','entropy','crossfreq']
b = ['Delta','Theta','Alpha-1','Alpha-2','Beta1','Beta2','Beta3','Gamma']
bp = ['Delta','Theta','Alpha-1','Alpha-2','Gamma']
bm = ['Mdelta','Mtheta','Malpha-1','Malpha-2','Mbeta1','Mbeta2','Mbeta3','Mgamma']
roi = ['F','C','T','PO']
data = delcol(data,m,b,bm,roi)
data = delcol(data,['power'],bp,bm,roi)
####

Biomarcadores = data[data['database'] == 0.0]
Duque = data[data['database'] == 2.0]
SRM = data[data['database'] == 3.0]
CHBMP = data[data['database'] == 1.0]
data.drop(['database'],axis=1,inplace=True)

#biomarcadores_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_CE_crossfreq_columns_ROI_BIOMARCADORES.feather"
#duque_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resting_crossfreq_columns_ROI_DUQUE.feather"
#srm_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resteyesc_crossfreq_columns_ROI_SRM.feather"
#chbmp_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_protmap_crossfreq_columns_ROI_CHBMP.feather"
#drop1 = ['subject', 'group','visit','condition','Study']
#drop2 = ['participant_id', 'group','visit','condition','database']
#Biomarcadores,Bands=createModel(biomarcadores_data,drop2,'CTR') #drop1 para power y drop2 para las demas
#Duque,Bands=createModel(duque_data,drop2,'Control')
#SRM,Bands=createModel(srm_data,drop2,'Control','t1')
#CHBMP,Bands=createModel(chbmp_data,drop2,'Control')


negativeTest(np.array(Biomarcadores))
negativeTest(np.array(Duque))
negativeTest(np.array(SRM))
negativeTest(np.array(CHBMP))

for i,band in enumerate(Biomarcadores.columns):
    sns.kdeplot(Biomarcadores[band], color='black', label='Biomarcadores')
    sns.kdeplot(Duque[band], color='g', label='Duque')
    sns.kdeplot(SRM[band], color='r', label='SRM')
    sns.kdeplot(CHBMP[band], color='b', label='CHBMP')
    plt.title(str(band)+' - Pipeline eeg_harmonization')
    plt.legend()
    #plt.savefig(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize\{name}_density.png'.format(name=band))
    #plt.close()