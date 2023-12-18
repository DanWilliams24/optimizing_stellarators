#!/usr/bin/env python3

import redpitaya_scpi as scpi
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from IPython.display import display
import time

IP = 'rp-F0956B.local'
rp_s = scpi.scpi(IP)

# Reset and configure acquisition
rp_s.tx_txt('ACQ:RST')
dec = 4
rp_s.acq_set(dec)

# Create a Plotly figure
fig = make_subplots(rows=1, cols=1)
trace = go.Scatter(y=[], mode='lines')
fig.add_trace(trace, row=1, col=1)
fig.update_layout(height=600, width=800, title='Real-time Voltage Plot')
plot = go.FigureWidget(fig)
display(plot)

while True:
    rp_s.tx_txt('ACQ:START')
    rp_s.tx_txt('ACQ:TRIG NOW')
    
    while True:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break
    
    buff = rp_s.acq_data(1, convert=True)

    plot.data[0].y = buff
    time.sleep(0.1)  # Adjust this for your desired refresh rate
    display(plot)