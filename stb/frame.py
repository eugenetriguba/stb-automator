import time

import numpy as np


class Frame(np.ndarray):
    """
    A frame of video from the video stream.

    OpenCV uses a numpy.ndarray to represent images, which is
    stored in a 8-bit BGR format.
    """

    def __new__(
        cls,
        array: np.ndarray,
        dtype: np.dtype = None,
        order=None,
        time: time.time = None,
    ):
        obj = np.asarray(array, dtype=dtype, order=order).view(cls)
        obj.time = time
        return obj

    def __repr__(self):
        if len(self.shape) == 3:
            dimensions = f"<{self.shape[1]}, {self.shape[0]}, {self.shape[2]}>"
        else:
            dimensions = f"<{self.shape[1]}, {self.shape[0]}>"

        time = "None" if self.time is None else "%.3f" % self.time
        return f"<stb.Frame(dimensions={dimensions}, time={time}>"
