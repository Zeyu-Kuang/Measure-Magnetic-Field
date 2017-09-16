import visa
import time
import matplotlib.pyplot as plt
import numpy as np

rm = visa.ResourceManager()
print(rm.list_resources())

inst = rm.open_resource('GPIB1::19::INSTR')
print(inst.query("*IDN?"))
del inst.timeout

# setting sensitivity
sensitivity = 20  # upper limit of input sensitivity (dBm) range=(-30, 24)
inst.write("Voltage:Rang " + str(sensitivity))

# setting window function
inst.write("Sens:Window:Gate HANN")  # hanning window

# averaging
N_aver = 32
inst.write("AVER ON")
inst.write("AVER:COUN " + str(N_aver))

# define frequency
fStart = 1.0  # Hz
fStop = 10000  # Hz
inst.write("frequency:start " + str(fStart) + "Hz")
inst.write("frequency:stop  " + str(fStop) + "Hz")


# display PSD
inst.write(":CALC:FEED 'XFR:POW:PSD 1'")
inst.write(":CALC:FORM MLOG")

# read data
est_time = float(inst.query("SWE2:TIME:gate?"))

psd = inst.query_ascii_values("CALC:DATA?")
time.sleep(est_time * N_aver+ 4)

inst.close()

fPoints = len(psd)
frequency = np.linspace(fStart, fStop, fPoints)


fs = 16

f, ax = plt.subplots(1,1)
ax.semilogx(frequency, psd)
ax.set_xlabel('Hz')
ax.set_ylabel('dBm/Hz')
ax.set_title('PSD')
plt.show()
