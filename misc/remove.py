import os
import glob


path = r'D:\BASESDEDATOS\CHBMP\derivatives\sovaharmony'
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\BIOMARCADORES_BIDS\derivatives\sovaharmony'
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\CHBMP\derivatives\sovaharmony'
#path = r'E:\Academico\Universidad\Posgrado\Tesis\Datos\BASESDEDATOS\SRM\derivatives\sovaharmony'
#path = r'D:\WEB\backend\filesSaved\SRM\derivatives\sovaharmony'
name = [']_eeg',']_stats','_powers','norm_eeg','norm_powers']
ext = ['.fif','.json','.txt']

#def remove_data(path,sub,v,name,ext): #con visitas
def remove_data(path,sub,name,ext): #Sin visitas
    #path_def = path+'\\'+sub+'\\'+v+'\\eeg\\'+name+ext #Con visitas
    
    path_def = path+'\\'+sub+'\\eeg\\'+name+ext #sin visitas
    if name in path_def:
        
        
        #icpowers_json_files = glob.glob(path+'\\'+sub+'\\'+v+'\\eeg\\*'+name+ext)#Con visitas
        icpowers_json_files = glob.glob(path+'\\'+sub+'\\eeg\\*'+name+ext)#sin visitas
        print(path+'\\'+sub+'\\eeg\\*'+name+ext)
        json_remove.append(icpowers_json_files)
    return json_remove



subjects = os.listdir(path)
json_remove = []
# for sub in subjects:# for con visitas
#     suffix = "sub"
#     if sub.endswith(suffix,0,3) == True:
#         ses = os.listdir(path+'/'+sub)
#         for v in ses:
#             json_remove = remove_data(path,sub,v,name[2],ext[0])
#             #json_remove = remove_data(path,sub,v,name[1],ext[1])
#             #json_remove = remove_data(path,sub,v,name[1],ext[2])
# print(json_remove)

for sub in subjects:#For sin visitas
    suffix = "sub"
    if sub.endswith(suffix,0,3) == True:
        #ses = os.listdir(path+'/'+sub)
        
        json_remove = remove_data(path,sub,name[2],ext[1])
            #json_remove = remove_data(path,sub,v,name[1],ext[1])
            #json_remove = remove_data(path,sub,v,name[1],ext[2])
print(json_remove)

for i in json_remove:
     for j in range(0,2):
         try:
             print(i[j])
             os.remove(i[j])
         except:
          continue