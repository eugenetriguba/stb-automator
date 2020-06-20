import gi
from config_file import ConfigFile
from gi.repository import Gst

from stb.frame import Frame
from stb.utils import get_config_file_path

gi.require_version("Gst", "1.0")
Gst.init(None)


class Display:
    def __init__(self, source_pipeline: str = None, sink_pipeline: str = None):
        self.source_pipeline = source_pipeline
        self.sink_pipeline = sink_pipeline

    def get_frame(self, timeout_secs: float = 10.0) -> Frame:
        pass

    def is_black(self, frame: Frame = get_frame()) -> bool:
        pass
