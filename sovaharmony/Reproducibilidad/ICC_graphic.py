import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

icc_data=pd.read_csv(r'sovaharmony\Reproducibilidad\icc_values.csv',sep=';')
bands=icc_data['Bands'].unique()
def barplot_icc(icc_data,group,plot=False,save=False):
    for band in bands:
        fil=np.logical_and(icc_data['Bands']==band,icc_data['Group']==group)
        filter_band=icc_data[fil]
        ax=sns.barplot(x='Components',y='ICC',data=filter_band,hue='Stage',palette='winter_r')
        sns.move_legend(ax, "lower center", bbox_to_anchor=(.5, 1), ncol=2, title=None, frameon=False)
        plt.title('ICC3 for '+ band +' in components by '+group,y=1.08)
        if save==True:
            plt.savefig('sovaharmony\Reproducibilidad\ICC\ICC_{name_group}_{name_band}_components.png'.format(name_group=group,name_band=band))
            plt.close()
        if plot:
            plt.show()
    
barplot_icc(icc_data,'G1',plot=False,save=True)
barplot_icc(icc_data,'G2',plot=False,save=True)
