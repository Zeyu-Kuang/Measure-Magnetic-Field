import pandas as pd
from Multi import init_multi
import time

inst = init_multi(0, 1)  # one sample in each trigger, 0 delay

N = 10000  # measured data points
delay = 0.03  # delay between each trigger

time0 = time.time()
time2 = 0
time_record = [None] * N
voltage = [None] * N

for i in range(N):
    time1 = time.time() - time0  # record end time

    # delay module
    time12 = time1 - time2  # time cost
    time_wait = delay - time12
    print('Time 1: ' + str(time1))
    print('Time wait: ' + str(time_wait))
    print(i)
    time.sleep(time_wait)  # time still need for enough delay

    time2 = time.time() - time0  # record the start time
    voltage[i] = inst.query_ascii_values('READ?')[0]  # trigger the multimeter (read the data as list)

    time_record[i] = time2  # record the time



# reporting result
print('Measured Voltage(V): ' + str(voltage))  # print measured x field

# save data
vol_df = pd.DataFrame({'Voltage (V)': voltage, 'Time (s)': time_record})  # create a DataFrame object for I/O
filename = '.\Data\multimeter_voltage.txt'
vol_df.to_csv(filename, index_label='Index')

# save para
para_df = pd.DataFrame({'delay': delay}, index=[0])
para_filename = '.\Data\multimeter_voltage_para.txt'
para_df.to_csv(para_filename, index_label='Index')




print('Program ended')