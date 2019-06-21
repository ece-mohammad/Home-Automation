#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import os
import json
import iot_error
from shutil import rmtree
import logging as log
import iot_message
import queue
from tcp_server import TCPMessage
import time
import threading as thread
from module import Module

from templates.ilm import ilm_data_update
from templates.acm import acm_data_update
from templates.fpm import fpm_data_update


class ModuleManager(object):
    """
    Handles IOT modules operations (adding modules to the system, removing modules, updating module data)
    and processing request messages to perform one of the previous tasks.
    """
    def __init__(self):
        self._logger = log.getLogger("ModuleManager")
        self._parent_dir = os.getcwd()
        self._modules_dir = os.path.join(self._parent_dir, "modules")
        self._templates_dir = os.path.join(self._parent_dir, "templates")
        self.message_queue = queue.Queue(maxsize=23)
        self.response_queue = queue.Queue(maxsize=23)
        self._running = False
        self._num_of_workers = 5
        self._workers = dict()

    def check_module_version(self, module):
        """
        Checks module version
        :param module:
        :return: (iot_error) status code that indicates if the module version is supported or not
        """
        # return status
        status = iot_error.FAILED

        # get module type
        module_type = module.get_module_type()

        # check module type
        if module_type:

            # get module info.json file
            module_info_path = os.path.join(self._templates_dir, module_type, "info.json")

            # check module info.json file
            if os.path.exists(module_info_path) and os.path.isfile(module_info_path):

                # read info.json file
                with open(module_info_path, 'r') as fh:
                    info = fh.read().strip()

                # get version info.json
                version_info = json.loads(info).get("version", None)

                # check version_info
                if version_info is not None:

                    version_info = str(version_info).zfill(3)

                    # get module version
                    module_version = module.get_module_version()

                    # compare module version with version from info.json file
                    # (backward compatibility with older versions)
                    if module_version <= version_info:
                        status = iot_error.SUCCESS

                    # if module version is not supported
                    else:
                        status = iot_error.UNSUPPORTED_MODULE_VERSION

                # version_info is None (info.json doesn't gave version field)
                else:
                    self._logger.debug("Version info is missing for module: {}".format(module_type))

            # info file doesn't exist
            else:
                self._logger.debug("Info file is missing for module: {}".format(module_type))

        # if module type is missing or is missing
        else:
            self._logger.debug("Module type is missing or is none: {}".format(module_type))

        return status

    def check_module_support(self, module):
        """
        Checks module support (version and support)
        :param module: Module to check if it's supported by the server
        :return: (iot_error) module support check result
        """
        status = iot_error.FAILED

        # get module type (short name)
        module_type = module.get_module_type()

        # check module type
        if module_type:

            # check if module type is in templates
            if module_type in os.listdir(self._templates_dir):

                # check if the module version is supported
                status = self.check_module_version(module=module)

            # module not in templates folder
            else:
                status = iot_error.UNSUPPORTED_MODULE

        # module type is missing or is None
        else:
            self._logger.debug("module type is missing or is none: {}".format(module_type))

        return status

    def check_module_registration(self, module):
        """
        Checks if a given module is already registered on the server
        :param module: Module to check
        :return: (iot_error) module registration check result
        """
        # return status
        status = iot_error.FAILED

        # get module name
        module_name = module.get_module_name()

        # module directory
        module_directory = os.path.join(self._modules_dir, module_name)

        # check if module is registered
        if os.path.exists(module_directory) and os.path.isdir(module_directory):
            status = iot_error.SUCCESS

        # if module is not registered
        else:
            status = iot_error.UNREGISTERED_MODULE

        return status

    def add_module(self, module_data):
        """
        Add a module to the server
        :param module_data: Module to add
        :return: (iot_error) status indicating if module was added or not
        """

        assert isinstance(module_data, dict)

        self._logger.debug("Adding module: {}".format(module_data))

        # return status
        status = iot_error.FAILED

        # get module name
        module_name = module_data["id"]

        # get module address
        module_address = module_data["ip"]

        # make module instance
        module = Module(name=module_name)

        # check module_data registration
        if self.check_module_registration(module).code == iot_error.UNREGISTERED_MODULE.code:

            # check module_data support
            if self.check_module_support(module).code == iot_error.SUCCESS.code:

                # get module_data type
                module_type = module.get_module_type()

                # get module html template file
                module_temp_html_file = os.path.join(self._templates_dir, module_type, module_type+"_html_temp.html")

                # get module data template file
                module_temp_data_file = os.path.join(self._templates_dir, module_type, module_type + "_data_temp.json")

                # get module directory
                module_directory = module_data["module_directory"]

                # get module html file
                module_html_file = module_data["module_html_file"]

                # get module data file
                module_data_file = module_data["module_data_file"]

                # make module_data directory
                os.mkdir(module_directory)

                # make module_data html file
                with open(module_temp_html_file, 'r') as fh:
                    module_html = fh.read().strip().format(id=module_name)

                with open(module_html_file, 'w') as fh:
                    fh.write(module_html)

                # make module_data data file
                with open(module_temp_data_file, 'r') as fh:
                    module_data = json.loads(fh.read().strip())

                # update module address
                module_data["ip"] = module_address

                with open(module_data_file, 'w') as fh:
                    fh.write(json.dumps(module_data))

                status = iot_error.SUCCESS

            # unsupported module_data
            else:
                status = iot_error.UNSUPPORTED_MODULE

        # module_data is already registered
        else:

            # # TODO:: Test module volatility
            #
            # # check module volatility
            #
            # # get module type
            # module_type = module.get_module_type()
            #
            # # get module info file
            # module_info_file = os.path.join(self._templates_dir, module_type, "info.json")
            #
            # # check if module info file exists
            # if os.path.exists(module_info_file) and os.path.isfile(module_info_file):
            #
            #     # get module info
            #     with open(module_info_file, 'r') as fh:
            #         module_info = json.loads(fh.read().strip())
            #
            #     # get module volatility info
            #     module_volatility = module_info["volatile"]
            #
            #     # check if module is volatile
            #     if module_volatility:
            #
            #         # remove module
            #         self.remove_module(module_data=module_data)
            #
            #         # add module
            #         status = self.add_module(module_data=module_data)
            #
            #     # module is not volatile
            #     else:
            #         status = iot_error.SUCCESS
            #
            # # module info file doesn't exist
            # else:
            #     status = iot_error.MISSING_MODULE_INFO_FILE

            status = iot_error.SUCCESS

        return status

    def remove_module(self, module_data):
        """
        Removes a given module from the server
        :param module_data: Module to remove
        :return: (iot_error) a status indicating if the module was removed or not
        """
        assert isinstance(module_data, dict)

        # error code
        status = iot_error.FAILED

        # get module_data name
        module_name = module_data["id"]

        # module instance
        module = Module(name=module_name)

        # check if module_data is registered
        if self.check_module_registration(module):

            # module_data directory
            module_directory = module_data["module_directory"]

            # remove module_data directory and its contents
            rmtree(module_directory)

            # set status to success
            status = iot_error.SUCCESS

        else:
            status = iot_error.UNREGISTERED_MODULE

        return status

    def update_module_data(self, module_data):
        """
        Updates module data
        :param module_data: Module data to update. It contains the module id, request origin address and parsed
        module data
        :return: (iot_error) a status indicating if the module data was updated or not
        """
        assert isinstance(module_data, dict)

        # status code
        status = iot_error.FAILED

        # get module name
        module_name = module_data.get("id")

        # module instance
        module = Module(name=module_name)

        # get module type
        module_type = module.get_module_type()

        # check if module is registered
        if self.check_module_registration(module).code == iot_error.SUCCESS.code:

            # check module support
            if self.check_module_support(module).code == iot_error.SUCCESS.code:

                # check for ilm module
                if module_type == "ilm":
                    status = ilm_data_update.update(module_data)

                # check for acm module
                elif module_type == "acm":
                    status = acm_data_update.update(module_data)

                # check for fpm module
                elif module_type == "fpm":
                    status = fpm_data_update.update(module_data)

            # unsupported module
            else:
                status = iot_error.UNSUPPORTED_MODULE

        # module is not registered before
        else:
            status = iot_error.UNREGISTERED_MODULE

        return status

    def process_message(self):
        """
        Processes a  message from message queue
        :return: None
        """

        while self._running:

            try:

                # get message from message queue
                message = self.message_queue.get(block=True, timeout=1)

                assert isinstance(message, TCPMessage)

                self._logger.debug("[{}]::Processing message: {}".format(
                        thread.current_thread(),
                        message.get_message_string()
                    )
                )

                # status
                status = iot_error.FAILED

                # get message string
                message_string = message.get_message_string()

                # get message address
                message_address = message.get_message_address()

                # validate message string
                validation_result, parsed_message = iot_message.IOTMessage.parse_message_string(message_string)

                # check if message string is valid
                if validation_result.code == iot_error.SUCCESS.code:

                    # get message type
                    message_type = parsed_message.get_message_type()

                    # get message data
                    message_data = parsed_message.get_data()

                    # add message address to message data
                    message_data["ip"] = message_address

                    # update parsed message data with message address
                    # (required for add_node method)
                    parsed_message.set_data(message_data)

                    # check for request message
                    if message_type == iot_message.REQUEST:
                        status = self.process_request(parsed_message)

                    # check for response message
                    elif message_type == iot_message.RESPONSE:
                        status = self.process_response(parsed_message)

                # message string is invalid
                else:
                    status = validation_result

                # log message processing status
                self._logger.debug("[{}]::Message processing status: {}".format(thread.current_thread(), status.string))

            except queue.Empty:
                # self._logger.debug("[{}] :: Message queue is empty".format(thread.current_thread()))
                pass

    def process_request(self, request):
        """
        Process a given request
        :param request: (iot_message) request message with an operation to perform
        :return: (iot_error)
            iot_error: request processing status
        """
        assert isinstance(request, iot_message.IOTMessage)

        # status
        status = iot_error.FAILED

        # build response message
        response = iot_message.IOTMessage()
        response.set_source(iot_message.TCP_SERVER)

        # get request type
        request_type = request.get_operation()

        # get request data
        request_data = request.get_data()

        # get module name
        module_name = request_data.get("id")

        # module instance
        module = Module(name=module_name)

        # get module type
        module_type = module.get_module_type()

        # get module directory
        module_directory = os.path.join(self._modules_dir, module_name)

        # get module data file
        module_data_file = os.path.join(self._modules_dir, module_name, module_type+".json")

        # get module html file
        module_html_file = os.path.join(self._modules_dir, module_name, module_type + ".html")

        # add module files to request data
        request_data["module_directory"] = module_directory
        request_data["module_data_file"] = module_data_file
        request_data["module_html_file"] = module_html_file

        # update request data
        request.set_data(request_data)

        # get module address (to send response to it)
        module_address = request_data.get("ip")

        # check for node add request
        if request_type == iot_message.ADD_NODE:
            status = self.add_module(request_data)

        # check for node remove request
        elif request_type == iot_message.REMOVE_NODE:
            status = self.remove_module(request_data)

        # check for data update request
        elif request_type == iot_message.UPDATE_DATA:
            status = self.update_module_data(request_data)

        """     build response message      """

        if (request_type == iot_message.ADD_NODE) or (request_type == iot_message.REMOVE_NODE):

            # get module address
            module_address = request_data.get("ip")

            # complete response message
            response.set_message_type(iot_message.RESPONSE)
            response.set_source(iot_message.TCP_SERVER)
            response.set_operation(status.string)
            response.set_data(
                {
                    "reason": status.string,
                }
            )

        elif request_type == iot_message.UPDATE_DATA:

            # get module IP from local data file
            module_data_file = os.path.join(self._modules_dir, module_name, module_type + ".json")

            # load module data
            with open(module_data_file, 'r') as fh:
                module_data = json.loads(fh.read().strip())

            # get request source
            request_source = request.get_source()

            # check request source
            # (WEB_SERVER means that the request was sent by a CGI script, so
            # the IP passed with the request is the web server's IP and not the module's actual IP)
            if request_source == iot_message.WEB_SERVER:

                module_address = module_data.get("ip")
                response_data = module_data

                # add module id to response data
                response_data["id"] = module_name

                # remove node IP from response data
                del response_data["ip"]

                # build response
                response.set_message_type(iot_message.REQUEST)
                response.set_operation(iot_message.UPDATE_DATA)
                response.set_data(response_data)

            else:
                response.set_message_type(iot_message.RESPONSE)
                response.set_operation(status.string)
                response.set_data(
                    {
                        "reason": status.string,
                    }
                )
                module_address = request_data.get("ip")

        # build response string
        response_validation, response_string = response.stringfy()

        # build TCP message for response
        response = TCPMessage(
            address=module_address,
            message=response_string,
        )

        # send response
        self.send_message(response)

        return status

    def process_response(self, response):
        """
        Process a given response, usually, by logging it to the system log
        :param response: (iot_message) response message
        :return: (iot_error) status
        """
        assert isinstance(response, iot_message.IOTMessage)

        status = iot_error.SUCCESS

        # log response to system
        self._logger.info("Received response: {}".format(response))

        return status

    def send_message(self, message):
        """
        Sends a message to TCP server.
        :param message: (iot_message) Message to send to TCP server
        :return: (iot_error) status indicating if the message was sent or not
        """
        # status
        status = iot_error.FAILED

        try:

            assert isinstance(message, TCPMessage)

            self.response_queue.put(message, False)

            self._logger.debug("Sent message: {}".format(message.get_message_string()))

            status = iot_error.SUCCESS

        except queue.Full:
            self._logger.debug("Failed to enqueue response! Response queue is full!!")

        except AssertionError:
            self._logger.debug("Passed message object is of invalid type: {}".format(message.__class__))

        return status

    def start(self):
        """
        Starts module manager
        :return: None
        """
        # set state to running
        self._running = True

        self._logger.debug("Staring module manager...")

        # spawn worker threads
        for worker in range(self._num_of_workers):

            worker_id = "WorkerThread_"+str(worker)
            worker = thread.Thread(target=self.process_message, name=worker_id)
            self._workers[worker_id] = worker
            worker.start()
            worker.join()


            time.sleep(1)

    def stop(self):
        """
        Stops module manager
        :return:
        """
        # set state to stop
        self._running = False

        # wait till all threads are done
        while thread.active_count() > 1:
            time.sleep(0.1)

        return None


if __name__ == '__main__':

    from module import Module
    import logging as log

    # configure logging level
    log.basicConfig(level=log.DEBUG)

    mod_mgr = ModuleManager()

    testing = 1

    if testing == 0:

        # add module
        add_message = TCPMessage(
            message="1102id=ilm_1_123",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(add_message)

        # remove module
        remove_message = TCPMessage(
            message="1202id=ilm_1_123",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(remove_message)

    elif testing == 1:

        # add module
        add_message = TCPMessage(
            message="1102id=ilm_1_123",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(add_message)

        # update module data
        update_data = TCPMessage(
            message="1302id=ilm_1_123&state=on",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(update_data)

    elif testing == 2:

        # add module
        add_message = TCPMessage(
            message="1102id=ilm_1_123",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(add_message)

        # update module data
        update_data = TCPMessage(
            message="1302id=ilm_1_123",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(update_data)

    elif testing == 3:

        # add module
        add_message = TCPMessage(
            message="1102id=ilm_1_123",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(add_message)

        # update module data
        update_data = TCPMessage(
            message="1302id=ilm_1_123&state=standby",
            address="192.168.137.1"
        )
        mod_mgr.message_queue.put(update_data)

    # start module manager
    mod_mgr.start()

