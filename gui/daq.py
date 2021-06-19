"""
https://github.com/plotly/dash-daq

"""

import dash_daq as daq


vmax = 3
v = 0
channels = 64

channel = 0

daq.Knob(id="v_{channel}", min=0, max=vmax, value=0)
daq.Gauge(id="i_{channel}", min=0, max=100, value=0)
