import gi
from gi.repository import Gst

from stb.frame import Frame

gi.require_version("Gst", "1.0")
Gst.init(None)


class Display:
    def __init__(self, source_pipeline, sink_pipeline):
        pass

    def get_frame(self, timeout_secs: float = 10.0) -> Frame:
        pass

    def is_black(self, frame: Frame = get_frame()) -> bool:
        pass
