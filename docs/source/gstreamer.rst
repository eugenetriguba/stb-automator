GStreamer
=========

GStreamer is used to access the video stream from the device under test.
See the `download page <https://gstreamer.freedesktop.org/documentation/installing/on-linux.html>`_
to get started.


Setup
-----
The important thing with GStreamer is to setup your source and sink pipeline correctly.
The source pipeline is what stb-automator uses to be able to pull video from the capture card.
The sink pipeline is used to show it back to you in a GUI window, if necessary.

To do this, first run `stb config setup` to setup the user configuration folder at `~/.stb`.
Inside, you'll find a `config.ini` file which has keys to set for `source_pipeline` and `sink_pipeline`.
Each capture card may need a different source and sink pipeline so it's hard to give a generic suggestion
here. Use `gst-launch-1.0` to experiment until you find a pipeline that works for you. If your capture
card is compatible with video for linux (v4l2), something like `gst-launch-1.0 v4l2src ! autovideosink`
may work to bring up your capture card stream. In this case, the `source_pipeline` would be `v4l2src` and
the `sink_pipeline` would be `autovideosink`.