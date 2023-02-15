from neuroCombat import neuroCombat
import pandas as pd
import numpy as np

# Getting example data
# 200 rows (features) and 10 columns (scans)
data = pd.read_feather(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\Data_complete_roi.feather')

databases = {label:float(idx) for idx,label in enumerate(np.unique(data['database']))}
print(databases)
group = {label:float(idx) for idx,label in enumerate(np.unique(data['group']))}
print(group)
gender = {label:float(idx) for idx,label in enumerate(np.unique(data['sex']))}
print(gender)
data.loc[:,'database'] = data.loc[:,'database'].map(databases) 
data.loc[:,'group'] = data.loc[:,'group'].map(group)
data.loc[:,'sex'] = data.loc[:,'sex'].map(gender)
data.drop(['participant_id','visit','condition'],axis=1,inplace=True)
data.drop(['MM_total','FAS_F','FAS_S','FAS_A','education'],axis=1,inplace=True)
data.rename(columns = {'database':'batch'},inplace=True)
# Specifying the batch (scanner variable) as well as a biological covariate to preserve:
covars = {'batch':data['batch'].to_numpy(),
          'gender':data['sex'].to_numpy(),
          'group':data['group'].to_numpy(),
          'age':data['age'].to_numpy()}
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
#covars.reset_index(drop = True , inplace = True)
#data.reset_index(drop = True , inplace = True)
#Harmonization step:
data_combat = neuroCombat(dat=data['power_F_Delta'].to_numpy(),
    covars=covars,
    batch_col=batch_col,
    categorical_cols=categorical_cols)["data"]