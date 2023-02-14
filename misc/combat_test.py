from neuroCombat import neuroCombat
import pandas as pd
import numpy as np

# Getting example data
# 200 rows (features) and 10 columns (scans)
data = pd.read_feather(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD\Datosparaorganizardataframes\Data_complete_roi.feather')

databases = {label:idx for idx,label in enumerate(np.unique(data['database']))}
print(databases)
group = {label:idx for idx,label in enumerate(np.unique(data['group']))}
print(group)
gender = {label:idx for idx,label in enumerate(np.unique(data['sex']))}
print(gender)
data.loc[:,'database'] = data.loc[:,'database'].map(databases) 
data.loc[:,'group'] = data.loc[:,'group'].map(group)
data.loc[:,'sex'] = data.loc[:,'sex'].map(gender)
data.drop(['participant_id'],axis=1,inplace=True)
data.drop(['visit'],axis=1,inplace=True)
data.drop(['condition'],axis=1,inplace=True)

data.drop(['MM_total'],axis=1,inplace=True)
data.drop(['FAS_F'],axis=1,inplace=True)
data.drop(['FAS_S'],axis=1,inplace=True)
data.drop(['FAS_A'],axis=1,inplace=True)
data.drop(['education'],axis=1,inplace=True)
# Specifying the batch (scanner variable) as well as a biological covariate to preserve:
covars = {'batch':data['database'].values,
          'gender':data['sex'].values,
          'group':data['group'].values,
          'age':data['age'].values}
          #'education':data['education'].values
          #'MM':data['MM_total'],
          #'FAS_F':data['FAS_F'],
          #'FAS_S':data['FAS_S'],
          #'FAS_A':data['FAS_A']} 
covars = pd.DataFrame(covars)  

# To specify names of the variables that are categorical:
categorical_cols = ['gender','group']

# To specify the name of the variable that encodes for the scanner/batch covariate:
batch_col = 'batch'

#Harmonization step:
data_combat = neuroCombat(dat=data,
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols)["data"]