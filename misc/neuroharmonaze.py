from neuroHarmonize import harmonizationLearn
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from funtionsHarmonize import delcol 
from funtionsHarmonize import negativeTest

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

covars = {'SITE':data['database'].to_numpy(),
          'gender':data['sex'].to_numpy(),
          'age':data['age'].to_numpy()}



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

#database_col = data['database'].reset_index(inplace=True)
database_col = np.array(data['database'])
data.drop(['database'],axis=1,inplace=True)
columnas = data.columns

col = ['SITE','gender','age','participant_id','visit','condition','group','MM_total','FAS_F','FAS_S','FAS_A','education',]

covars = pd.DataFrame(covars)  

my_data = np.array(data)
negativeTest(my_data)
# run harmonization and store the adjusted data
my_model, my_data_adj = harmonizationLearn(my_data, covars)
#data_combat = neuroCombat(dat=data['power_F_Delta'].to_numpy(),
#    covars=covars,
#    batch_col='SITE',
#    categorical_cols=col)["data"]

print(my_data_adj)
negativeTest(my_data_adj)
datos_windex=data.reset_index()    
#new_data=pd.concat([datos_windex.loc[:,col],pd.DataFrame(data=my_data_adj,columns=columnas)],axis=1)
new_data = pd.DataFrame(data=my_data_adj,columns=columnas)
new_data['database']=database_col

Biomarcadores = new_data[new_data['database'] == 0.0]
Duque = new_data[new_data['database'] == 2.0]
SRM = new_data[new_data['database'] == 3.0]
CHBMP = new_data[new_data['database'] == 1.0]

sns.kdeplot(Biomarcadores['power_F_Beta1'], color='black', label='Biomarcadores')
sns.kdeplot(Duque['power_F_Beta1'], color='g', label='Duque')
sns.kdeplot(SRM['power_F_Beta1'], color='r', label='SRM')
sns.kdeplot(CHBMP['power_F_Beta1'], color='b', label='CHBMP')
plt.title(+' - neuroHarmonize')
plt.legend()
plt.show()