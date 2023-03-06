import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from funtionsHarmonize import delcol 
from funtionsHarmonize import negativeTest
from funtionsHarmonize import createModel

# path
biomarcadores_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_CE_power_columns_ROI_BIOMARCADORES.feather"
duque_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resting_power_columns_ROI_DUQUE.feather"
srm_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_resteyesc_power_columns_ROI_SRM.feather"
chbmp_data = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Datosparaorganizardataframes\data_protmap_power_columns_ROI_CHBMP.feather"
drop1 = ['subject', 'group','visit','condition','Study']
drop2 = ['participant_id', 'group','visit','condition','database']


Biomarcadores,Bands=createModel(biomarcadores_data,drop2,'CTR') #drop1 para power y drop2 para las demas
Duque,Bands=createModel(duque_data,drop2,'Control')
SRM,Bands=createModel(srm_data,drop2,'Control','t1')
CHBMP,Bands=createModel(chbmp_data,drop2,'Control')

negativeTest(Biomarcadores)
negativeTest(Duque)
negativeTest(SRM)
negativeTest(CHBMP)

for i,band in enumerate(Bands):
    sns.kdeplot(Biomarcadores[i], color='black', label='Biomarcadores')
    sns.kdeplot(Duque[i], color='g', label='Duque')
    sns.kdeplot(SRM[i], color='r', label='SRM')
    sns.kdeplot(CHBMP[i], color='b', label='CHBMP')
    plt.title(str(band)+' - Pipeline eeg_harmonization')
    plt.legend()
    plt.show()
    #plt.savefig(r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_BD\Graficos_Harmonize\{name}_density.png'.format(name=band))
    plt.close()