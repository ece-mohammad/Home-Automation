#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import sys
import os


# on linux systems, add parent folder directory to path
sys.path.insert(0, os.path.abspath("."))


import cgi
import cgitb
import socket
import iot_message
import iot_error
from module import Module
from config import TCP_SERVER_CONFIG


# enable CGI debugging
cgitb.enable()


def response(message="", redirect_time=3):
    """
    Update script response
    :return: (string) response page source code
    """
    source = """
    <html>
        <meta http-equiv="refresh" content="{redirect_time};url=/home.html">
        
        <body>
            <p>
            {message}
            Redirecting to homepage in {redirect_time} seconds.
            </p>
        </body>
    </html>
    
    """
    return source.format(message=message, redirect_time=redirect_time)


def main():

    """
    Make an update request with the module form data
    :return: (iot_error)
    """

    # module update status
    status = iot_error.FAILED

    # get module update from data
    form_data = cgi.FieldStorage()
    form_data = {key: form_data.getvalue(key) for key in form_data.keys()}

    # get module id
    module_name = form_data["id"]

    # module instance
    module = Module(name=module_name)

    # request message
    request_message = iot_message.IOTMessage()
    request_message.set_message_type(iot_message.REQUEST)
    request_message.set_operation(iot_message.UPDATE_DATA)
    request_message.set_source(iot_message.WEB_SERVER)
    request_message.set_data(
        dict(form_data)
    )

    # make request string
    status, request_message_string = request_message.stringfy()

    # get TCP server address
    remote_address = TCP_SERVER_CONFIG["IP"]

    # get TCP server port
    remote_port = TCP_SERVER_CONFIG["PORT"]

    # create TCP socket to send update request
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect socket to TCP server and send update request
    try:

        send_socket.connect((remote_address, remote_port))
        send_socket.settimeout(10)
        send_socket.send(
            bytes(request_message_string+"\r\n", "utf-8")
        )
        status = iot_error.SUCCESS

    except Exception as e:

        print("An exception occurred while sending update request from 'update_data.py' to IOT server")
        print("Exception:", e)
        status = iot_error.FAILED

    finally:
        send_socket.close()

    return status


print("Content-Type: text/html")
print('<meta charset="UTF-8">')
print()
update_status = main()

# check module update status
if update_status.code == iot_error.SUCCESS.code:
    response_message = response(message="Module update successfully.", redirect_time=10)

elif update_status.code == iot_error.UNSUPPORTED_MODULE.code:
    response_message = response(message="Unsupported module. Make sure the server is up to date!", redirect_time=10)

elif update_status.code == iot_error.UNREGISTERED_MODULE.code:
    response_message = response(message="Unregistered module. Register the module and try again!", redirect_time=10)

elif update_status.code == iot_error.MISSING_MODULE_ARGS.code:
    response_message = response(message="Missing module parameters!", redirect_time=10)

elif update_status.code == iot_error.MISSING_MODULE_ID.code:
    response_message = response(message="Missing module ID!", redirect_time=10)

elif update_status.code == iot_error.INVALID_DATA_FILED_VALUE.code:
    response_message = response(message="Invalid data field in module parameters", redirect_time=10)

elif update_status.code == iot_error.MISSING_MODULE_IP.code:
    response_message = response(message="Missing module IP!", redirect_time=10)

else:

    response_message = response(message="Module update failed!", redirect_time=10)
    print("Update status [{}]: {}".format(update_status.code, update_status.string))

print(response_message)

