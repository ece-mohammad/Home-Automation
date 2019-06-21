#!/usr/bin/env python3

__version__ = 1.2
__author__ = "Mohammad Mohsen"


import socket
from config import TCP_SERVER_CONFIG, NODE_CONFIG
import logging as log
import threading as thread
import queue
import time


class TCPMessage(object):

    def __init__(self, message, address):

        # ip of the message source or the destination
        self._address = address

        # message string
        self._message = message

    def set_message_string(self, message):
        """
        Sets message string
        :param message: (string) message string
        :return: None
        """
        self._message = message
        return None

    def get_message_string(self):
        """
        Gets message string
        :return: (string) message string
        """
        return self._message

    def set_destination(self, address):
        """
        Sets message source or destination
        :param address: (string) IP of the source/destination
        :return: None
        """
        self._address = address
        return None

    def get_message_address(self):
        """
        Gets address of the message source/destination
        :return: (string) IP
        """
        return self._address


class CustomTCPServer(object):

    def __init__(self, address, port):

        self._address = address
        self._port = port

        self._logger = log.getLogger("TCPServer")

        self.transmit_buffer = queue.Queue(maxsize=23)
        self.receiver_buffer = queue.Queue(maxsize=23)

        self._running = False

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._logger.debug("Initialized TCP server on address: ({}, {})".format(self._address, self._port))

    def send_message(self):
        """
        A method that runs as a daemon thread alongside thr server to send messages in transmit buffer
        :return: None
        """
        while self._running:

            try:

                message = self.transmit_buffer.get(block=True, timeout=1)
                assert isinstance(message, TCPMessage)

                remote_address = message.get_message_address()

                # TODO :: change remote port, 5070 is used to echo responses back to the server for debugging
                remote_port = NODE_CONFIG["SERVER_PORT"]
                # remote_port = 5070

                message_string = message.get_message_string()

                send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_socket.connect((remote_address, remote_port))
                send_socket.settimeout(5)
                send_socket.send(
                    bytes(message_string, "utf-8")
                )
                send_socket.close()

                self._logger.debug("Sent message string: {} to address: ({}, {})".format(
                        message_string,
                        remote_address,
                        remote_port
                    )
                )

            except queue.Empty:
                # self._logger.debug("Transmit queue is empty!")
                pass

            except AssertionError:
                self._logger.debug("Message object is not of the correct type: {}".format(message.__class__))

            except Exception as e:
                self._logger.error("Failed to send message: {} to ({}, {}) due to exception: {}".format(
                        message_string,
                        remote_address,
                        remote_port,
                        e,
                    )
                )

            finally:
                time.sleep(0.1)

    def receive_message(self):
        """
        A method that runs as a daemon thread alongside the server
        that receives message and pushes it in the receive buffer
        :return: None
        """
        while self._running:

            try:

                client_socket, (client_address, client_port) = self._server_socket.accept()

                request_string = client_socket.recv(1024).decode().strip()

                received_message = TCPMessage(
                    message=request_string,
                    address=client_address
                )

                self.receiver_buffer.put(received_message)

                self._logger.debug("Received message: {} from ({},{})".format(
                        request_string,
                        client_address,
                        client_port,
                    )
                )

            except Exception as e:
                print(e)

            finally:
                time.sleep(0.1)

    def server_forever(self):
        """
        Runs the server indefinitely
        :return: None
        """
        while self._running:
            time.sleep(10)

    def start(self):
        """
        Starts TCP server
        :return:
        """

        # change server state to running
        self._running = True

        self._logger.debug("Starting TCp server..")

        # bind to server address
        self._server_socket.bind((self._address, self._port))

        # start listening for connections (allow up to 23 connections)
        self._server_socket.listen(23)

        self._logger.debug("Server bound to its socket..")

        # start sender thread
        send_thread = thread.Thread(target=self.send_message, daemon=True, name="SenderThread")
        send_thread.start()

        self._logger.debug("Started send thread..")

        # start receiver thread
        receive_thread = thread.Thread(target=self.receive_message, daemon=True, name="ReceiveThread")
        receive_thread.start()

        self._logger.debug("Started receive thread..")


if __name__ == '__main__':

    log.basicConfig(level=log.DEBUG)

    test_server = CustomTCPServer(
        address=TCP_SERVER_CONFIG["IP"],
        port=TCP_SERVER_CONFIG["PORT"],
    )
    server_thread = thread.Thread(target=test_server.start, daemon=True, name="ServerThread")
    server_thread.start()
    test_server.server_forever()


