import numpy as np
from scipy.signal import butter, lfilter, freqz, filtfilt
import matplotlib.pyplot as plt
import mne
from scipy import signal


filename=r"C:\Users\veroh\OneDrive - Universidad de Antioquia\Datos_MsC_Veronica\BIOMARCADORES\derivatives\sovaharmony\sub-CTR001\ses-V0\eeg\sub-CTR001_ses-V0_task-CE_desc-prep_eeg.fif"
raw = mne.io.read_raw(filename,preload=True )
data = np.asarray(raw._data[0], dtype='float64')

Fs = 1000 # Frecuencia de muestreo
T = 1/Fs # Periodo de muestreo
t1 = np.arange(0, len(data))

fig = plt.figure()

F1 = np.fft.fft(data)
F2 = np.zeros((len(F1)))
F2[1:6] = F1[1:6]
F3 = np.zeros((len(F1)))
F3[6:8] = F1[6:8]
F4 = np.zeros((len(F1)))
F4[8:10] = F1[8:10]
F5 = np.zeros((len(F1)))
F5[10:12] = F1[10:12]
F6 = np.zeros((len(F1)))
F6[12:18] = F1[12:18]
F7 = np.zeros((len(F1)))
F7[18:21] = F1[18:21]
F8 = np.zeros((len(F1)))
F8[21:30] = F1[21:30]
F9 = np.zeros((len(F1)))
F9[30:45] = F1[30:45]

xr1 = np.fft.ifft(F2)
xr2 = np.fft.ifft(F3)
xr3 = np.fft.ifft(F4)
xr4 = np.fft.ifft(F5)
xr5 = np.fft.ifft(F6)
xr6 = np.fft.ifft(F7)
xr7 = np.fft.ifft(F8)
xr8 = np.fft.ifft(F9)

ax1 = fig.add_subplot(811)
ax1.set_title('Delta (1.5Hz - 6Hz)')
ax1.plot(t1, np.real(xr1))
ax1.axis('off')

ax2 = fig.add_subplot(812)
ax2.set_title('Theta (6Hz - 8.5Hz)')
ax2.plot(t1, np.real(xr2))
ax2.axis('off')

ax3 = fig.add_subplot(813)
ax3.set_title('Alpha1 (8.5Hz - 10.5Hz)')
ax3.plot(t1, np.real(xr3))
ax3.axis('off')

ax4 = fig.add_subplot(814)
ax4.set_title('Alpha2 (10.5Hz- 12.5Hz)')
ax4.plot(t1, np.real(xr4))
ax4.axis('off')

ax5 = fig.add_subplot(815)
ax5.set_title('Beta1 (12.5Hz - 18.5Hz)')
ax5.plot(t1, np.real(xr5))
ax5.axis('off')

ax6 = fig.add_subplot(816)
ax6.set_title('Beta2 (18.5Hz - 21Hz)')
ax6.plot(t1, np.real(xr6))
ax6.axis('off')

ax7 = fig.add_subplot(817)
ax7.set_title('Beta3 (21Hz - 30Hz)')
ax7.plot(t1, np.real(xr7))
ax7.axis('off')

ax8 = fig.add_subplot(818)
ax8.set_title('Gamma (30Hz - 45Hz)')
ax8.plot(t1, np.real(xr8))
ax8.axis('off')

plt.show()

'''
bands =Bands({'delta':[1.5,6],
        'theta':[6,8.5],
        'alpha-1':[8.5,10.5],
        'alpha-2':[10.5,12.5],
        'beta1':[12.5,18.5],
        'beta2':[18.5,21],
        'beta3':[21,30],
        'gamma':[30,45]})
'''




