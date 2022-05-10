import os
import glob

name1 = ['_eeg','_stats']
name2 = ['[restEC]']
ext = ['.fif','.json','.txt']
path = None
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\derivatives\sovaharmony'
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM\derivatives\sovaharmony'
#path = r'D:\WEB\backend\filesSaved\SRM\derivatives\sovaharmony'
def remove_data(path,sub,v,name,ext):
#def remove_data(path,sub,name,ext):
    path_def = path+'\\'+sub+'\\'+v+'\\eeg\\*'+name2+name1+ext
    path_d = path+'\\'+sub+'\\'+v+'\\eeg\\*'+name1+ext
    #path_def = path+'\\'+sub+'\\eeg\\*'+name+ext
    if name2 in path_def:
        icpowers_json_files = glob.glob(path_d)
        #icpowers_json_files = glob.glob(path_def)
        json_remove.append(icpowers_json_files)
    return json_remove

subjects = os.listdir(path)
json_remove = []
for sub in subjects:
    suffix = "sub"
    if sub.endswith(suffix,0,3) == True:
        ses = os.listdir(path+'/'+sub)
        for v in ses:
            json_remove = remove_data(path,sub,v,name[1],ext[2])
        #json_remove = remove_data(path,sub,name[0],ext[1])
print(json_remove)

for i in json_remove:
     for j in range(0,2):
         try:
             print(i[j])
             os.remove(i[j])
         except:
          continue 
