#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt
import redpitaya_scpi as scpi

IP = 'rp-F0956B.local'

rp_s = scpi.scpi(IP)

rp_s.tx_txt('ACQ:RST')

dec = 4

# Function for configuring Acquisition
rp_s.acq_set(dec)

rp_s.tx_txt('ACQ:START')
rp_s.tx_txt('ACQ:TRIG NOW')

while 1:
    rp_s.tx_txt('ACQ:TRIG:STAT?')
    if rp_s.rx_txt() == 'TD':
        break
print("Ran....")

# function for Data Acquisition
buff = rp_s.acq_data(1, convert= True)

plt.plot(buff)
plt.ylabel('Voltage')
plt.show()