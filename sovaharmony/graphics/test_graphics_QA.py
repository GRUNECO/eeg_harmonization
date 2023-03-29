import pandas as pd 
from graphics_QA import create_check
from graphics_QA import stats_pair
from graphics_QA import graphics
from graphics_QA import table_groups_DB

path=r'C:\Users\Victoria\OneDrive - Universidad de Antioquia\GRUNECO\Doctorado Ximena\QA' #Cambia dependieron de quien lo corra

#data loading
data_p_roi=pd.read_feather(r'{path}\derivatives\data_long_power_roi_without_oitliers.feather'.format(path=path))
data_p_com=pd.read_feather(r'{path}\derivatives\data_long_power_components_without_oitliers.feather'.format(path=path))
data_sl_roi=pd.read_feather(r'{path}\derivatives\data_long_sl_roi.feather'.format(path=path))
data_sl_com=pd.read_feather(r'{path}\derivatives\data_long_sl_components.feather'.format(path=path))
data_c_roi=pd.read_feather(r'{path}\derivatives\data_long_coherence_roi.feather'.format(path=path))
data_c_com=pd.read_feather(r'{path}\derivatives\data_long_coherence_components.feather'.format(path=path))
data_e_roi=pd.read_feather(r'{path}\derivatives\data_long_entropy_roi.feather'.format(path=path))
data_e_com=pd.read_feather(r'{path}\derivatives\data_long_entropy_components.feather'.format(path=path))
data_cr_roi=pd.read_feather(r'{path}\derivatives\data_long_crossfreq_roi.feather'.format(path=path))
data_cr_com=pd.read_feather(r'{path}\derivatives\data_long_crossfreq_components.feather'.format(path=path))

datos_roi={'Power':data_p_roi,'SL':data_sl_roi,'Coherence':data_c_roi,'Entropy':data_e_roi,'Cross Frequency':data_cr_roi}
datos_com={'Power':data_p_com,'SL':data_sl_com,'Coherence':data_c_com,'Entropy':data_e_com,'Cross Frequency':data_cr_com}

bands= data_sl_com['Band'].unique()
bandsm= data_cr_com['M_Band'].unique()

matrix_roi=pd.DataFrame(columns=['group', 'ROI', 'A', 'B', 'cv', 'effect size', 'space', 'state','band','mband', 'metric'])
matrix_com=pd.DataFrame(columns=['group', 'Component', 'A', 'B', 'cv', 'effect size', 'space', 'state','band','mband', 'metric'])


for metric in datos_roi.keys():
    for band in bands:
        d_roi=datos_roi[metric]
        d_banda_roi=d_roi[d_roi['Band']==band]
        d_com=datos_com[metric]
        d_banda_com=d_com[d_com['Band']==band]
        if metric!='Cross Frequency':  
            print(str(band)+' '+str(metric)) 
            table_roi,save_roi=stats_pair(d_banda_roi,metric,'ROI',path,band,'ROI')
            check_roi=create_check(save_roi,'ROI',band,metric,'different',None)
            table_com,save_com=stats_pair(d_banda_com,metric,'Component',path,band,'IC') 
            check_com=create_check(save_com,'Component',band,metric,'different',None)
            path_roi=graphics(d_banda_roi,metric,path,band,'ROI',num_columns=2,save=True,plot=False)
            path_com=graphics(d_banda_com,metric,path,band,'IC',num_columns=4,save=True,plot=False)
            tg_roi,save_tg_roi=table_groups_DB(d_banda_roi,metric,'ROI',path,band,'ROI',id_cross=None)
            check_tg_roi=create_check(save_tg_roi,'ROI',band,metric,'equal',None)
            tg_com,save_tg_com=table_groups_DB(d_banda_com,metric,'Component',path,band,'IC',id_cross=None)
            check_tg_com=create_check(save_tg_com,'Component',band,metric,'equal',None)
            # joinimages([path_roi,table_roi,tg_roi])
            # joinimages([path_com,table_com,tg_com])
            # os.remove(tg_roi)
            # os.remove(tg_com)
            matrix_roi = matrix_roi.append(check_roi, ignore_index = True)
            matrix_com = matrix_com.append(check_com, ignore_index = True)
            matrix_roi = matrix_roi.append(check_tg_roi, ignore_index = True)
            matrix_com = matrix_com.append(check_tg_com, ignore_index = True)
            
        else:
            for bandm in bandsm:  
                print(str(band)+' '+str(metric)+' '+str(bandm)) 
                if d_banda_roi[d_banda_roi['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
                    table_roi,save_roi=stats_pair(d_banda_roi[d_banda_roi['M_Band']==bandm],metric,'ROI',path,band,'ROI',id_cross=bandm)
                    check_roi=create_check(save_roi,'ROI',band,metric,'different',bandm)
                    path_roi=graphics(d_banda_roi[d_banda_roi['M_Band']==bandm],'Cross Frequency',path,band,'ROI',id_cross=bandm,num_columns=2,save=True,plot=False)
                    tg_roi,save_tg_roi=table_groups_DB(d_banda_roi[d_banda_roi['M_Band']==bandm],metric,'ROI',path,band,'ROI',id_cross=bandm)
                    check_tg_roi=create_check(save_tg_roi,'ROI',band,metric,'equal',bandm)
                    # joinimages([path_roi,table_roi,tg_roi])    
                    # os.remove(tg_roi)
                    matrix_roi = matrix_roi.append(check_roi, ignore_index = True)
                    matrix_roi = matrix_roi.append(check_tg_roi, ignore_index = True)
                   
                if d_banda_com[d_banda_com['M_Band']==bandm]['Cross Frequency'].iloc[0]!=0:
                    table_com,save_com=stats_pair(d_banda_com[d_banda_com['M_Band']==bandm],metric,'Component',path,band,'IC',id_cross=bandm) 
                    check_com=create_check(save_com,'Component',band,metric,'different',bandm)
                    path_com=graphics(d_banda_com[d_banda_com['M_Band']==bandm],'Cross Frequency',path,band,'IC',id_cross=bandm,num_columns=4,save=True,plot=False)
                    tg_com,save_tg_com=table_groups_DB(d_banda_com[d_banda_com['M_Band']==bandm],metric,'Component',path,band,'IC',id_cross=bandm)
                    check_tg_com=create_check(save_tg_com,'Component',band,metric,'equal',bandm)
                    # joinimages([path_com,table_com,tg_com])
                    # os.remove(tg_com) 
                    matrix_com = matrix_com.append(check_com, ignore_index = True)
                    matrix_com = matrix_com.append(check_tg_com, ignore_index = True)   

print('table lista')
matrix_com['Compared groups']=matrix_com['A']+'-'+matrix_com['B']
matrix_roi['Compared groups']=matrix_roi['A']+'-'+matrix_roi['B']
filename = r"{path}\check_sin_cv.xlsx".format(path=path)
writer = pd.ExcelWriter(filename)
matrix_com.to_excel(writer ,sheet_name='Component')
matrix_roi.to_excel(writer ,sheet_name='ROI')
writer.save()
writer.close()              
print('Graficos SL,coherencia,entropia y cross frequency guardados')