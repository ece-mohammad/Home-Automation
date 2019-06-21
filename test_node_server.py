#!/usr/bin/env python3


import socket
import config
import sys


class NodeServer(object):

    def __init__(self):
        self._server_address = socket.gethostbyname(socket.gethostname())
        self._server_port = config.NODE_CONFIG["PORT"]
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def server_forever(self):
        """
        Starts server indefinitely
        :return None
        """
        self._server_socket.bind((self._server_address, self._server_port))
        self._server_socket.listen(10)

        print("Started TCP server on ({}, {})...".format(
                self._server_address,
                self._server_port
            )
        )

        while True:

            try:
                client_socket, (client_address, client_port) = self._server_socket.accept()
                message = client_socket.recv(1024).decode().strip()

                print("Client: ({}, {}) sent message: {}".format(
                        client_address,
                        client_port,
                        message
                    )
                )

            except KeyboardInterrupt:

                self._server_socket.close()
                sys.exit(0)

            except Exception as e:
                print(e)


if __name__ == '__main__':

    test_node = NodeServer()
    test_node.server_forever()

