import socket
from unittest import TestCase, mock

from stb.lirc import Lirc


class MockSocketTest(TestCase):

    def setUp(self):
        self.mock_socket = mock.Mock(spec=socket.socket)


class LircMockSocketTest(MockSocketTest):

    def setUp(self):
        super().setUp()
        self.lirc = Lirc(socket=self.mock_socket)
