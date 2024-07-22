import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Ruta al archivo Excel
ruta_archivo = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_Paper\Datosparaorganizardataframes\Tamaño de efecto\tabla_effectsize_ic_G1.xlsx"

# Leer la hoja 'Power' en un DataFrame
df = pd.read_excel(ruta_archivo, sheet_name='Power')

# Filtrar las columnas que te interesan
columnas_interesantes = ['Component', 'Band', 'sova', 'neuro']
df_filtrado = df[columnas_interesantes]

# Calcular la diferencia entre los valores de 'sova' y 'neuro'
df_filtrado['Diferencia'] = df_filtrado['sova'] - df_filtrado['neuro']

# Obtener el valor absoluto máximo de las diferencias
max_abs_diff = abs(df_filtrado['Diferencia']).max()

# Reorganizar los datos para que las bandas estén en el orden deseado
band_order = ['Delta', 'Theta', 'Alpha-1', 'Alpha-2', 'Beta1', 'Beta2', 'Beta3', 'Gamma']
df_filtrado['Band'] = pd.Categorical(df_filtrado['Band'], categories=band_order, ordered=True)

# Usar pivot_table para reorganizar los datos
heatmap_data = df_filtrado.pivot_table(index='Component', columns='Band', values='Diferencia')

# Crear un heatmap de la diferencia centrado en 0
plt.figure(figsize=(10, 6))
heatmap = sns.heatmap(heatmap_data, annot=True, cmap = "seismic", fmt=".2f", center=0, vmin=-max_abs_diff, vmax=max_abs_diff)

# Configuración de etiquetas en el eje x
column_labels = ['Delta', 'Theta', 'Alpha1', 'Alpha2', 'Beta1', 'Beta2', 'Beta3', 'Gamma']
plt.xticks(np.arange(len(column_labels)) + 0.5, column_labels, rotation=45, ha='center')
plt.xlabel("Bands")

# Configuración de etiquetas
plt.title("Difference sovaHarmony - neuroHarmonize (Control Group)")
plt.xticks(rotation=0)
plt.yticks(rotation=0)

# Mostrar el heatmap
plt.show()




# Ruta al archivo Excel
ruta_archivo = r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Articulo análisis longitudinal\Resultados_Armonizacion_Paper\Datosparaorganizardataframes\Tamaño de efecto\tabla_effectsize_ic_G1.xlsx"

# Leer la hoja 'Power' en un DataFrame
df = pd.read_excel(ruta_archivo, sheet_name='Power')

# Cambiar el orden de las columnas en el DataFrame
column_order = ['Component', 'Band', 'neuro', 'sova']
df_filtrado = df[column_order]

# Usar pivot_table para reorganizar los datos
heatmap_data = df_filtrado.pivot_table(index='Component', columns='Band', values=['sova'])

# Crear un heatmap
plt.figure(figsize=(10, 6))
heatmap = sns.heatmap(heatmap_data, annot=True, cmap = "seismic", fmt=".2f")

# Configuración de etiquetas en el eje x
#column_labels = [f"{col[1]}-{col[0]}" for col in heatmap_data.columns]
column_labels = ['Delta', 'Theta', 'Alpha-1', 'Alpha-2', 'Beta1', 'Beta2', 'Beta3', 'Gamma']
plt.xticks(range(len(column_labels)), column_labels, rotation=45)
plt.xlabel("Bands")

# Configuración de etiquetas en el eje y y título
plt.yticks(rotation=0)
plt.ylabel("Component")
plt.title("Effect Size (Sova)")

# Mostrar el heatmap
plt.show()

