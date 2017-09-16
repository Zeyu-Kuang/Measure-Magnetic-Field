__author__ = 'Francis'
import pandas as pd
import matplotlib.pyplot as plt

# initial filename
pathname = '.\Data\\'
filename = 'sensitivity.txt'

# create DataFrame
ss_df = pd.read_csv(pathname+filename, index_col='Index')

# get data from ss_df
frequency = ss_df['frequency (Hz)']

psd_df = ss_df.drop(['frequency (Hz)'], axis=1)
psdList = psd_df.values
ssCol = psd_df.columns.values

ssList = ['sensitivity: ' + x for x in ssCol]

fs = 16

f, ax = plt.subplots(1,1)
ax.semilogx(frequency, psdList)
ax.set_xlabel('Hz')
ax.set_ylabel('dBm/Hz')
ax.set_title('PSD')
plt.legend(ssList)
plt.show()