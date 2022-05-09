import os
import glob

#name = [']_eeg',']_stats','_powers','norm_eeg','norm_powers']
name = '[restEC]'
name_end = ']_powers'
ext = ['.fif','.json','.txt']
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'
<<<<<<< HEAD
path=r'F:\BIOMARCADORES\derivatives\sovaharmony'
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM'
=======
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\derivatives\sovaharmony'
path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM\derivatives\sovaharmony'
>>>>>>> c5511851a053fc0a4cc48e384c8d5eeaf37f8c43
def remove_data(path,sub,v,name,ext):
#def remove_data(path,sub,name,ext):
    path_def = path+'\\'+sub+'\\'+v+'\\eeg\\'+name+ext
    #path_def = path+'\\'+sub+'\\eeg\\'+name+ext
    if name in path_def:
        icpowers_json_files = glob.glob(path+'\\'+sub+'\\'+v+'\\eeg\\*'+name_end+ext)
        json_remove.append(icpowers_json_files)
    return json_remove

subjects = os.listdir(path)
json_remove = []
for sub in subjects:
    suffix = "sub"
    if sub.endswith(suffix,0,3) == True:
        ses = os.listdir(path+'/'+sub)
        for v in ses:
<<<<<<< HEAD
            remove_data(path,sub,v,name[3],ext[0])
=======
            json_remove = remove_data(path,sub,v,name,ext[1])
        #json_remove = remove_data(path,sub,name,ext[1])
>>>>>>> c5511851a053fc0a4cc48e384c8d5eeaf37f8c43
print(json_remove)

for i in json_remove:
     for j in range(0,2):
         try:
             print(i[j])
             os.remove(i[j])
         except:
          continue 

