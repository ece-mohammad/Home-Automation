#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import sys
import time
import logging as log
from http.server import HTTPServer, CGIHTTPRequestHandler
import config


# default server settings (IP/socket)
HOST_NAME = config.WEB_SERVER_CONFIG["IP"]
PORT_NUMBER = config.WEB_SERVER_CONFIG["PORT"]


# custom HTTP server class
class CustomHTTPServer(HTTPServer):

    def __init__(self, *args, **kwargs):

        self._server_address = kwargs.get("server_address", HOST_NAME)
        self._server_port = kwargs.get("server_port", PORT_NUMBER)
        self._request_handler = kwargs.get("request_handler", CGIHTTPRequestHandler)
        self._logger = log.getLogger("HTTPServer")

        HTTPServer.__init__(
            self,
            server_address=(self._server_address, self._server_port),
            RequestHandlerClass=self._request_handler
        )
        self._logger.debug("Initialized HTTP Server with params: {}".format(kwargs))

    def start(self):
        """
        Starts HTTP server
        :return: None
        """

        try:
            self._logger.info("Starting web server on address: {}:{}".format(self._server_address, self._server_port))
            self.serve_forever()

        except Exception as e:

            self._logger.critical("Server exception occurred: {}".format(e))

        finally:

            self.server_close()
            self._logger.info("Closing web server...")


if __name__ == '__main__':

    log.basicConfig(level=log.DEBUG, stream=sys.stdout)

    if len(sys.argv) == 1:

        httpd = CustomHTTPServer(
            server_address=HOST_NAME,
            server_port=PORT_NUMBER,
            request_handler=CGIHTTPRequestHandler
        )

        try:
            print(time.asctime(), 'HTTP Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
            httpd.serve_forever()

        except KeyboardInterrupt:
            pass

        finally:
            httpd.server_close()
            print(time.asctime(), 'HTTP Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))

        sys.exit(0)

    elif len(sys.argv) == 3:

        server_address = sys.argv[1]
        server_port = int(sys.argv[2])

        httpd = CustomHTTPServer(
            server_address=server_address,
            server_port=server_port,
            request_handler=CGIHTTPRequestHandler
        )

        try:
            print(time.asctime(), 'HTTP Server UP - %s:%s' % (server_address, server_port))
            httpd.serve_forever()

        except KeyboardInterrupt:
            pass

        finally:
            httpd.server_close()
            print(time.asctime(), 'HTTP Server DOWN - %s:%s' % (server_address, server_port))

        sys.exit(0)

    else:
        print("Invalid server address! Server requires an IP address and a port number!")
        sys.exit(-1)
