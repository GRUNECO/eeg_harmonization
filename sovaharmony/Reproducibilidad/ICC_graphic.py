import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import os

os.path.isfile(r'E:\Academico\Universidad\Posgrado\Tesis\Paquetes\eeg_harmonization\sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_Components_G1-G2.csv')
icc_data_Roi=pd.read_csv(r'E:\Academico\Universidad\Posgrado\Tesis\Paquetes\eeg_harmonization\sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_ROIS_G2-CTR.csv',sep=';')
icc_data_Comp=pd.read_csv(r'E:\Academico\Universidad\Posgrado\Tesis\Paquetes\eeg_harmonization\sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_Components_G1-G2.csv',sep=';')


def barplot_icc_nB_1G(icc_data,x_value,group,plot=False,save=False):
    filter_band=icc_data[icc_data['Group']==group]
    sns.set(font_scale = 0.9)
    sns.set_theme(style="white")
    ax=sns.catplot(x=x_value,y='ICC',data=filter_band,hue='Stage',palette='winter_r',kind='bar',col='Bands',col_wrap=4,legend=False, ci=True, capsize=.2)
     #ax.despine(left=True)
    ax.fig.suptitle('ICC3k for '+ x_value +' in frequency bands of '+group+' group')
    ax.add_legend(loc='upper center',bbox_to_anchor=(.5,0.94),ncol=2)
    ax.fig.subplots_adjust(top=0.829,bottom=0.133, right=0.936,left=0.062, hspace=0.143, wspace=0.11) # adjust the Figure in rp
    ax.set(xlabel=None)
    ax.set(ylabel=None)
    ax.fig.text(0.5, 0.07, x_value, ha='center', va='center')
    ax.fig.text(0.03, 0.5,  'ICC', ha='center', va='center',rotation='vertical')
    # iterate through axes
    for axs in ax.axes.ravel():
        # add annotations
        for c in axs.containers:
            labels = [f'{(v.get_height()):.3f}' for v in c]
            #axs.bar_label(c, labels=labels, label_type='center',size=7,rotation='vertical',color='w')
            axs.bar_label(c, labels=labels, label_type='edge',size=10,rotation='vertical')
        #axs.margins(y=0.02)
    if save==True:
        plt.savefig(r'eeg_harmonization\sovaharmony\Reproducibilidad\ICC_Graphics\ICC_{name_group}_{tipo}.png'.format(name_group=group,tipo=x_value))
        plt.close()
    if plot:
        plt.show()

def barplot_icc_comp_nG(icc_data,x_value,plot=False,save=False):
    sns.set(font_scale = 0.9)
    sns.set_theme(style="white")
    ax=sns.catplot(x=x_value,y='ICC',data=icc_data,hue='Group',palette='winter_r',kind='bar',col='Bands',col_wrap=4,legend=False,ci=True, capsize=.2)
    #ax.despine(left=True)
    ax.fig.suptitle('ICC3k for '+ x_value +' in frequency bands')
    ax.add_legend(loc='upper center',bbox_to_anchor=(.5,0.94),ncol=2)
    ax.fig.subplots_adjust(top=0.829,bottom=0.133, right=0.936,left=0.062, hspace=0.143, wspace=0.11) # adjust the Figure in rp
    ax.set(xlabel=None)
    ax.set(ylabel=None)
    ax.fig.text(0.5, 0.07, x_value, ha='center', va='center')
    ax.fig.text(0.03, 0.5,  'ICC', ha='center', va='center',rotation='vertical')
    # iterate through axes
    for axs in ax.axes.ravel():
        # add annotations
        for c in axs.containers:
            labels = [f'{(v.get_height()):.3f}' for v in c]
            #axs.bar_label(c, labels=labels, label_type='center',size=7,rotation='vertical', color='w')
            axs.bar_label(c, labels=labels, label_type='edge',size=10,rotation='vertical')
        #axs.margins(y=0.02)
    if save==True:
        plt.savefig(r'eeg_harmonization\sovaharmony\Reproducibilidad\ICC_Graphics\ICC_Comparacióngrupos_{tipo}.png'.format(tipo=x_value))
        plt.close()
    if plot:
        plt.show()


pl = False
sa = True   

barplot_icc_comp_nG(icc_data_Roi[icc_data_Roi['Stage']=='Normalized data'],'Roi',plot=pl,save=sa)
barplot_icc_comp_nG(icc_data_Comp[icc_data_Comp['Stage']=='Normalized data'],'Components',plot=pl,save=sa)
barplot_icc_nB_1G(icc_data_Roi,'Roi','G2',plot=pl,save=sa)
barplot_icc_nB_1G(icc_data_Roi,'Roi','CTR',plot=pl,save=sa)
barplot_icc_nB_1G(icc_data_Comp,'Components','G2',plot=pl,save=sa)
barplot_icc_nB_1G(icc_data_Comp,'Components','G1',plot=pl,save=sa)

def icc_mean(data):
    Stage=data['Stage'].unique()
    bands=data['Bands'].unique()
    for st in Stage:
        print(st+':')
        d_stage=data[data['Stage']==st]
        print('Promedio general: '+str(d_stage['ICC'].mean())+' ± ' +str(d_stage['ICC'].std())+'\n')
        for band in bands:
            d_band=d_stage[d_stage['Bands']==band]
            print('Promedio '+band+': '+str(d_band['ICC'].mean())+' ± ' +str(d_band['ICC'].std()))
        print('\n')

print('Promedios por bandas de ROIs\n')
icc_mean(icc_data_Roi)
print('Promedios por bandas de Componentes\n')
icc_mean(icc_data_Comp)