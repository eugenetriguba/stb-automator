import pytest

from stb.lirc import Lirc, LircResponse


def test_default_lirc_init(mock_lirc):
    mock_lirc.socket.connect.assert_called_with(mock_lirc.DEFAULT_SOCKET_PATH)


def test_custom_path_lirc_init(mock_socket):
    TEST_SOCKET_PATH = "test_path"
    Lirc(socket=mock_socket, socket_path=TEST_SOCKET_PATH)
    mock_socket.connect.assert_called_with(TEST_SOCKET_PATH)


@pytest.mark.parametrize(
    "reply_packet, success, data, repeat_count",
    [
        (
            b"BEGIN\nSEND_ONCE remote key\nSUCCESS\nEND\n",
            True,
            [],
            1
        )

    ]
)
def test_send_once(mock_lirc, reply_packet, success, data, repeat_count):
    REMOTE = "remote"
    KEY = "key"
    COMMAND = f"SEND_ONCE {REMOTE} {KEY}"

    mock_lirc.socket.recv.return_value = reply_packet
    response = mock_lirc.send_once(KEY, REMOTE)
    mock_lirc.socket.sendall.assert_called_with(
        (COMMAND + "\n").encode(mock_lirc.ENCODING))

    if repeat_count > 1:
        assert type(response) == list
        assert len(response) == repeat_count

        for r in response:
            assert type(r) == LircResponse
            assert r.command == COMMAND
            assert r.success == success
            assert r.data == data
    else:
        assert type(response) == LircResponse
        assert response.command == COMMAND
        assert response.success == success
        assert response.data == data
