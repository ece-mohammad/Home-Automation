#!/usr/bin/env python3


import sys
import socket
import logging as log
import iot_message
import config


# remote host address
REMOTE_HOST_ADDRESS = config.TCP_SERVER_CONFIG["IP"]
REMOTE_HOST_PORT = config.TCP_SERVER_CONFIG["PORT"]


class MockTCPClient(object):

    def __init__(self, remote_address, remote_port):

        self._logger = log.getLogger("MockClient")
        self._remote_address = remote_address
        self._remote_port = remote_port

    def write(self, message):

        try:

            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.settimeout(3)
            send_socket.connect((self._remote_address, self._remote_port))
            send_socket.send(bytes(message + "\r\n", "utf-8"))

        except Exception as e:

            self._logger.critical("Couldn't connect to remote host on address: {} : {}".format(
                self._remote_address,
                self._remote_port
                )
            )
            print(e)
            sys.exit(-1)

        return None


if __name__ == '__main__':

    test_client = MockTCPClient(
        remote_address=REMOTE_HOST_ADDRESS,
        remote_port=REMOTE_HOST_PORT,
    )

    print("-----------------------------------------------")
    print("| ---------- IOT Server Tester -------------- |")
    print("-----------------------------------------------")

    while True:

        message_string = input("Enter message to send: ")

        test_client.write(message_string)

        print("*************************************************")

