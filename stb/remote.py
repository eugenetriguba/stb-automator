import time
from typing import Union, List

from lirc import Client, LircdConnection

from .key_press import KeyPress


class Remote:
    """Send IR signals via LIRC."""

    def __init__(self, name: str, connection: LircdConnection = None):
        """
        Initialize this Remote by connecting to the lircd socket.

        Args:
            name: Name of the remote to use.
                  Corresponds to the name of your LIRC remote.

            connection: An LircdConnection specifying how to connect to LIRC
            on your system. By default, this will choose sensible defaults
            depending on the operating system it is run on. See
            https://pypi.org/project/lirc/ for more.
        """
        self.__name = name
        self.__lirc = Client(connection=connection if connection else LircdConnection())

    def press(
        self, key: str, repeat_count: int = 1, interpress_delay_secs: float = 0.3
    ) -> Union[KeyPress, List[KeyPress]]:
        """
        Emit an IR signal for a given key.

        Args:
            key: The name of the key.
            repeat_count: The number of times to press this key.
            interpress_delay_secs: The wait time between key presses if repeat_count > 1.

        Returns:
            a KeyPress or a list of KeyPress if repeat_count > 1.
        """
        if repeat_count > 1:
            key_presses = []

            while repeat_count > 0:
                key_presses.append(self.__timed_send(key))
                time.sleep(interpress_delay_secs)
                repeat_count -= 1

            return key_presses

        return self.__timed_send(key)

    def __timed_send(self, key: str) -> KeyPress:
        start_time = time.time()
        self.__lirc.send(self.__name, key)
        end_time = time.time()

        return KeyPress(key, start_time, end_time)

    def press_and_wait(self, key: str):
        """
        Press the specified key and wait until the screen changes or stops changing.
        """

    def press_until_match(self, key, image):
        """
        Keep pressing key until we find the specified image.
        """
