#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import tcp_server
import config
import module_manager
import sys
import time
import subprocess
import threading as thread
import logging as log


class IOTServer(object):

    def __init__(self):

        # server state
        self._is_running = False

        # logger
        self._logger = log.getLogger("IOTServer")

        # get web server address
        self._web_sever_address = config.WEB_SERVER_CONFIG["IP"]

        # get web server port
        self._web_sever_port = config.WEB_SERVER_CONFIG["PORT"]

        # web server process id
        self._web_server_process = None

        # get TCP server address
        self._tcp_server_address = config.TCP_SERVER_CONFIG["IP"]
        self._tcp_server_port = config.TCP_SERVER_CONFIG["PORT"]

        # initialize TCP server instance
        self._tcp_server = tcp_server.CustomTCPServer(
            address=self._tcp_server_address,
            port=self._tcp_server_port,
        )

        # TCP server thread handler
        self._tcp_server_thread = None

        # initialize module manager instance
        self._module_manager = module_manager.ModuleManager()

        # module manager thread handler
        self._module_manager_thread = None

    def start(self):
        """
        Starts IOT server components
        :return: None
        """
        # set server state
        self._is_running = True

        # check if running on windows
        if sys.platform == "win32":

            self._web_server_process = subprocess.Popen(
                [
                    "python",
                    "webserver.py",
                    self._web_sever_address,
                    str(self._web_sever_port),
                ]
            )

        # start web server in a separate process
        else:

            self._web_server_process = subprocess.Popen(
                [
                    "python",
                    "webserver.py",
                    self._web_sever_address,
                    str(self._web_sever_port),
                ]
            )

        # start TCP server
        self._tcp_server_thread = thread.Thread(
            target=self._tcp_server.start,
            daemon=True,
            name="TCPServerThread"
        )
        self._tcp_server_thread.start()

        # connect buffers
        self._module_manager.message_queue = self._tcp_server.receiver_buffer
        self._module_manager.response_queue = self._tcp_server.transmit_buffer

        # start manager
        self._module_manager_thread = thread.Thread(
            target=self._module_manager.start,
            daemon=True,
            name="ModuleManagerThread"
        )
        self._module_manager_thread.start()

    def server_forever(self):
        """
        Keeps the server running indefinitely
        :return: None
        """
        while self._is_running:

            try:
                pass

            except Exception as e:
                pass

            finally:
                time.sleep(10)

    def teat_down(self):
        """
        Stops IOT server components
        :return: None
        """
        self._is_running = False
        self._web_server_process.kill()
        self._logger.debug("Closing server...")


if __name__ == '__main__':

    log.basicConfig(level=log.DEBUG)

    iot_sever = IOTServer()
    iot_sever.start()
    iot_sever.server_forever()

