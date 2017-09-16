import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

# reading voltage spectrum
filename = '.\Data\multimeter_voltage.txt'
data = pd.read_csv(filename, index_col='Index')
voltage = data['Voltage (V)']
time = data['Time (s)']

# reading parameters (manually from txt file)
para_filename = '.\Data\multimeter_voltage_para.txt'
delay_df = pd.read_csv(para_filename, index_col='Index')
delay = float(delay_df.values)
print(delay)

# calculating Power Spectrum Density (PSD)
f_s = 1 / delay  # sampling frequency (HZ)
npp = len(voltage)  # length of each section. Same as original length to reserve information

f_voltage, S_voltage = signal.welch(voltage, fs=f_s, nperseg=npp)
S_voltage = 10 * np.log10(abs(S_voltage).astype(np.float64))  # convention S = 10 * log10(S)

# ----------------------------- plotting -----------------------
f, (ax1, ax2) = plt.subplots(1,2,figsize=(14,6))
fs = 16  # fontsize

# plotting spectrum
ax1.plot(time, voltage, "o-")
ax1.set_xlabel('Time (s)', fontsize=fs)
ax1.set_ylabel("Voltage (V)", fontsize=fs)
ax1.set_title('Multimeter', fontsize=fs)
ax1.tick_params(labelsize=fs)

# plotting PSD
ax2.semilogx(f_voltage, S_voltage, "-")
ax2.set_xlabel('Frequency (HZ)', fontsize=fs)
ax2.set_ylabel("PSD", fontsize=fs)
ax2.set_title('Multimeter Voltage', fontsize=fs)
ax2.tick_params(labelsize=fs)

plt.show()
