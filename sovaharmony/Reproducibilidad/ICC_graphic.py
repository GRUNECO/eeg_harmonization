import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

icc_data_Roi=pd.read_csv(r'sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_ROIS_G2-CTR.csv',sep=';')
icc_data_Comp=pd.read_csv(r'sovaharmony\Reproducibilidad\ICC_values_csv\icc_values_Components_G2-CTR.csv',sep=';')

def barplot_icc_nB_1G(icc_data,x_value,group,plot=False,save=False):
    fil=icc_data['Group']==group
    filter_band=icc_data[fil]
    sns.set(font_scale = 0.9)
    sns.set_theme(style="white")
    ax=sns.catplot(x=x_value,y='ICC',data=filter_band,hue='Stage',palette='winter_r',kind='bar',col='Bands',col_wrap=4,legend=False,estimator=np.mean)
    ax.fig.suptitle('ICC3k for frequency bands and '+x_value )
    ax.add_legend(loc='upper center',bbox_to_anchor=(.5,0.94),ncol=2)
    ax.fig.subplots_adjust(top=0.829,bottom=0.133, right=0.936,left=0.062, hspace=0.143, wspace=0.11) # adjust the Figure in rp
    ax.set(xlabel=None)
    ax.set(ylabel=None)
    ax.fig.text(0.5, 0.07, x_value, ha='center', va='center')
    ax.fig.text(0.03, 0.5,  'ICC', ha='center', va='center',rotation='vertical')
    if save==True:
        plt.savefig('sovaharmony\Reproducibilidad\ICC_Graphics\ICC_{name_group}_{tipo}.png'.format(name_group=group,tipo=x_value))
        plt.close()
    if plot:
        plt.show()

barplot_icc_nB_1G(icc_data_Roi,'Roi','Control',plot=True,save=True)
barplot_icc_nB_1G(icc_data_Comp,'Components','Control',plot=True,save=True)


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

