import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_excel(r"C:\Users\user\Desktop\longitudinal_data_icpowers_avengers.xlsx",sheet_name="Sheet1")

all_columns = list(df.columns)
#derivatives = [x if '_r' in x for x in all_columns]
BANDS = {"Delta","Theta","Alpha-1","Alpha-2","Alpha","Beta","Gamma"}
GROUPS = {'G1', 'DCL', 'DTA', 'G2', 'CTR'}
TASKS = {'CE','OE'}
# Transversal Analysis
task = 
component = 15
visit = 'V1'
band = 'Alpha-2'
dft = df[df['visit']==visit]

dft.boxplot(column=['C'+str(component)+'_r'+band] ,by='group')
plt.show()

# Longitudinal Analysis
component = 15
band = 'Alpha-2'
dft = df[df['group']==group]
group = 'DCL'
dft.boxplot(column=['C'+str(component)+'_r'+band] ,by='visit')
plt.show()