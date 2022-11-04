from combat.pycombat import pycombat

data = r'E:\Academico\Universidad\Posgrado\Tesis\Paquetes\Data_analysis_ML_Harmonization_Proyect\Manipulacion- Rois-Componentes de todas las DB\Datosparaorganizardataframes\BasesdeDatosFiltradas_componenteporcolumnas_sin_atipicos.feather'
batch = ['Power','Coherence','SL','Entropy','PME']
data_corrected = pycombat(data,batch)