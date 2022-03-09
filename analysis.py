import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_excel(r"E:\Academico\Universidad\Posgrado\Tesis\Datos\longitudinal_data_icpowers_avengers.xlsx",sheet_name="Sheet1")

ALL_COLUMNS = list(df.columns)
DERIVATIVES = set([x  for x in ALL_COLUMNS if '_r' in x])
VARIABLES = set([x  for x in ALL_COLUMNS if '_r' not in x and 'Unnamed' not in x])
BANDS = set([x.split('_r')[1] for x in DERIVATIVES])
GROUPS = set(df.group)
TASKS = set(df.condition)
SESSIONS = set(df.visit)

for v in VARIABLES:
    print('*'*100)
    print(v)
    print(set(df[v]))

print('*'*100)
print('BANDS')
print(BANDS)

# Transversal Analysis
task = 'CE'
component = 15
visit = 'V1'
band = 'Beta'
dft = df[df['visit']==visit]
dft = dft[dft['condition']==task]
dft.boxplot(column=['C'+str(component)+'_r'+band] ,by='group')
plt.show()

# Longitudinal Analysis
component = 15
group = 'DCL'

dfl = df[df['group']==group]
dfl = dfl[dfl['condition']==task]
dfl.boxplot(column=['C'+str(component)+'_r'+band] ,by='visit')
plt.show()