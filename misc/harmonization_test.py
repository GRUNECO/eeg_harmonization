import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# path
biomarcadores_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_CE_entropy_columns_ROI_BIOMARCADORES.feather"
duque_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resting_entropy_columns_ROI_DUQUE.feather"
srm_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resteyesc_entropy_columns_ROI_SRM.feather"
chbmp_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_protmap_entropy_columns_ROI_CHBMP.feather"
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

Biomarcadores,Bands=createModel(biomarcadores_data,drop2,'CTR') #drop1 para power y drop2 para las demas
Duque,Bands=createModel(duque_data,drop2,'Control')
SRM,Bands=createModel(srm_data,drop2,'Control','t1')
CHBMP,Bands=createModel(chbmp_data,drop2,'Control')

negativeTest('Biomarcadores',Biomarcadores)
negativeTest('Duque',Duque)
negativeTest('SRM',SRM)
negativeTest('CHBMP',CHBMP)

for i,band in enumerate(Bands):
    sns.kdeplot(Biomarcadores[i], color='black', label='Biomarcadores')
    sns.kdeplot(Duque[i], color='g', label='Duque')
    sns.kdeplot(SRM[i], color='r', label='SRM')
    sns.kdeplot(CHBMP[i], color='b', label='CHBMP')
    plt.title(str(band)+' - Pipeline eeg_harmonization')
    plt.legend()
    plt.savefig(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize\{name}_density.png'.format(name=band))
    plt.close()