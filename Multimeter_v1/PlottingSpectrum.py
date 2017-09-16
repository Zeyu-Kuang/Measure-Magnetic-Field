import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

# reading voltage spectrum
filename = '.\Data\multimeter_voltage.txt'
voltage = pd.read_csv(filename, index_col='Index')

# reading parameters (manually from txt file)
para_filename = '.\Data\multimeter_voltage_para.txt'
delay_df = pd.read_csv(para_filename, index_col='Index')
delay = float(delay_df.values)
print(delay)

# changing data to numpy
vv = voltage.values
index = voltage.index.values
# 2d to 1d
vv = vv.reshape(len(vv))
index = index.reshape(len(index))

# calculating Power Spectrum Density (PSD)
f_s = 1 / delay  # sampling frequency (HZ)
npp = len(vv)  # length of each section. Same as original length to reserve information

f_voltage, S_voltage = signal.welch(vv, fs=f_s, nperseg=npp)
S_voltage = 10 * np.log10(abs(S_voltage).astype(np.float64))  # convention S = 10 * log10(S)

# ----------------------------- plotting -----------------------
f, (ax1, ax2) = plt.subplots(1,2,figsize=(14,6))
fs = 16  # fontsize

# plotting spectrum
ax1.plot(index*delay, vv, "o-")
ax1.set_xlabel('Time (s)', fontsize=fs)
ax1.set_ylabel("Voltage (V)", fontsize=fs)
ax1.set_title('Multimeter', fontsize=fs)
ax1.tick_params(labelsize=fs)

# plotting PSD
ax2.semilogx(f_voltage, S_voltage, "o-")
ax2.set_xlabel('Frequency (HZ)', fontsize=fs)
ax2.set_ylabel("PSD", fontsize=fs)
ax2.set_title('Multimeter Voltage', fontsize=fs)
ax2.tick_params(labelsize=fs)

plt.show()
