__author__ = 'Francis'

import visa
import time
import pandas as pd
import numpy as np

# ------------------------------------ initialization
rm = visa.ResourceManager()
print(rm.list_resources())
inst = rm.open_resource('GPIB1::19::INSTR')
print(inst.query("*IDN?"))

del inst.timeout  #  infinite time out

# setting window function
inst.write("Sens:Window:Gate HANN")  # hanning window

# set integrating time
inst.write("sens:sweep:time:span 4e-4")  # seconds
print('Time Span: ' + str(inst.query_ascii_values("SWE:TIME:span?")[0]) + 's')
print('RBW: ' + str(inst.query_ascii_values("BANDwidth?")[0]) + 'Hz')

# averaging
N_aver = 32
inst.write("AVER:COUN " + str(N_aver))
inst.write("AVER ON")

# define frequency
fStart = 1.0  # Hz
fStop = 10000  # Hz
fPoints = 1601
inst.write("frequency:start " + str(fStart) + "Hz")
inst.write("frequency:stop  " + str(fStop) + "Hz")
inst.write("SWE:POIN " + str(fPoints))


# display PSD
inst.write(":CALC:FEED 'XFR:POW:PSD 1'")
inst.write(":CALC:FORM MLOG")

# ------------------------------------------------------------------------  read data
ssList = list(range(-30, 24, 10))  # read data for different sensitivity
nList = len(ssList)
psdList = [None] * nList
for i in range(nList):
    # report stage
    print(str(i+1) + '/' + str(nList))
    # setting sensitivity
    sensitivity = ssList[i]  # upper limit of input sensitivity (dBm) range=(-30, 24)
    inst.write("Voltage:Rang " + str(sensitivity))  # change sensitivity of the VSA
    inst.write("SYST:KEY 21")  # restart average
    time.sleep(0.2 * N_aver)  # program sleep
    psd = inst.query_ascii_values("CALC:DATA?")  # query data
    psdList[i] = psd

inst.close()

# create frequency for x and transpose psdList for y
frequency = np.linspace(fStart, fStop, fPoints)
psdList = np.array(psdList)
psdList = psdList.transpose()

# ------------------------------------------------------------------  store data

# initial filename
pathname = '.\Data\\'
filename = 'sensitivity.txt'

# create DataFrame Object
ss_df = pd.DataFrame(data=psdList, columns=ssList)
ss_df['frequency (Hz)'] = frequency

# store data
ss_df.to_csv(pathname+filename, index_label='Index')