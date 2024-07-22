
import pandas as pd
import numpy as np

path_feather = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Verónica Henao Isaza\Resultados\dataframes'
data_in = pd.read_feather(path_feather+r'\Data_complete_ic.feather')

CTR_in=data_in[data_in['group']=='Control']
CTR_VO = CTR_in[( CTR_in['visit'] == 'V0') | ( CTR_in['visit'] == 't1')]
print('CTR: ',CTR_VO.shape)
CTR_VO_medad = CTR_VO['age'].mean()
print('CTR-mean-age: ',CTR_VO_medad)
CTR_VO_sedad = CTR_VO['age'].std()
print('CTR-std-age: ',CTR_VO_sedad)
CTR_VO_F = CTR_VO[CTR_VO['sex']=='F']
print('CTR-F: ',CTR_VO_F.shape)
CTR_VO_M = CTR_VO[CTR_VO['sex']=='M']
print('CTR-M: ',CTR_VO_M.shape)

CTR_VO_B = CTR_VO[CTR_VO['database'] == 'BIOMARCADORES']
print('CTR-Biomarcadores: ',CTR_VO_B.shape)
CTR_VO_B_medad = CTR_VO_B['age'].mean()
print('CTR-Biomarcadores-mean-age: ',CTR_VO_B_medad)
CTR_VO_B_sedad = CTR_VO_B['age'].std()
print('CTR-Biomarcadores-std-age: ',CTR_VO_B_sedad)
CTR_VO_B_F = CTR_VO_B[CTR_VO_B['sex']=='F']
print('CTR-Biomarcadores-F: ',CTR_VO_B_F.shape)
CTR_VO_B_M = CTR_VO_B[CTR_VO_B['sex']=='M']
print('CTR-Biomarcadores-M: ',CTR_VO_B_M.shape)

CTR_VO_D = CTR_VO[CTR_VO['database'] == 'DUQUE']
print('CTR-Duque: ',CTR_VO_D.shape)
CTR_VO_D_medad = CTR_VO_D['age'].mean()
print('CTR-Duque-mean-age: ',CTR_VO_D_medad)
CTR_VO_D_sedad = CTR_VO_D['age'].std()
print('CTR-Duque-std-age: ',CTR_VO_D_sedad)
CTR_VO_D_F = CTR_VO_D[CTR_VO_D['sex']=='F']
print('CTR-Duque-F: ',CTR_VO_D_F.shape)
CTR_VO_D_M = CTR_VO_D[CTR_VO_D['sex']=='M']
print('CTR-Duque-M: ',CTR_VO_D_M.shape)

CTR_VO_S = CTR_VO[CTR_VO['database'] == 'SRM']
print('CTR-SRM: ',CTR_VO_S.shape)
CTR_VO_S_medad = CTR_VO_S['age'].mean()
print('CTR-SRM-mean-age: ',CTR_VO_S_medad)
CTR_VO_S_sedad = CTR_VO_S['age'].std()
print('CTR-SRM-std-age: ',CTR_VO_S_sedad)
CTR_VO_S_F = CTR_VO_S[CTR_VO_S['sex']=='F']
print('CTR-SRM-F: ',CTR_VO_S_F.shape)
CTR_VO_S_M = CTR_VO_S[CTR_VO_S['sex']=='M']
print('CTR-SRM-M: ',CTR_VO_S_M.shape)


CTR_VO_C = CTR_VO[CTR_VO['database'] == 'CHBMP']
print('CTR-CHBMP: ',CTR_VO_C.shape)
CTR_VO_C_medad = CTR_VO_C['age'].mean()
print('CTR-CHBMP-mean-age: ',CTR_VO_C_medad)
CTR_VO_C_sedad = CTR_VO_C['age'].std()
print('CTR-CHBMP-std-age: ',CTR_VO_C_sedad)
CTR_VO_C_F = CTR_VO_C[CTR_VO_C['sex']=='F']
print('CTR-CHBMP-F: ',CTR_VO_C_F.shape)
CTR_VO_C_M = CTR_VO_C[CTR_VO_C['sex']=='M']
print('CTR-CHBMP-M: ',CTR_VO_C_M.shape)

