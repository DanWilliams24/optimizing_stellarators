import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import redpitaya_scpi as scpi
import time

# Initialize Red Pitaya connection
IP = 'rp-F0956B.local'
rp_s = scpi.scpi(IP)
rp_s.tx_txt('ACQ:RST')
dec = 4
rp_s.acq_set(dec)

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='graph-update',
        interval=1000, # in milliseconds
        n_intervals=0
    ),
])

@app.callback(
    Output('live-graph', 'figure'),
    [Input('graph-update', 'n_intervals')]
)
def update_graph(n):
    rp_s.tx_txt('ACQ:START')
    rp_s.tx_txt('ACQ:TRIG NOW')

    while True:
        rp_s.tx_txt('ACQ:TRIG:STAT?')
        if rp_s.rx_txt() == 'TD':
            break

    buff = rp_s.acq_data(1, convert=True)
    
    data = go.Scatter(
        y=buff,
        mode='lines',
        name='Voltage'
    )
    # auto-scaling based on the current buffer data
    y_range = [min(buff), max(buff)] if buff else [0, 1]  # Default range if buff is empty
    x_range = [0, len(buff)] if buff else [0, 1]  # Default range if buff is empty

    return {'data': [data], 
            'layout': go.Layout(xaxis=dict(range=x_range), 
                                yaxis=dict(range=y_range),
                                title='Real-time Voltage Plot')}
    #return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(buff), max(buff)]), yaxis=dict(range=[min(buff), max(buff)]))}

if __name__ == '__main__':
    app.run_server(debug=True)
