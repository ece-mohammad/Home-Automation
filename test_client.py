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

    import time

    test_client = MockTCPClient(
        remote_address=REMOTE_HOST_ADDRESS,
        remote_port=REMOTE_HOST_PORT,
    )

    # add module
    request = iot_message.IOTMessage()
    request.set_message_type(iot_message.REQUEST)
    request.set_operation(iot_message.ADD_NODE)
    request.set_source(iot_message.REMOTE_MODULE)
    request.set_data(
        {
            "id": "ilm_1_12345"
        }
    )
    _, request_string = request.stringfy()
    test_client.write(request_string)

    time.sleep(5)

    # update module data
    request = iot_message.IOTMessage()
    request.set_message_type(iot_message.REQUEST)
    request.set_operation(iot_message.UPDATE_DATA)
    request.set_source(iot_message.REMOTE_MODULE)
    request.set_data(
        {
            "id": "ilm_1_12345",
            "state": "on",
        }
    )
    _, request_string = request.stringfy()
    test_client.write(request_string)

    time.sleep(5)

    # update module data
    request = iot_message.IOTMessage()
    request.set_message_type(iot_message.REQUEST)
    request.set_operation(iot_message.UPDATE_DATA)
    request.set_source(iot_message.REMOTE_MODULE)
    request.set_data(
        {
            "id": "ilm_1_12345",
            "state": "off",
        }
    )
    _, request_string = request.stringfy()
    test_client.write(request_string)

    time.sleep(5)

    # update module data
    request = iot_message.IOTMessage()
    request.set_message_type(iot_message.REQUEST)
    request.set_operation(iot_message.REMOVE_NODE)
    request.set_source(iot_message.REMOTE_MODULE)
    request.set_data(
        {
            "id": "ilm_1_12345",
        }
    )
    _, request_string = request.stringfy()
    test_client.write(request_string)

    time.sleep(5)







