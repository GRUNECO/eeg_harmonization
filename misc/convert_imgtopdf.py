import os
import img2pdf
import itertools
import numpy as np

path = r'C:\Users\veroh\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD\Graficos_Tablas_All'
postprocessing = ['Coherence','Cross Frequency','Entropy','SL']
space = ['IC','ROI']
img = []
imagenes_png = []
#for features in postprocessing:
for s in space: 
    #for file in os.listdir(path+features+'/'+s):
    for file in os.listdir(path):
        if file.endswith("_table.png"):
            #imagenes_png.append(path+features+'/'+s+'/'+file)
            imagenes_png.append(path+'/'+file)
    #imagenes_png = [archivo for archivo in os.listdir(path+features+'/'+s) if archivo.endswith(".png")]
    img.append(imagenes_png)
imagenes=list(itertools.chain(*img))
with open(r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Resultados_Armonizacion_BD\Result_all.pdf", "wb") as documento:
    documento.write(img2pdf.convert(imagenes))