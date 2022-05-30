import pandas as pd
import numpy as np

participant = pd.read_csv(r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\participants.tsv', sep='\t')#,index_col='participant_id')
G1 = participant[participant['participant_id'].str.contains("sub-G1", case=False)]
G2 = participant[participant['participant_id'].str.contains("sub-G2", case=False)]
G1.join(G2, lsuffix='G1', rsuffix='G2')
G1_G2 = pd.concat([G1, G2])

G1['age']=G1['age'].mask(G1['age'].eq('None'))
G2['age']=G2['age'].mask(G2['age'].eq('None'))
G1_G2['age']=G1_G2['age'].mask(G1_G2['age'].eq('None'))


min=G1_G2['age'].dropna().min()
max=G1_G2['age'].dropna().max()
print('Rango G1+G2: ',min,'-',max)


min=G1['age'].dropna().min()
max=G1['age'].dropna().max()
print('Rango G1: ',min,'-',max)


min=G2['age'].dropna().min()
max=G2['age'].dropna().max()
print('Rango G2: ',min,'-',max)


