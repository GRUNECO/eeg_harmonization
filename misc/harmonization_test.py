from neuroHarmonize import harmonizationLearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from neuroHarmonize import loadHarmonizationModel
from scipy.stats import norm

# path
biomarcadores_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_powers_column_ROI_norm_BIOMARCADORES.feather"
duque_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resting_power_columns_ROI_DUQUE.feather"
srm_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resteyesc_power_columns_ROI_SRM.feather"
chbmp_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_protmap_power_columns_ROI_CHBMP.feather"
drop1 = ['subject', 'group','visit','condition','Study']
drop2 = ['participant_id', 'group','visit','condition','database']

def createModel(path,drop,control=None,replace=None):
    data = pd.read_feather(path)
    if not replace == None:
        data = data.replace({replace:'V0'})
    data= data[data['visit']=='V0']
    data= data[data['group']==control]
    data = data.drop(drop, axis=1)
    model = np.array(data)
    return model,data.columns

def negativeTest(name,model):
    positivos = []
    negativos = []
    for row in model:
        positivos.extend([x for x in row if x >= 0])
        negativos.extend([x for x in row if x < 0])
    print(name,' :',len(negativos))

Biomarcadores,Bands=createModel(biomarcadores_data,drop1,'CTR')
Duque,Bands=createModel(duque_data,drop2,'Control')
SRM,Bands=createModel(srm_data,drop2,'Control','t1')
CHBMP,Bands=createModel(chbmp_data,drop2,'Control')

negativeTest('Biomarcadores',Biomarcadores)
negativeTest('Duque',Duque)
negativeTest('SRM',SRM)
negativeTest('CHBMP',CHBMP)

for i,band in enumerate(Bands):
    sns.kdeplot(Biomarcadores[0], color='black', label='Biomarcadores')
    #sns.kdeplot(Duque[0], color='red', label='Duque')
    sns.kdeplot(SRM[0], color='red', label='SRM')
    #sns.kdeplot(CHBMP[0], color='blue', label='CHBMP')
    plt.title('Sin Combat - '+ band)
    plt.legend()
    plt.show()