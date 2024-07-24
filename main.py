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
import time
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
from nidaqmx.stream_readers import AnalogMultiChannelReader

# Set desired parameters for data acquisition and plotting.
READ_CHANNELS = ["Dev1/ai0", "Dev1/ai1", "Dev1/ai2"]  # channel(s) to read from  # FIXME: disentangle DevX from channel numbers
READ_RATE = 3000  # acquisition sampling rate, in Hz
HISTORY_DURATION = 3  # history duration, in seconds
PLOT_REFRESH_RATE = 20  # refresh rate of the plot, in Hz

# Calculate derived parameters.
HIST_LEN = int(READ_RATE * HISTORY_DURATION)  # number of samples in history
PLOT_INTERVAL = 1 / PLOT_REFRESH_RATE  # plot update interval, in seconds
# For real-time plotting, the plot refresh rate is the limiting factor;
# i.e., it is unnecessary to acquire data faster than the plot refresh rate.
#
# FIXME: For PLOT_REFRESH_RATE > ~10 Hz, the following error occurs:
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
# Thus, set the buffer size for continuous acquisition to a multiple of the
# plotting rate.
SAMPS_PER_CHAN = int(READ_RATE / PLOT_REFRESH_RATE * 2)
# Set the number of samples per plot refresh from the buffer to be slightly
# larger than what is expected to be in the buffer at that time, to avoid
# buffer overflows by too much acquisition over too little consumption.
NUMBER_OF_SAMPLES_PER_CHANNEL = int(READ_RATE / PLOT_REFRESH_RATE * 1.1)

# initialize variables for data storage and plotting
data_read = np.zeros([len(READ_CHANNELS), NUMBER_OF_SAMPLES_PER_CHANNEL])
data_hist = np.nan * np.zeros([len(READ_CHANNELS), HIST_LEN])  # history of read data
# generate x-values based on linspace, and repeat the same array for all channels
xvalues = np.linspace(-HIST_LEN, 0, HIST_LEN)  # FIXME: For now, in samples, not in seconds
xvalues = np.tile(xvalues, [len(READ_CHANNELS), 1])

# create an interactive plotting window
plt.ion()
fig, axs = plt.subplots()
lines = axs.plot(xvalues.T, data_hist.T)
axs.set_xlabel('History of samples (newest on the right ->)')
axs.set_ylabel('Voltage [V]')
axs.set_title(f"Real-time plot, sampling rate = {READ_RATE} Hz")
axs.legend(READ_CHANNELS, loc='upper left')

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
        reader.read_many_sample(data = data_read, 
            number_of_samples_per_channel = NUMBER_OF_SAMPLES_PER_CHANNEL)
        # shift the history to the left and append the new data
        data_hist = np.roll(data_hist, -NUMBER_OF_SAMPLES_PER_CHANNEL, axis=1)
        data_hist[:, -NUMBER_OF_SAMPLES_PER_CHANNEL:] = data_read
        
        # update the plot
        for idx, line in enumerate(lines):
            line.set_ydata(data_hist[idx, :].T)
        axs.relim()
        axs.autoscale_view()
        time_start = time.time()
        # FIXME: pause() takes about >0.1 seconds even for shorter intervals, leading to buffer overflows
        plt.pause(PLOT_INTERVAL)
        time_stop = time.time()
        print(f"Time since update = {time_stop - time_start:.3f} s")
