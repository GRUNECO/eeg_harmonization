import pandas as pd
import numpy as np

participant = pd.read_csv(r'D:\TDG\filesSaved\BIOMARCADORES_TEST\participants.tsv', sep='\t')#,index_col='participant_id')
G1 = participant[participant['participant_id'].str.contains("sub-G1", case=False)]
G2 = participant[participant['participant_id'].str.contains("sub-G2", case=False)]
CTR = participant[participant['participant_id'].str.contains("sub-CTR", case=False)]
G1.join(G2, lsuffix='G1', rsuffix='G2')
G2.join(CTR, lsuffix='G2', rsuffix='CTR')
G1_G2 = pd.concat([G1, G2])
CTR_G2 = pd.concat([CTR, G2])

G1['age']=G1['age'].mask(G1['age'].eq('None'))
G2['age']=G2['age'].mask(G2['age'].eq('None'))
G1_G2['age']=G1_G2['age'].mask(G1_G2['age'].eq('None'))
CTR_G2['age']=CTR_G2['age'].mask(CTR_G2['age'].eq('None'))

print('RANGO G2+CTR: ',CTR_G2['age'].dropna().min(),CTR_G2['age'].dropna().max())

x=CTR_G2['age'].dropna().tolist()
b= [float(i) for i in x]
print('mean G2+CTR: ',np.mean(b),np.std(b))
min=G1_G2['age'].dropna().min()
max=G1_G2['age'].dropna().max()
print('Rango G1+G2: ',min,'-',max)


min=G1['age'].dropna().min()
max=G1['age'].dropna().max()
print('Rango G1: ',min,'-',max)


min=G2['age'].dropna().min()
max=G2['age'].dropna().max()
print('Rango G2: ',min,'-',max)


