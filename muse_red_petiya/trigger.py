#!/usr/bin/env python3

import sys
import redpitaya_scpi as scpi
import time

IP = 'rp-f0956b.local'
rp_s = scpi.scpi(IP)

wave_form = 'square'
freq = 700
ampl = 1
n = 1000

rp_s.tx_txt('GEN:RST')

# Function for configuring a Source
rp_s.sour_set(1, wave_form, ampl, freq, burst=True, ncyc=1, trig="EXT_PE")

# For short triggering signals set the length of internal debounce filter in us (minimum of 1 us)


timeout = time.time() + 60 # 60 seconds from now
while time.time() < timeout:
    rp_s.tx_txt('OUTPUT1:STATE ON')
    time.sleep(1)
    rp_s.close()


