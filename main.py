# PURPOSE: A simple GUI to use NI-DAQmx and plot data in real-time.
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

READ_CHANNELS = ["Dev1/ai0", "Dev1/ai1", "Dev1/ai2"]  # channel(s) to read from  # FIXME: disentangle DevX from channel numbers
READ_RATE = 1000  # reading/sampling rate in Hz
SAMPS_PER_CHAN = 100  # number of samples to acquire per channel into the PC buffer
NUMBER_OF_SAMPLES_PER_CHANNEL = 10  # number of samples to read per channel from PC buffer
PLOT_INTERVAL = 0.01  # interval between plot updates (in seconds)
HISTORY_DURATION = 3  # in seconds
HISTORY_LENGTH = int(READ_RATE * HISTORY_DURATION)

# FIXME: Record and plot a fixed amount of history. Works for a bit, then crashes:
#     "Exception has occurred: DaqReadError -200279"
#     "The application is not able to keep up with the hardware acquisition."
#     "Increasing the buffer size, reading the data more frequently,
#      or specifying a fixed number of samples to read instead of reading
#      all available samples might correct the problem."
#
# Here some relevant(?) information from the NI-DAQmx documentation:
#
#            ---------- HARDWARE ----------         ---- SOFTWARE ----
# Data path: DAQ device -(1)-> Host PC (RAM) -(2)-> Python application
#
# 1. The Timing() function sets the data rate into the DAQ device.
#    - RATE sets how fast the samples are acquired. The specified rate
#      must be a division of the SOURCE input.
#    - SAMPS_PER_CHAN sets the per-channel size of the PC buffer when
#      set to continuous acquisition.
# 2. The Read() function sets the data transfer from PC RAM into Python.
#    - NUMBER_OF_SAMPLES_PER_CHANNEL sets how many samples are pulled
#      from the PC buffer into Python.
#      The number of samples should be ~1/10th the rate set by Timing().
#
# Both steps must agree: The data rate from hardware to the PC buffer must
# not be too fast nor too slow compared to the data rate into the hardware.
#
# FIXME: It seems to work now, but does it really? Need to understand the
#        underlying mechanisms better.

# initialize variables for data storage and plotting
read_data = np.zeros([len(READ_CHANNELS), SAMPS_PER_CHAN])  # most recently read data
data_history = np.nan * np.zeros([len(READ_CHANNELS), HISTORY_LENGTH])  # history of read data
# generate x-values based on linspace, and repeat the same array for all channels
xvalues = np.linspace(0, HISTORY_LENGTH, HISTORY_LENGTH)  # FIXME: For now, in samples, not in seconds
xvalues = np.tile(xvalues, [len(READ_CHANNELS), 1])

# create an interactive plotting window
plt.ion()
fig, axs = plt.subplots()
lines = axs.plot(xvalues.T, data_history.T)
axs.set_xlabel('History of samples')
axs.set_ylabel('Voltage [V]')

plt.show()

with nidaqmx.Task() as read_task:
    for channel in READ_CHANNELS:
        read_task.ai_channels.add_ai_voltage_chan(channel,
                                                  terminal_config=TerminalConfiguration.RSE)
    read_task.timing.cfg_samp_clk_timing(rate = READ_RATE,
                                         sample_mode = AcquisitionType.CONTINUOUS,
                                         samps_per_chan = SAMPS_PER_CHAN)
    reader = AnalogMultiChannelReader(read_task.in_stream)
    read_task.start()
    
    while True:
        reader.read_many_sample(data = read_data, 
                                number_of_samples_per_channel = SAMPS_PER_CHAN)
        # shift the history to the left and append the new data
        data_history = np.roll(data_history, -SAMPS_PER_CHAN, axis=1)
        data_history[:, -SAMPS_PER_CHAN:] = read_data
        # update the plot
        for idx, line in enumerate(lines):
            line.set_ydata(data_history[idx, :].T)
        axs.relim()
        axs.autoscale_view()
        plt.pause(PLOT_INTERVAL)  # refresh the plot
