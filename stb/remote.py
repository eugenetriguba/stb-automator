import time

from stb.lirc import Lirc


class KeyPress:
    def __init__(self, key: str, success: bool, start_time: float, end_time: float):
        self.key = key
        self.success = success
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return (
            f"KeyPress(key={self.key}, "
            f"success={self.success}, "
            f"start_time={self.start_time}, "
            f"end_time={self.end_time})"
        )


class Remote:
    """
    Send IR signals via LIRC.

    This class provides the high-level api for sending IR wheras
    the Lirc class is the lower level api to interacting with LIRC.
    """

    def __init__(
        self, remote_name: str, lirc_socket_path: str = Lirc.DEFAULT_SOCKET_PATH
    ):
        """Initialize this Remote by connecting to the lircd socket."""
        self.remote = remote_name
        self.__lirc = Lirc(socket_path=lirc_socket_path)

    def press(
        self, key: str, repeat_count: int = 1, interpress_delay_secs: float = 0.3
    ):
        """
        Emit an IR signal for a given key.

        :param key: The name of the key.
        :param repeat_count: The number of times to press this key.
        :param interpress_delay_secs: The wait time between key presses
                                      if repeat_count > 1.

        :return: a KeyPress or a list of KeyPress if repeat_count > 1.
        :rtype: KeyPress or list
        """
        if repeat_count > 1:
            key_presses = []

            while repeat_count > 0:
                key_presses.append(self.__timed_send_once(key))
                time.sleep(interpress_delay_secs)
                repeat_count -= 1

            return key_presses

        return self.__timed_send_once(key)

    def __timed_send_once(self, key: str) -> KeyPress:
        start_time = time.time()
        response = self.__lirc.send_once(key, self.remote)
        end_time = time.time()
        value, key_name = response.key.split(" ")
        return KeyPress(key_name, response.success, start_time, end_time)

    def press_and_wait(self, key: str):
        """
        Press the specified key and wait until the screen changes or stops changing.
        """

    def press_until_match(self, key, image):
        """
        Keep pressing key until we find the specified image.
        """
