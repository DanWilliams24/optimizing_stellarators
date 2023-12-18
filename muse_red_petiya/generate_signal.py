#!/usr/bin/env python3

import sys
import redpitaya_scpi as scpi

IP = 'rp-F0956B.local'
rp_s = scpi.scpi(IP)

wave_form = 'sine'
freq = 10000
ampl = 1

rp_s.tx_txt('GEN:RST')

# Function for configuring a Source
rp_s.sour_set(1, wave_form, ampl, freq, burst=True, nor=10000, ncyc=2, period=5000)
# nor=65536 for INF pulses

rp_s.tx_txt('OUTPUT1:STATE ON')
rp_s.tx_txt('SOUR1:TRIG:INT')

rp_s.close()