# Stb Automator

> Automated Control & Testing for Set-Top Boxes

![Python](https://img.shields.io/badge/python-%203.6%20%7C%203.7%20%7C%203.8-blue)
[![Black](https://img.shields.io/badge/style-black-black)](https://pypi.org/project/black/)
![Build Status](https://travis-ci.com/eugenetriguba/stb.svg?branch=master)
[![codecov](https://codecov.io/gh/eugenetriguba/stb/branch/master/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/stb)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)

Stb allows you to issue commands to your set-top box (or whatever device you're wanting to control that takes in IR). It can then anaylze the behavior of the device and how it responds to those commands by
inspecting the video output (using image recognition and OCR).

Full documentation can be found at https://stb-automator.readthedocs.io

## Usage

Stb is a regular python library. It does not come with a test runner or enforce a way for you to write your tests. This package is designed to be a small library that you can easily add to the test suite of your existing applications. It does not come with any sort of test runner. You can use it with python's unittest or a third party library like pytest.

```python
import pytest
import stb

def

```

## Installation

To install the python package, we can do so using pip.

```bash
$ pip install stb-automator
```

## Installation Enviroment Requirements

Stb requires [OpenCV](https://opencv.org/), [LIRC](http://www.lirc.org/), and [Gstreamer](https://gstreamer.freedesktop.org/) to be setup and installed already on the given system in order to work properly. LIRC works best with Linux, but there are ports to macOS and Windows. However, this package is setup to only work with Linux right now.

If you use Ubuntu, there is a installation script for the prerequisites in `tools/prerequisites-install-ubuntu.sh`. Note that you will still have to setup the LIRC configuration and figure out your gstreamer pipelines. Further documentation on how to install these prerequisites and set it all up can be found at the full documentaiton site: https://stb-automator.readthedocs.io