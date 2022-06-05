import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 

icc_data=pd.read_csv(r'sovaharmony\Reproducibilidad\icc_values_G2-CTR.csv',sep=';')
bands=icc_data['Bands'].unique()
def barplot_icc(icc_data,group,plot=False,save=False):
    for band in bands:
        fil=np.logical_and(icc_data['Bands']==band,icc_data['Group']==group)
        filter_band=icc_data[fil]
        ax=sns.barplot(x='Components',y='ICC',data=filter_band,hue='Stage',palette='winter_r', row='Bands')
        sns.move_legend(ax, "lower center", bbox_to_anchor=(.5, 1), ncol=2, title=None, frameon=False)
        plt.title('ICC3 for '+ band +' in components by '+group,y=1.08)
        if save==True:
            plt.savefig('sovaharmony\Reproducibilidad\ICC\ICC_{name_group}_{name_band}_components.png'.format(name_group=group,name_band=band))
            plt.close()
        if plot:
            plt.show()
    

def barplot_icc_nB_1G(icc_data,group,plot=False,save=False):
    fil=icc_data['Group']==group
    filter_band=icc_data[fil]
    sns.set(font_scale = 0.9)
    sns.set_theme(style="white")
    ax=sns.catplot(x='Components',y='ICC',data=filter_band,hue='Stage',palette='winter_r',kind='bar',col='Bands',col_wrap=4,legend=False,estimator=np.mean)
    ax.fig.suptitle('ICC3k for frequency bands in neuronal components' )
    ax.add_legend(loc='upper center',bbox_to_anchor=(.5,0.94),ncol=2)
    ax.fig.subplots_adjust(top=0.829,bottom=0.133, right=0.936,left=0.062, hspace=0.143, wspace=0.11) # adjust the Figure in rp
    ax.set(xlabel=None)
    ax.set(ylabel=None)
    ax.fig.text(0.5, 0.07, 'Neuronal components', ha='center', va='center')
    ax.fig.text(0.03, 0.5,  'ICC', ha='center', va='center',rotation='vertical')
    # _, ylabels = plt.yticks()
    # _, xlabels = plt.xticks()
    # ax.set_yticklabels(ylabels, fontsize=18)
    # ax.set_xticklabels(xlabels, fontsize=18)
    #ax.fig.subplots_adjust(top=0.857,bottom=0.121, right=0.986,left=0.2, hspace=0.138, wspace=0.062)
    # sns.move_legend(ax, "lower center", bbox_to_anchor=(.5, 1), ncol=2, title=None, frameon=False)
    # plt.title('ICC3 for ' +' in components by '+group,y=1.08)
    if save==True:
        plt.savefig('sovaharmony\Reproducibilidad\ICC\ICC_{name_group}_components.png'.format(name_group=group))
        plt.close()
    if plot:
        plt.show()


#barplot_icc_nB_1G(icc_data,'G1',plot=True,save=False)
barplot_icc_nB_1G(icc_data,'Control',plot=True,save=False)

