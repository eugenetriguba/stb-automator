import socket
from unittest import mock

import pytest
from click.testing import CliRunner

from stb.lirc import Lirc


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_socket():
    return mock.Mock(spec=socket.socket)


@pytest.fixture
def mock_lirc(mock_socket):
    return Lirc(socket=mock_socket)
