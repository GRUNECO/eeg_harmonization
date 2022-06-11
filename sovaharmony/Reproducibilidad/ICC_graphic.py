import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

icc_data=pd.read_csv(r'eeg_harmonization\sovaharmony\Reproducibilidad\icc_values.csv',sep=';')
bands=icc_data['Bands'].unique()
def barplot_icc(icc_data,group,plot=False,save=False):
    for band in bands:
        fil=np.logical_and(icc_data['Bands']==band,icc_data['Group']==group)
        filter_band=icc_data[fil]
        ax=sns.barplot(x='Components',y='ICC',data=filter_band,hue='Stage',palette='winter_r', row='Bands')
        sns.move_legend(ax, "lower center", bbox_to_anchor=(.5, 1), ncol=2, title=None, frameon=False)
        plt.title('ICC3 for '+ band +' in components by '+group,y=1.08)
        if save==True:
            plt.savefig('eeg_harmonization\sovaharmony\Reproducibilidad\ICC\ICC_{name_group}_{name_band}_components.png'.format(name_group=group,name_band=band))
            plt.close()
        if plot:
            plt.show()
    

def barplot_icc_nB_1G(icc_data,x_value,group,plot=False,save=False):
    fil=icc_data['Group']==group
    filter_band=icc_data[fil]
    plt.figure(figsize=(8, 6))
    ax=sns.catplot(x='Components',y='ICC',data=filter_band,hue='Stage',palette='winter_r',kind='bar',col='Bands',col_wrap=4,legend=False)
    ax.fig.suptitle('ICC3k for frequency bands' +' in components by '+group)
    ax.add_legend(loc='upper center',bbox_to_anchor=(.5,0.98),ncol=2)
    _, ylabels = plt.yticks()
    _, xlabels = plt.xticks()
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    #ax.set_yticklabels(ylabels, size=18)
    #ax.set_xticklabels(xlabels, size=18)
    # sns.move_legend(ax, "lower center", bbox_to_anchor=(.5, 1), ncol=2, title=None, frameon=False)
    # plt.title('ICC3 for ' +' in components by '+group,y=1.08)
    if save==True:
        plt.savefig('eeg_harmonization\sovaharmony\Reproducibilidad\ICC\ICC_{name_group}_components.png'.format(name_group=group))
        plt.close()
    if plot:
        plt.show()

barplot_icc_nB_1G(icc_data_Roi[icc_data_Roi['Stage']=='Preprocessed data'],'Roi','Control',plot=True,save=True)
barplot_icc_nB_1G(icc_data_Comp[icc_data_Comp['Stage']=='Preprocessed data'],'Components','Control',plot=True,save=True)


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
icc_mean(icc_data_Roi[icc_data_Roi['Stage']=='Preprocessed data'])
print('Promedios por bandas de Componentes\n')
icc_mean(icc_data_Comp[icc_data_Comp['Stage']=='Preprocessed data'])

