# nidaqmx-tk-gui-plotter

A simple GUI to use NI-DAQmx and plot data in real time, in Python and Tk

## Purpose

Showcase the use of a National Instruments DAQ device in Python.
For now, aim to plot the recorded data in real time and control the data acquisition with a simple GUI.

## Status

This is very much a work in progress, in its early stages.
Nothing works yet, please tread with care.

## Design

The code aims to be as simple and extensible as possible, to enable learning and modification.
Make it as Pythonic and as efficient as possible, but readability is more important.
Default values are only changed when necessary.

Dependencies are limited to the essential libraries.
Only the most recent versions are supported.

## Roadmap

- [ ] Create minimal useful example of using NI-DAQmx in Python.
- [ ] Add minimal plotting of the data in real time.
- [ ] Add a TKinter GUI to control the data acquisition and plotting.

## Installation

Install Python 3 and the necessary modules, see <https://wiki.python.org/moin/BeginnersGuide/Download>.

The following modules are required:

- `nidaqmx` to use NI-DAQmx, see [nidaqmx](https://nidaqmx-python.readthedocs.io/)
- `numpy` to handle arrays, see [numpy](https://numpy.org/)
- `matplotlib` to plot data, see [matplotlib](https://matplotlib.org/)
- `tkinter` to create the GUI, see [tkinter](https://docs.python.org/3/library/tkinter.html)

## License

This project is licensed under the CC0 1.0 Universal Creative Commons License - see the [LICENSE](LICENSE) file for details.
A simple summary and translations of the CC0 license are available at <https://creativecommons.org/publicdomain/zero/1.0/>.
