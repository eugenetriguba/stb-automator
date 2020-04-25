import numpy
import pytest

from stb.frame import Frame


@pytest.mark.parametrize("dimensions, time", [(numpy.ndarray(shape=(2, 2)), None)])
def test_frame_repr_for_size_two(dimensions, time):
    frame = Frame(dimensions, time=time)
    assert (
        f"<stb.Frame(dimensions=<{frame.shape[1]}, {frame.shape[0]}>, time={time}>"
        == frame.__repr__()
    )


@pytest.mark.parametrize("dimensions, time", [(numpy.ndarray(shape=(2, 2, 2)), None)])
def test_frame_repr_for_size_three(dimensions, time):
    frame = Frame(dimensions, time=time)
    assert (
        f"<stb.Frame("
        f"dimensions=<{frame.shape[1]}, {frame.shape[0]}, {frame.shape[2]}>, "
        f"time={time}>" == frame.__repr__()
    )