#
#
#f1 = (2*21)/1000
#f2 = (2*30)/1000
#
#b, a = signal.butter(2, [f1,f2], fs = 1000, btype = 'bandpass', analog = False)   #Configuration filter 8 representa el orden del filtro
#filtedData = filtfilt(b, a, data)
#filtedData[np.isnan(filtedData)] = 0
#
#
## Import numpy and matplotlib
#import numpy as np
#import matplotlib.pyplot as plt
#
## Import the FOOOF object
#from fooof import FOOOF
#
## Import simulation, utility, and plotting tools
#from fooof.bands import Bands
#from fooof.utils import trim_spectrum
#from fooof.analysis import get_band_peak_fm
#from fooof.sim.gen import gen_power_spectrum
#from fooof.sim.utils import set_random_seed
#from fooof.plts.spectra import plot_spectra_shading
#
#def compare_exp(fm1, fm2):
#    """Compare exponent values."""
#
#    exp1 = fm1.get_params('aperiodic_params', 'exponent')
#    exp2 = fm2.get_params('aperiodic_params', 'exponent')
#
#    return exp1 - exp2
#
#def compare_peak_pw(fm1, fm2, band_def):
#    """Compare the power of detected peaks."""
#
#    pw1 = get_band_peak_fm(fm1, band_def)[1]
#    pw2 = get_band_peak_fm(fm2, band_def)[1]
#
#    return pw1 - pw2
#
#def compare_band_pw(fm1, fm2, band_def):
#    """Compare the power of frequency band ranges."""
#
#    pw1 = np.mean(trim_spectrum(fm1.freqs, fm1.power_spectrum, band_def)[1])
#    pw2 = np.mean(trim_spectrum(fm1.freqs, fm2.power_spectrum, band_def)[1])
#
#    return pw1 - pw2
#
## Set consistent aperiodic parameters
#ap_params = [1, 1]
#
## Set periodic parameters, defined to vary between groups
##   All parameters are set to match, except for systematic power differences
#pe_g1 = [[2, 0.25, 1], [6, 0.2, 1], [10, 0.5, 1.5], [20, 0.2, 3], [40, 0.25, 3.5]]
#pe_g2 = [[2, 0.5, 1], [6, 0.3, 1], [10, 0.5, 1.5], [20, 0.15, 3], [40, 0.15, 3.5]]
#
## Set random seed, for consistency generating simulated data
#set_random_seed(21)
#bands =Bands({'delta':[1.5,6],
#        'theta':[6,8.5],
#        'alpha-1':[8.5,10.5],
#        'alpha-2':[10.5,12.5],
#        'beta1':[12.5,18.5],
#        'beta2':[18.5,21],
#        'beta3':[21,30],
#        'gamma':[30,45]})
#
## Define plot settings
#t_settings = {'fontsize' : 24, 'fontweight' : 'bold'}
#shade_cols = ['#e8dc35', '#46b870', '#1882d9', '#a218d9', '#e60026']
#labels = ['Group-1', 'Group-2']
#
## General simulation settings
#f_range = [1, 50]
#nlv = 0
## Simulate example power spectra for each group
#freqs, g1_spectrum_bands = gen_power_spectrum(f_range, ap_params, pe_g1, nlv)
#freqs, g2_spectrum_bands = gen_power_spectrum(f_range, ap_params, pe_g2, nlv)
#
## Define some template strings for reporting
#exp_template = "The difference of aperiodic exponent is: \t {:1.2f}"
#pw_template = ("The difference of {:5} power is  {: 1.2f}\t"
#               "with peaks or  {: 1.2f}\t with bands.")
#
## Plot the power spectra differences, representing the 'band-by-band' idea
#plot_spectra_shading(freqs, [g1_spectrum_bands, g2_spectrum_bands],
#                     log_powers=True, linewidth=3,
#                     shades=bands.definitions, shade_colors=shade_cols,
#                     labels=labels)
#plt.xlim(f_range);
#plt.title('Band-by-Band', t_settings);
#plt.xlim(1.5,45)
#plt.show()
#
## Initialize FOOOF objects
#fm_bands_g1 = FOOOF(verbose=False)
#fm_bands_g2 = FOOOF(verbose=False)
#
## Fit power spectrum models
#fm_bands_g1.fit(freqs, g1_spectrum_bands)
#fm_bands_g2.fit(freqs, g2_spectrum_bands)
#
## Plot the power spectra differences
#plot_spectra_shading(freqs, [fm_bands_g1._spectrum_flat, fm_bands_g2._spectrum_flat],
#                     log_powers=False, linewidth=3,
#                     shades=bands.definitions, shade_colors=shade_cols,
#                     labels=labels)
#plt.xlim(f_range);
#plt.title('Band-by-Band - Flattened', t_settings);
#plt.xlim(1.5,45)
#plt.show()