#!/usr/bin/env python3

import sys
import time
import matplotlib.pyplot as plt
import redpitaya_scpi as scpi
import os 


if (len(sys.argv) > 2):
    led = int(sys.argv[2])
else:
    led = 0

    
IP = '169.254.49.9'        # 'rp-f066c8.local'
rp_s = scpi.scpi(IP)


pid = os.fork()


if pid > 0:
    print("I am parent process:") 
    print("Process ID:", os.getpid()) 
    print("Child's process ID:", pid) 
    wave_form = 'sine'
    freq = 1000000
    ampl = 1

    # Reset Generation and Acquisition
    rp_s.tx_txt('GEN:RST')
    rp_s.tx_txt('ACQ:RST')

    ##### Generation #####
    rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))

    rp_s.tx_txt('SOUR1:BURS:STAT BURST')        # Mode set to BURST
    rp_s.tx_txt('SOUR1:BURS:NCYC 3')            # 3 periods in each burst

    ##### Acqusition #####
    rp_s.tx_txt('ACQ:DEC 1')
    rp_s.tx_txt('ACQ:TRIG:LEV 0')
    rp_s.tx_txt('ACQ:TRIG:DLY 0')

    rp_s.tx_txt('ACQ:START')
    time.sleep(1)
    rp_s.tx_txt('ACQ:TRIG AWG_PE')
    rp_s.tx_txt('OUTPUT1:STATE ON')
    time.sleep(1)

    rp_s.tx_txt('SOUR1:TRIG:INT')

    # Wait for trigger
    while 1:
        rp_s.tx_txt('ACQ:TRIG:STAT?')           # Get Trigger Status
        if rp_s.rx_txt() == 'TD':               # Triggerd?
            break

    while 1:
        rp_s.tx_txt('ACQ:TRIG:FILL?')
        if rp_s.rx_txt() == '1':
            break

    # Read data and plot
    rp_s.tx_txt('ACQ:SOUR1:DATA?')              # Read full buffer (source 1)
    data_string = rp_s.rx_txt()                 # data into a string

    # Remove brackets and empty spaces + string => float
    data_string = data_string.strip('{}\n\r').replace("  ", "").split(',')
    data = list(map(float, data_string))        # transform data into float

    plt.plot(data)
    plt.show()

else:
    print("\nI am child process:") 
    print("Process ID:", os.getpid()) 
    print("Parent's process ID:", os.getppid())
    print ("Blinking LED["+str(led)+"]")

    period = 1 # seconds

    while 1:
        time.sleep(period/2.0)
        rp_s.tx_txt('DIG:PIN LED' + str(led) + ',' + str(1))
        time.sleep(period/2.0)
        rp_s.tx_txt('DIG:PIN LED' + str(led) + ',' + str(0))

    rp_s.close()