import visa
import pandas as pd

# searching for devices
print('Searching for devices ...')
rm = visa.ResourceManager()
print('Avaliable devices: ' + str(rm.list_resources()))  # print avaliable devices
inst = rm.open_resource('GPIB0::22::INSTR')  # selecting Multimeter
print('Selecting devices: ' + str(inst.query("*IDN?")))  # print Multimeter

# set parameters
delay = 0.0001  #  set the delay (seconds)
counts = 511  # set the sample counts (maxium 512)
del inst.timeout  # set infinite timeout

# intialization
inst.write("CONF:VOLT:DC 10, 0.3")  # Configure the initial state: DC voltage with certain range and resolution
inst.write("TRIGger:DElay " + str(delay))  # set the triggering delay
inst.write("SAMPle:COUNt " + str(counts))  # set the sampling numbers in one trigger
inst.write("TRIG:SOUR IMM")  # chose a trigger source (immediate internal trigger)

# reporting settings
print('Triggering delay (seconds) set to: ' + inst.query("TRIGger:DELay?"))
print('Sample Counts set to ' + inst.query("SAMPle:COUNt?"))
print('Timeout: infinite')

# reading voltage
inst.write("INIT")  # prepare multimeter for triggering
voltage = inst.query_ascii_values('FETC?')  # trigger the multimeter (read the data as list)

# reporting result
print('Measured Voltage(V): ' + str(voltage))  # print measured x field

# save data
vol_df = pd.DataFrame({'Voltage (V)': voltage})  # create a DataFrame object for I/O
filename = '.\Data\multimeter_voltage.txt'
vol_df.to_csv(filename, index_label='Index')

# save para
para_df = pd.DataFrame({'delay': delay}, index=[0])
para_filename = '.\Data\multimeter_voltage_para.txt'
para_df.to_csv(para_filename, index_label='Index')



print('Program ended')