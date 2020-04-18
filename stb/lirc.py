import platform
import socket
import sys
import threading
from itertools import islice


class LircResponse:
    """
    A response from the LIRC daemon. Stores the command that had
    been sent, whether or not it was successful, and the parsed
    reply packet data.
    """

    def __init__(self, command: str, success: bool, data: list):
        self.command = command
        self.success = success
        self.data = data


class Lirc:
    """
    Communicate with the lircd daemon.

    More information on the lircd daemon, socket interface,
    reply package format, etc. can be found at https://www.lirc.org/html/lircd.html

    Example Usage:

        from stb.lirc import Lirc

        lirc = Lirc()
        response = lirc.version()

        print(response.command)
        >>> 'VERSION'
        print(response.success)
        >>> True
        print(response.data)
        >>> ['0.10.1']
    """

    DEFAULT_SOCKET_PATH = "/var/run/lirc/lircd"
    DEFAULT_PORT = 8765
    ENCODING = "utf-8"

    def __init__(self, lirc_socket_path: str = DEFAULT_SOCKET_PATH):
        """
        Initialize Lirc by connecting to the lircd socket.

        Currently, this will exit with a status code of 1 if the
        system running it is not a Linux system as support for
        connecting over TCP is not implemented yet (which is what
        you'd have to use on Windows if you use winLIRC).

        There is a port to macOS, but it doesn't seem to be maintained or
        work all that well last time I installed it using macports.
        https://github.com/andyvand/LIRC
        """
        system = platform.system()
        if system == "Linux":
            self.__lock = threading.Lock()
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(lirc_socket_path)
        else:
            print(f"The current system ({system}) is not supported.")
            sys.exit(1)

    def __send_command(self, command: str) -> LircResponse:
        """
        Send a command to lircd.

        A lock is setup for the purpose of ensuring we are the only
        ones accessing the socket during this send and released at
        the end.

        :param command: A command from the lircd socket command interface.
        See SOCKET COMMAND INTERFACE in https://www.lirc.org/html/lircd.html
        for more information.
        """
        if not command.endswith("\n"):
            command += "\n"

        try:
            self.__lock.acquire()
            self.socket.sendall(command.encode(self.ENCODING))

            reply_packet = self.__read_reply_packet()
            return self.__parse_reply_packet(reply_packet)
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

        :return: The contents of the reply packet from BEGIN to END as a str.
        """
        BUFFER_LENGTH = 256
        buffer = ""
        data = self.socket.recv(BUFFER_LENGTH)

        # Ignore recieve requests that the socket caches
        while "BEGIN" not in data.decode(self.ENCODING):
            data = self.socket.recv(BUFFER_LENGTH)

        buffer += data.decode(self.ENCODING)

        while not buffer.endswith("END\n"):
            data = self.socket.recv(BUFFER_LENGTH)
            buffer += data.decode(self.ENCODING)

        return buffer

    def __parse_reply_packet(self, packet: str) -> LircResponse:
        """
        Parse the reply packaet from lircd.

         The format of the reply packet is

            BEGIN
            <command>
            [SUCCESS|ERROR]
            [DATA
            n
            n lines of data]
            END
        """
        lines = packet.split("\n")
        current_index = 0
        response = LircResponse("", False, [])

        if lines[current_index] == "BEGIN":
            current_index += 1
        else:
            return response

        response.command = lines[current_index]
        current_index += 1

        response.success = True if lines[current_index] == "SUCCESS" else False
        current_index += 1

        if lines[current_index] == "END":
            return response
        elif lines[current_index] == "DATA":
            current_index += 1
            data_length = int(lines[current_index])
            current_index += 1
        else:
            raise ValueError(f"Unknown format for reply packet: \n{lines}")

        for line in islice(lines, current_index, current_index + data_length):
            response.data.append(line)

        return response

    def send_once(self, key: str, remote: str, repeat_count: int = 1):
        """
        Send an LIRC SEND_ONCE command.

        Structure of the command:
          * SEND_ONCE <remote-name> <key-name-from-remote-file> [repeat-count]

        The reason the optional repeat-count parameter isn't used in this implementaiton
        is because we want to be able to store all the responses from each command.

        :param key: The name of the key to send.
        :param remote: The remote to use keys from.
        :param repeat_count: The number of times to press this key.

        :return: a LircResponse or a list of LircResponses if repeat_count > 1.
        :rtype: LircResponse or list
        """
        if repeat_count > 1:
            responses = []

            while repeat_count > 0:
                responses.append(self.__send_command(f"SEND_ONCE {remote} {key}"))
                repeat_count -= 1

            return responses

        return self.__send_command(f"SEND_ONCE {remote} {key}")

    def send_start(self, key: str, remote: str) -> LircResponse:
        """
        Send an LIRC SEND_START command.

        Structure of the command:
          * SEND_START <remote-name> <key-name-from-remote-file>

        :param key: The name of the key to start sending.
        :param remote: The remote to use keys from.
        """
        return self.__send_command(f"SEND_START {remote} {key}")

    def send_stop(self, key: str, remote: str) -> LircResponse:
        """
        Send an LIRC SEND_STOP command.

        Structure of the command:
          * SEND_STOP <remote-name> <key-name-from-remote-file>

        :param key: The name of the key to start sending.
        :param remote: The remote to use keys from.
        """
        return self.__send_command(f"SEND_STOP")

    def list_remotes(self) -> LircResponse:
        """List all the remotes in LIRC"""
        return self.__send_command("LIST")

    def list_remote_keys(self, remote: str) -> LircResponse:
        """List all the keys for a specific remote"""
        return self.__send_command(f"LIST {remote}")

    def set_inputlog(self, path: str) -> LircResponse:
        """Set the path to log all lircd received data to"""
        return self.__send_command(f"SET_INPUTLOG {path}")

    def stop_inputlog(self) -> LircResponse:
        """
        Stop logging to the inputlog path from set_inputlog.

        When calling SET_INPUTLOG without the path argument,
        it will stop logging and close the logfile.
        """
        return self.__send_command("SET_INPUTLOG")

    def version(self) -> LircResponse:
        """Retrieve the version of LIRC"""
        return self.__send_command("VERSION")
