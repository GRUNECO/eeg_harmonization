"""
@author: Brayan Hoyos Madera, Universidad de Antioquia, leobahm72@gmail.com

"""

from mne.io import read_raw_cnt

def load(path):
    try:
        raw_data = read_raw_cnt(path, montage=None, stim_channel=False)
        data = raw_data.get_data()
        return data, raw_data.info['sfreq']
    except:
        print("The file path: %s no found"%path)
