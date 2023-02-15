from neuroHarmonize import harmonizationLearn
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def negativeTest(model):
    positivos = []
    negativos = []
    for row in model:
        positivos.extend(x for x in row if float(x) >= 0)
        negativos.extend(x for x in row if float(x) < 0)
    print('negativos: ',len(negativos))

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

data.drop(['participant_id','visit','condition','group'],axis=1,inplace=True)
data.drop(['MM_total','FAS_F','FAS_S','FAS_A','education'],axis=1,inplace=True)
columnas = data.columns
col = ['SITE','gender','age','participant_id','visit','condition','group','MM_total','FAS_F','FAS_S','FAS_A','education',]

covars = pd.DataFrame(covars)  

my_data = np.array(data)
# run harmonization and store the adjusted data
my_model, my_data_adj = harmonizationLearn(my_data, covars)
print(my_data_adj)
negativeTest(my_data_adj)
datos_windex=data.reset_index()    
#new_data=pd.concat([datos_windex.loc[:,col],pd.DataFrame(data=my_data_adj,columns=columnas)],axis=1)
new_data = pd.DataFrame(data=my_data_adj,columns=columnas)
new_data['database'] = database

Biomarcadores = new_data[new_data['database'] == 'BIOMARCADORES']
Duque = new_data[new_data['database'] == 'DUQUE']
SRM = new_data[new_data['database'] == 'SRM']
CHBMP = new_data[new_data['database'] == 'CHBMP']




sns.kdeplot(Biomarcadores['power_F_Delta'], color='black', label='Biomarcadores')
sns.kdeplot(SRM['power_F_Delta'], color='red', label='SRM')
plt.title('Con Combat - power_F_Delta')
plt.legend()
plt.show()