G1_in=data_in[data_in['group']=='G1']
G1_VO = G1_in[( G1_in['visit'] == 'V0') | ( G1_in['visit'] == 't1')]
print('G1_VO: ',G1_VO.shape)
G1_VO_medad = G1_VO['age'].mean()
print('G1_VO-mean-age: ',G1_VO_medad)
G1_VO_sedad = G1_VO['age'].std()
print('G1_VO-std-age: ',G1_VO_sedad)
G1_VO_F = G1_VO[G1_VO['sex']=='F']
print('G1_VO-F: ',G1_VO_F.shape)
G1_VO_M = G1_VO[G1_VO['sex']=='M']
print('G1_VO-M: ',G1_VO_M.shape)

G1_VO_B = G1_VO[G1_VO['database'] == 'BIOMARCADORES']
print('G1-Biomarcadores: ',G1_VO_B.shape)
G1_VO_B_medad = G1_VO_B['age'].mean()
print('G1-Biomarcadores-mean-age: ',G1_VO_B_medad)
G1_VO_B_sedad = G1_VO_B['age'].std()
print('G1-Biomarcadores-std-age: ',G1_VO_B_sedad)
G1_VO_B_F = G1_VO_B[G1_VO_B['sex']=='F']
print('G1-Biomarcadores-F: ',G1_VO_B_F.shape)
G1_VO_B_M = G1_VO_B[G1_VO_B['sex']=='M']
print('G1-Biomarcadores-M: ',G1_VO_B_M.shape)

G1_VO_D = G1_VO[G1_VO['database'] == 'DUQUE']
print('G1-Duque: ',G1_VO_D.shape)
G1_VO_D_medad = G1_VO_D['age'].mean()
print('G1-Duque-mean-age: ',G1_VO_D_medad)
G1_VO_D_sedad = G1_VO_D['age'].std()
print('G1-Duque-std-age: ',G1_VO_D_sedad)
G1_VO_D_F = G1_VO_D[G1_VO_D['sex']=='F']
print('G1-Duque-F: ',G1_VO_D_F.shape)
G1_VO_D_M = G1_VO_D[G1_VO_D['sex']=='M']
print('G1-Duque-M: ',G1_VO_D_M.shape)

G2_in=data_in[data_in['group']=='G2']
G2_VO = G2_in[( G2_in['visit'] == 'V0') | ( G2_in['visit'] == 't1')]
print('G2_VO: ',G2_VO.shape)
G2_VO_medad = G2_VO['age'].mean()
print('G2_VO-mean-age: ',G2_VO_medad)
G2_VO_sedad = G2_VO['age'].std()
print('G2_VO-std-age: ',G2_VO_sedad)
G2_VO_F = G2_VO[G2_VO['sex']=='F']
print('G2_VO-F: ',G2_VO_F.shape)
G2_VO_M = G2_VO[G2_VO['sex']=='M']
print('G2_VO-M: ',G2_VO_M.shape)


G2_VO_B = G2_VO[G2_VO['database'] == 'BIOMARCADORES']
print('G2-Biomarcadores: ',G2_VO_B.shape)
G2_VO_B_medad = G2_VO_B['age'].mean()
print('G2-Biomarcadores-mean-age: ',G2_VO_B_medad)
G2_VO_B_sedad = G2_VO_B['age'].std()
print('G2-Biomarcadores-std-age: ',G2_VO_B_sedad)
G2_VO_B_F = G2_VO_B[G2_VO_B['sex']=='F']
print('G2-Biomarcadores-F: ',G2_VO_B_F.shape)
G2_VO_B_M = G2_VO_B[G2_VO_B['sex']=='M']
print('G2-Biomarcadores-M: ',G2_VO_B_M.shape)

G2_VO_D = G2_VO[G2_VO['database'] == 'DUQUE']
print('G2-Duque: ',G2_VO_D.shape)
G2_VO_D_medad = G2_VO_D['age'].mean()
print('G2-Duque-mean-age: ',G2_VO_D_medad)
G2_VO_D_sedad = G2_VO_D['age'].std()
print('G2-Duque-std-age: ',G2_VO_D_sedad)
G2_VO_D_F = G2_VO_D[G2_VO_D['sex']=='F']
print('G2-Duque-F: ',G2_VO_D_F.shape)
G2_VO_D_M = G2_VO_D[G2_VO_D['sex']=='M']
print('G2-Duque-M: ',G2_VO_D_M.shape)
