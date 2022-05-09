import os
import glob

name = [']_eeg',']_stats','_powers','norm_eeg','norm_powers']
ext = ['.fif','.json','.txt']
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'
path=r'F:\BIOMARCADORES\derivatives\sovaharmony'
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM'
def remove_data(path,sub,v,name,ext):
    icpowers_json_files = glob.glob(path+'/'+sub+'/'+v+'\eeg/*'+name+ext)
    json_remove.append(icpowers_json_files)

subjects = os.listdir(path)
json_remove = []
for sub in subjects:
    suffix = "sub"
    if sub.endswith(suffix,0,3) == True:
        ses = os.listdir(path+'/'+sub)
        for v in ses:
            remove_data(path,sub,v,name[3],ext[0])
print(json_remove)

for i in json_remove:
     for j in range(0,2):
         try:
             print(i[j])
             os.remove(i[j])
         except:
          continue 

