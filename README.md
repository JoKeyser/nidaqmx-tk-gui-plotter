# nidaqmx-tk-gui-plotter

A simple GUI to use NI-DAQmx and plot data in real time, in Python and Tk

## Purpose

Showcase the use of a National Instruments (NI) Data Acquisition (DAQ) device in Python.
For now, aim to plot the recorded data in real time and control the data acquisition with a simple GUI.

## Status

This is very much a work in progress, in its early stages.
Almost nothing works yet, please tread with care.

## Design

The code aims to be as simple and extensible as possible, to enable learning and modification.
Make it as Pythonic and as efficient as possible, but readability is more important.
Default values are only changed when necessary.

Dependencies are limited to the essential libraries.
Only the most recent versions are supported.

## Roadmap

- [x] Create minimal useful example of using NI-DAQmx in Python.
- [ ] Add minimal plotting of the data in real time.
     - [x] Allow for multiple recording channels.
     - [ ] Plot a fixed history of the data, not just the very last capture.
           (So far, it's working for a while, but then crashes.)
- [ ] Add a TKinter GUI to control the data acquisition and plotting.
     - [ ] Let user select the device and channels.
     - [ ] Let user select the sampling rate.


## Installation

Install Python 3 and the necessary modules, see <https://wiki.python.org/moin/BeginnersGuide/Download>.

The following modules are required:

- [`nidaqmx`](https://nidaqmx-python.readthedocs.io/) to use NI-DAQmx, see 
    - For `nidaqmx` you need to have the NI-DAQmx driver installed; please refer to their documentation.
- [`numpy`](https://numpy.org/) to handle arrays of data
- [`matplotlib`](https://matplotlib.org/) to plot data
- [`tkinter`](https://docs.python.org/3/library/tkinter.html) to create the GUI


## License

This project is licensed under the CC0 1.0 Universal Creative Commons License - see the [LICENSE](LICENSE) file for details.
A simple summary and translations of the CC0 license are available at <https://creativecommons.org/publicdomain/zero/1.0/>.
