#!/usr/bin/env python3

import sys
import time
import matplotlib.pyplot as plt
import redpitaya_scpi as scpi

IP = '169.254.49.9'
rp_s = scpi.scpi(IP)

wave_form = 'sine'
freq = 1000000
ampl = 1

# Reset Generation and Acquisition
rp_s.tx_txt('GEN:RST')
rp_s.tx_txt('ACQ:RST')

# Configure Source
rp_s.sour_set(1, wave_form, ampl, freq, burst=True, ncyc=3)

# Configure Acquisition
rp_s.acq_set(dec=1, trig_lvl=0.1, trig_delay=0)  # Adjust trigger level if necessary

# Start Acquisition
rp_s.tx_txt('ACQ:START')
time.sleep(1)
rp_s.tx_txt('ACQ:TRIG AWG_PE')
rp_s.tx_txt('OUTPUT1:STATE ON')
time.sleep(1)

rp_s.tx_txt('SOUR1:TRIG:INT')
print("starting")
# Wait for Trigger
while 1:
    rp_s.tx_txt('ACQ:TRIG:STAT?')
    if rp_s.rx_txt() == 'TD':
        break

print("almost")
# Wait for Buffer to Fill
while 1:
    rp_s.tx_txt('ACQ:TRIG:FILL?')
    if rp_s.rx_txt() == '1':
        break
print("acquiring")
# Data Acquisition
data = rp_s.acq_data(1, convert=True)

plt.plot(data)
plt.show()
