from graphics_QA import graphics
import pandas as pd 
import tkinter as tk
from tkinter.filedialog import askdirectory

tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
path = askdirectory() 
print("user chose", path, "for save graphs")

#data loading
data_ic=pd.read_feather(r'{path}\Data_long_complete_ic_sova_G1Control.feather'.format(path=path))
data_roi=pd.read_feather(r'{path}\Data_long_complete_roi_sova_G1Control.feather'.format(path=path))
# graphics connectivity and power in IC and ROI
colors=["#127369","#10403B","#8AA6A3","#45C4B0"]
#m = ['Coherence','Entropy','Power','SL']
m = ['Cross Frequency']
bands=list(data_roi.Band.unique())
bandsm=list(data_roi.M_Band.unique())
for met in m:
    if met!='Cross Frequency':
        for band in bands:
            graphics(data_ic,met,path,band,'IC',id_cross=None,num_columns=4,save=True,plot=False,kind='box',palette=colors)
            graphics(data_roi,met,path,band,'ROI',id_cross=None,num_columns=2,save=True,plot=False,kind='box',palette=colors)
    else:
        for band in bands:
            for mband in bandsm:
                try:
                    graphics(data_ic[data_ic['M_Band']==mband],met,path,band,'IC',id_cross=mband,num_columns=4,save=True,plot=False,kind='box',palette=colors)
                    graphics(data_roi[data_roi['M_Band']==mband],met,path,band,'ROI',id_cross=mband,num_columns=2,save=True,plot=False,kind='box',palette=colors)
                except:
                    pass
