import platform
import socket
import sys
import threading
import time


class PressResult:
    def __init__(self, command: str, success: bool, lirc_data: list):
        self.command = command
        self.success = success
        self.lirc_data = lirc_data
        self.start_time = None
        self.end_time = None


class Remote:
    """
    Send IR signals via LIRC.

    More information on the lircd daemon, socket interface,
    reply package format, etc. can be found at https://www.lirc.org/html/lircd.html
    """

    DEFAULT_UNIX_SOCKET = "/var/run/lirc/lircd"

    def __init__(self, remote_name: str, lirc_socket_path: str = DEFAULT_UNIX_SOCKET):
        """
        Initialize this Remote by connecting to the lircd socket.

        Currently, the remote will exit with a status code of 1 if the
        system running it is not a Linux system.
        """
        system = platform.system()
        if system == "Linux":
            self.__lock = threading.Lock()
            self.remote = remote_name
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(lirc_socket_path)
        else:
            print(f"The current system ({system}) is not supported.")
            sys.exit(1)

    def __send_command(self, command: str) -> PressResult:
        """
        Send a command to lircd.

        :param command: A command from the lircd socket command interface.
        :return: A PressResult
        """
        command += "\n"

        try:
            self.__lock.acquire()

            start_time = time.time()
            self.socket.sendall(command.encode("utf-8"))
            end_time = time.time()

            reply_packet = self.__read_reply_packet()
            press_result = self.__parse_reply_packet(reply_packet)
            press_result.start_time = start_time
            press_result.end_time = end_time

            return press_result
        finally:
            self.__lock.release()

    def __read_reply_packet(self) -> str:
        """
        Read the reply packet that lircd sends after a sent command.

        Reply packet format:

            BEGIN
            <command>
            [SUCCESS|ERROR]
            [DATA
            n
            n lines of data]
            END
        """
        BUFFER_LENGTH = 256
        buffer = ""
        data = self.socket.recv(BUFFER_LENGTH)

        # Ignore recieve requests that the socket caches
        while "BEGIN" not in data.decode("utf-8"):
            data = self.socket.recv(BUFFER_LENGTH)

        buffer += data.decode("utf-8")

        while not buffer.endswith("END\n"):
            data = self.socket.recv(BUFFER_LENGTH)
            buffer += data

        return buffer

    def __parse_reply_packet(self, packet: str) -> PressResult:
        """WIP"""
        lines = packet.split("\n")
        print(lines)
        return PressResult("blah", True, [])

    def press(
        self, key: str, repeat_count: int = 1, interpress_delay_secs: float = 0.3
    ):
        """
        Emit an IR signal for a given key.

        :param key: The name of the key.
        :param repeat_count: The number of times to press this key.
        :param interpress_delay_secs: The wait time between key presses
                                      if repeat_count > 1.

        :return: a PressResult or a list of PressResults if repeat_count > 1.
        :rtype: PressResult or list
        """
        if repeat_count > 1:
            responses = []

            while repeat_count > 0:
                responses.append(
                    self.__send_command(f"SEND_ONCE {self.remote} {key} 1")
                )
                repeat_count -= 1

                if repeat_count >= 1:
                    time.sleep(interpress_delay_secs)

            return responses

        return self.__send_command(f"SEND_ONCE {self.remote} {key} {repeat_count}")

    def press_and_wait(self, key: str):
        """
        Press the specified key and wait until the screen changes or stops changing.
        """

    def press_until_match(self, key, image):
        """
        Keep pressing key until we find the specified image.
        """
