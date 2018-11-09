Implementing an Etch-a-Sketch using an e-Paper Display
Scott Baker, http://www.smbaker.com/

### Purpose

An Etch-a-Sketch is a popular toy that uses two dials to move a plotter and draw lines on a screen. The device does not use electricity, but rather a physical plotter that displaces aluminum powder.

This project attempts to replicate an Etch-a-Sketch using modern e-Paper displays and optical encoders.

### Blog post

See http://www.smbaker.com/making-an-e-paper-etch-a-sketch

### Required equipment

The project makes use of the following parts:

* Raspberry Pi - CPU. A Pi model 3, or a Pi Zero (or Zero W) should do fine.
* 4.2" e-Paper display (or other display capable of fast refresh, with the appropriate python libraries)
* Breakout board for the display 
* Two encoders. I chose optical encoders, ENS1J-B28-R00128, due to the high number of pulses per revolution. If using a 5V optical encoder like I did, make sure to add resistors to the encoder outputs.
* Miscellaneous wires, dupont-style connectors, etc. 

### Acknowledgments

- Waveshare, e-paper display libraries
- Ben Krasnow, techniques for fast refresh on 4.2" e-Paper display
- "Etch-a-Sketch" is a trademark of Spin Master LTD
