# Stb

> Automated Control & Testing for Set-Top Boxes

[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/) 

Stb allows you to issue commands to your set-top box (or whatever device you're wanting to control that takes in IR). It can then anaylze the behavior of the device and how it responds to those commands by
inspecting the video output (using image recognition and OCR).

## Installation

Stb requires [OpenCV](https://opencv.org/), [LIRC](http://www.lirc.org/), and [Gstreamer](https://gstreamer.freedesktop.org/) to be setup and installed already on the given system in order to work properly. LIRC works best with Linux, but there are ports to macOS and Windows. However, this package is setup to only work with Linux right now.

If you use Ubuntu, there is a installation script for the prerequisites in `tools/prerequisites-install-ubuntu.sh`. Note that you will still have to setup the lirc 
configuration and figure out your gstreamer pipelines.

## Linux Infrared Remote Control (LIRC)

The stb library relies on [LIRC](http://lirc.org) to receive and
emit IR signals. Typically your system package manager will be able to
install LIRC e.g. `sudo apt install lirc` for Ubuntu.

The two things you'll have to figure out on your own is the
`lirc_options.conf` file and the remote configuration file as these are
dependent on the hardware you use for your setup. LIRC configuration is
typically in `etc/lirc/`.

For `lirc_options.conf`, the main change you'll want to make is to
change the driver from `devinput` to `default`. Devinput works fine for
receiving IR, but it will not allow you to emit IR. This driver is
dependent on your hardware, but LIRC just works with most devices on
this driver nowadays.

For the remote configuration file, if you're using a common remote
control, you may be able to find it in the LIRC remote control database.
Otherwise, you'll have to create it yourself. This can be done with
LIRC's IR record utility. However, I've had much better luck using a
RedRat3-II and RedRat's IR Signal Database for creating the remote
configuration file. RedRat3-II is now discontinued, but you could look
into the RedRatX or see if you can find a RedRat3-II used. Place this
generated remote configuration file in `etc/lirc/lircd.conf.d/`.

If you're using an Iguanaworks IR Transciever, you may find the discussion
here useful:
  * https://github.com/iguanaworks/iguanair/issues/39

See the [LIRC configuration guide](https://www.lirc.org/html/configuration-guide.html) for more information.

## GStreamer

GStreamer is used to access the video stream from the device under test.
See the [download
page](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html)
to get started.

The important thing with GStreamer is to setup your source and sink pipeline correctly
so stb is able to pull video from the capture card and show it back to you using the sink
pipeline if necessary. To do this, first run `stb config setup` to setup the user configuration
folder at `~/.stb`. Inside, you'll find a `config.ini` file which has keys to set for `source_pipeline`
and `sink_pipeline`. Each capture card may need a different source and sink pipeline so it's hard
to give a generic suggestion here. Use `gst-launch-1.0` to experiment until you find a pipeline 
that works for you. If your capture card is compatible with video for linux (v4l2), something like `gst-launch-1.0 v4l2src ! autovideosink` would likely work to bring up your capture card stream. In
this case, the `source_pipeline` would be `v4l2src` and the `sink_pipeline` would be `autovideosink`.