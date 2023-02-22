import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from funtionsHarmonize import delcol 
from funtionsHarmonize import negativeTest


# path
data = pd.read_feather(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\Data_complete_roi.feather')
#data = pd.read_feather(r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\Data_complete_roi_con_atipicos.feather")
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
data = delcol(data,m,b,roi,bm)
data = delcol(data,['power'],bp,roi,bm)
####

data = data.reset_index(drop=True)    


Biomarcadores = data[data['database'] == 0.0]
Duque = data[data['database'] == 2.0]
SRM = data[data['database'] == 3.0]
CHBMP = data[data['database'] == 1.0]
Biomarcadores.drop(['database'],axis=1,inplace=True)
Duque.drop(['database'],axis=1,inplace=True)
SRM.drop(['database'],axis=1,inplace=True)
CHBMP.drop(['database'],axis=1,inplace=True)


nb=negativeTest(np.array(Biomarcadores))
nd=negativeTest(np.array(Duque))
ns=negativeTest(np.array(SRM))
nc=negativeTest(np.array(CHBMP))
n = nb+nd+ns+nc

for band in Biomarcadores.columns:
    sns.kdeplot(Biomarcadores[band], color='darkcyan', label='Biomarcadores')
    sns.kdeplot(Duque[band], color='darkslateblue', label='Duque')
    sns.kdeplot(SRM[band], color='lightgreen', label='SRM')
    sns.kdeplot(CHBMP[band], color='mediumblue', label='CHBMP')
    plt.title(band+' - pipeline eeg_harmonization - Sin atipicos')
    plt.annotate(f'Negativos: {n} ',xy=(-0.2, 11))
    plt.legend()
    #plt.savefig(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize\{name}_density.png'.format(name=band))
    #plt.close()