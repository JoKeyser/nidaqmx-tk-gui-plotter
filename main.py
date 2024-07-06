# PURPOSE: A simple GUI to use NI-DAQmx and plot data in real-time.
#          For now, just read data from one channel.
#
# AUTHORS: Johannes Keyser
#
# LICENSE: CC0-1.0 Universal, Public Domain Dedication
# 
# SPDX-FileCopyrightText: 2024 Johannes Keyser
#
# SPDX-License-Identifier: CC0-1.0


import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
from nidaqmx.stream_readers import AnalogMultiChannelReader

READ_CHANNEL = "Dev1/ai0"  # channel to read from
READ_RATE = 1000  # read rate in Hz
READ_NUMBER = 100  # number of samples to read at once
PLOT_INTERVAL = 0.1  # interval between plot updates (in seconds)

# initialize variables for data storage and plotting
read_data = np.nan * np.ones([1, READ_NUMBER])
xvalues = np.linspace(0, READ_NUMBER, READ_NUMBER)  # for now, just plot the last READ_NUMBER samples

# create an interactive plotting window
plt.ion()
fig, axs = plt.subplots()
line, = axs.plot(xvalues, read_data.flatten())  # FIXME: get rid of the flatten()?
axs.set_xlabel('Last samples')
axs.set_ylabel('Voltage [V]')

with nidaqmx.Task() as read_task:  
    read_task.ai_channels.add_ai_voltage_chan(READ_CHANNEL,
                                              terminal_config=TerminalConfiguration.RSE)
    read_task.timing.cfg_samp_clk_timing(rate = READ_RATE,
                                         sample_mode = AcquisitionType.CONTINUOUS,
                                         samps_per_chan = READ_NUMBER)
    reader = AnalogMultiChannelReader(read_task.in_stream)
    read_task.start()
    
    while True:
        reader.read_many_sample(data = read_data, 
                                number_of_samples_per_channel = READ_NUMBER)
        line.set_ydata(read_data)
        axs.relim()
        axs.autoscale_view()
        plt.pause(PLOT_INTERVAL)  # refresh the plot

