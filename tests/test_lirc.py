from unittest import main

from stb.lirc import Lirc
from tests.utils.sockets import LircMockSocketTest


class TestLirc(LircMockSocketTest):

    def test_default_lirc_init(self):
        self.mock_socket.connect.assert_called_with(self.lirc.DEFAULT_SOCKET_PATH)

    def test_custom_path_lirc_init(self):
        TEST_SOCKET_PATH = "test_path"
        Lirc(socket=self.mock_socket, socket_path=TEST_SOCKET_PATH)
        self.mock_socket.connect.assert_called_with(TEST_SOCKET_PATH)


if __name__ == '__main__':
    main()
