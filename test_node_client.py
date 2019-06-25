#!/usr/bin/env python3


import socket
import config


class NodeClient(object):

    def __init__(self):
        # self._remote_address = "192.168.1.1"
        self._remote_address = config.TCP_SERVER_CONFIG["IP"]
        self._remote_port = config.TCP_SERVER_CONFIG["PORT"]

    def send_messge(self, message):
        """
        Sends a message to remote server
        :param message: (string) message to send
        :return: None
        """
        try:
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect((self._remote_address, self._remote_port))
            send_socket.send(
                bytes(message, "utf-8")
            )
        except Exception as e:
            print(e)

    def start(self):
        """
        Starts a console session to send messages to remote server
        :return: None
        """
        print("----------------------------------")
        print("| ----- Node Client Emulator ----|")
        print("----------------------------------")

        while True:

            message = input("Enter message to send or quit to exit: ").strip()

            if message == "quit":
                return None

            else:
                self.send_messge(message=message)
                print("**********************************")


if __name__ == '__main__':

    test_node_client = NodeClient()
    test_node_client.start()
