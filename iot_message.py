#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import iot_error
import auxiliary_tools


"""     message types       """
REQUEST = "REQUEST"
RESPONSE = "RESPONSE"

"""     request messages        """
ADD_NODE = "ADD_NODE"
REMOVE_NODE = "REMOVE_NODE"
UPDATE_DATA = "UPDATE_DATA"

"""     message Sources     """
REMOTE_MODULE = "REMOTE_MODULE"
LOCAL_SCRIPT = "LOCAL_SCRIPT"

"""     general response messages       """
SUCCESS = iot_error.SUCCESS.string
FAILED = iot_error.FAILED.string
INVALID_MESSAGE_FORMAT = iot_error.INVALID_MESSAGE_FORMAT


"""     message specific response messages      """
INVALID_MESSAGE_OBJECT = iot_error.INVALID_MESSAGE_OBJECT.string
UNKNOWN_MESSAGE_TYPE = iot_error.UNKNOWN_MESSAGE_TYPE.string
UNKNOWN_REQUEST = iot_error.UNKNOWN_REQUEST.string
UNKNOWN_RESPONSE = iot_error.UNKNOWN_RESPONSE.string

"""     module specific response messages       """
UNSUPPORTED_MODULE = iot_error.UNSUPPORTED_MODULE.string
UNSUPPORTED_MODULE_VERSION = iot_error.UNSUPPORTED_MODULE_VERSION.string
UNREGISTERED_MODULE = iot_error.UNREGISTERED_MODULE.string
MISSING_MODULE_ID = iot_error.MISSING_MODULE_ID.string
INVALID_DATA_FILED_VALUE = iot_error.INVALID_DATA_FILED_VALUE.string
MISSING_MODULE_ARGS = iot_error.MISSING_MODULE_ARGS.string
UNKNOWN_SOURCE = iot_error.UNKNOWN_SOURCE.string
MISSING_MESSAGE_SOURCE = iot_error.MISSING_MESSAGE_SOURCE.string

"""     internal errors response messages       """
MISSING_MODULE_HTML_TEMPLATE = iot_error.MISSING_MODULE_HTML_TEMPLATE.string
MISSING_MODULE_DATA_TEMPLATE = iot_error.MISSING_MODULE_DATA_TEMPLATE.string
MISSING_MODULE_HTML_FILE = iot_error.MISSING_MODULE_HTML_FILE.string
MISSING_MODULE_DATA_FILE = iot_error.MISSING_MODULE_DATA_FILE.string
MISSING_MODULE_IP = iot_error.MISSING_MODULE_IP.string


class IOTMessage(object):
    """
    A class that handles message formatting and parsing
    """

    """     Message Sources     """
    _SOURCES = {
        LOCAL_SCRIPT: 1,
        REMOTE_MODULE: 2,
    }

    """     Message Types       """
    _MESSAGE_TYPES = {
        REQUEST: 1,
        RESPONSE: 2,
    }

    """     Requests        """
    _REQUESTS = {
        ADD_NODE: 10,
        REMOVE_NODE: 20,
        UPDATE_DATA: 30,
    }

    """     Responses       """
    _RESPONSES = {
        SUCCESS: iot_error.SUCCESS.code,
        FAILED: iot_error.FAILED.code,
        INVALID_MESSAGE_FORMAT: iot_error.INVALID_MESSAGE_FORMAT.code,

        INVALID_MESSAGE_OBJECT: iot_error.INVALID_MESSAGE_OBJECT.code,
        UNKNOWN_MESSAGE_TYPE: iot_error.UNKNOWN_MESSAGE_TYPE.code,
        UNKNOWN_REQUEST: iot_error.UNKNOWN_REQUEST.code,
        UNKNOWN_RESPONSE: iot_error.UNKNOWN_RESPONSE.code,

        UNSUPPORTED_MODULE: iot_error.UNSUPPORTED_MODULE.code,
        UNSUPPORTED_MODULE_VERSION: iot_error.UNSUPPORTED_MODULE_VERSION.code,
        UNREGISTERED_MODULE: iot_error.UNREGISTERED_MODULE.code,
        MISSING_MODULE_ID: iot_error.MISSING_MODULE_ID.code,
        UNKNOWN_SOURCE: iot_error.UNKNOWN_SOURCE.code,
        MISSING_MESSAGE_SOURCE: iot_error.MISSING_MESSAGE_SOURCE.code,
        MISSING_MODULE_ARGS: iot_error.MISSING_MODULE_ARGS.code,
        INVALID_DATA_FILED_VALUE: iot_error.INVALID_DATA_FILED_VALUE.code,

        MISSING_MODULE_HTML_TEMPLATE: iot_error.MISSING_MODULE_HTML_TEMPLATE.code,
        MISSING_MODULE_DATA_TEMPLATE: iot_error.MISSING_MODULE_DATA_TEMPLATE.code,
        MISSING_MODULE_HTML_FILE: iot_error.MISSING_MODULE_HTML_FILE.code,
        MISSING_MODULE_DATA_FILE: iot_error.MISSING_MODULE_DATA_FILE.code,
        MISSING_MODULE_IP: iot_error.MISSING_MODULE_IP.code,

    }

    def __init__(self, *args, **kwargs):

        self._operation = kwargs.get("operation", None)
        self._type = kwargs.get("type", None)
        self._data = kwargs.get("data", None)
        self._src = kwargs.get("src", None)

    def set_message_type(self, msg_type):
        """
        Sets message type.
        :param msg_type: (string) Message type [REQUEST, RESPONSE]
        :return: None
        """
        self._type = msg_type

    def get_message_type(self):
        """
        Gets message type
        :return: (string) current message type (self._type)
        """
        return self._type

    def set_operation(self, operation):
        """
        Stes message operation (purpose of request or response)
        :param operation: (string) operation
        for request message type: [ "ADD_NODE", "REMOVE_NODE", "UPDATE_DATA"]
        for response message type: ["OK", "NOK", "REGISTRATION_COMPLETE", "UNREGISTRATION_COMPLETE",
          "DATA_UPDATE_COMPLETE", "UNKNOWN_MESSAGE_TYPE", "UNKNOWN_REQUEST_TYPE", "UNKNOWN_RESPONSE_TYPE"
          "UNKNOWN_NODE_ID", "UNKNOWN_DATA_FIELD", "MISSING_DATA_FIELD", "CORRUPT_DATA" ]
        :return: None
        """
        self._operation = operation

    def get_operation(self):
        """
        Gets operation type
        :return: (string) current operation type (self._operation)
        """
        return self._operation

    def set_data(self, data):
        """
        Sets message data
        :param data: (dict) Message data as a dictionary in key, value pairs
        :return: None
        """
        self._data = data

    def get_data(self):
        """
        Gets current message data
        :return: (dict) current message data (self._data)
        """
        return self._data

    def set_source(self, src):
        """
        Sets message sender IP
        :param src: Sender IP
        :return: None
        """
        self._src = src

    def get_source(self):
        """
        Gets message sender IP
        :return: (string) message sender IP
        """
        return self._src

    def validate_message_fields(self):
        """
        Validate message (message, message type and message operation)
        should be done before serialization to avoid formatting errors.
        :return: (iot_error) message validation result
        """

        # validation status
        status = iot_error.FAILED

        # check for request message type
        if self._type == REQUEST:

            # check request type
            if IOTMessage._REQUESTS.get(self._operation, None):

                # check source
                if IOTMessage._SOURCES.get(self._src, None):

                    # check data and  id field
                    if isinstance(self._data, dict) and self._data.get("id", None):
                        status = iot_error.SUCCESS

                    # missing data filed
                    else:
                        status = iot_error.MISSING_MODULE_ID

                # invalid source
                else:
                    status = iot_error.UNKNOWN_SOURCE

            # unknown request
            else:
                status = iot_error.UNKNOWN_REQUEST

        # check for response operation
        elif self._type == RESPONSE:

            # check response type
            if IOTMessage._RESPONSES.get(self._operation, None):

                # check message source
                if IOTMessage._SOURCES.get(self._src, None):

                    # check response msg_data
                    if isinstance(self._data, dict):
                        status = iot_error.SUCCESS

                    # invalid data
                    else:
                        status = iot_error.INVALID_DATA_FILED_VALUE

                # invalid message source
                else:
                    status = iot_error.UNKNOWN_SOURCE

            # unknown response
            else:
                status = iot_error.UNKNOWN_RESPONSE

        # invalid message type
        else:
            status = iot_error.UNKNOWN_MESSAGE_TYPE

        return status

    def stringfy(self):
        """
        Formats the message into a string
        :return: (iot_error, string) status and string of the formatted message
        """
        # message
        message_string = ""

        # status
        status = iot_error.FAILED

        # validate message fields
        message_validation_result = self.validate_message_fields()

        # check message fields
        if message_validation_result.code == iot_error.SUCCESS.code:

            # check for request message
            if self._type == REQUEST:

                # construct data string
                data_string = ""

                for key in self._data.keys():
                    data_string += "{}={}&".format(key, self._data[key])

                data_string = data_string[:-1]

                # construct message string
                message_string = "{}{}{}{}".format(
                    IOTMessage._MESSAGE_TYPES[self._type],
                    IOTMessage._REQUESTS[self._operation],
                    IOTMessage._SOURCES[self._src],
                    data_string
                )

                status = iot_error.SUCCESS

            # check for response message
            elif self._type == RESPONSE:

                data_string = ""

                for key in self._data.keys():
                    data_string += "{}={}&".format(key, self._data[key])

                data_string = data_string[:-1]

                message_string = "{}{}{}{}".format(
                    IOTMessage._MESSAGE_TYPES[self._type],
                    IOTMessage._RESPONSES[self._operation],
                    IOTMessage._SOURCES[self._src],
                    data_string,
                )

                status = iot_error.SUCCESS

            # invalid message type
            else:
                status = iot_error.UNKNOWN_MESSAGE_TYPE

        # invalid message fields
        else:
            status = iot_error.MISSING_MODULE_ID

        return status, message_string

    @classmethod
    def validate_message_string(cls, message_str):
        """
        Validates message string
        :param message_str: message string to validate
        :return: (iot_error) status indicating string validation result
        """
        # status
        status = iot_error.FAILED

        # transform the message string into lower case
        message_str = message_str.lower()

        # map message types codes to message types strings
        message_types = {v: k for (k, v) in cls._MESSAGE_TYPES.items()}

        # map request types codes to request types strings
        response_messages = {v: k for (k, v) in cls._RESPONSES.items()}

        # map response types codes to response types strings
        request_messages = {v: k for (k, v) in cls._REQUESTS.items()}

        # map message sources codes to message sources strings
        sources = {v: k for (k, v) in cls._SOURCES.items()}

        # check message string length
        # 4 being the shortest message, corresponding to a response message from a node
        # 2101
        # (2) response message
        # (10) success response
        # (1) sent by server
        if len(message_str) < 4:

            # invalid message format
            status = iot_error.INVALID_MESSAGE_FORMAT

        # message is string might be of sufficient length
        else:

            # get message type
            message_type = int(message_str[0])

            # get message operation
            message_operation = int(message_str[1:3])

            # get message source
            message_source = message_str[3]

            if message_source.isdigit():

                message_source = int(message_source)

                # check for request message
                if message_types.get(message_type, None) == REQUEST:

                    # check request message length
                    # min request length:16
                    # 1 char for message type (request)
                    # 2 char for request operation
                    # 1 char for request source (origin)
                    # 3 chars for id=
                    # minimum id length: 9 [3 chars for name, _ , 1 char for version, _, 3 chars for id]
                    # total = 9 + 3 + 4 = 16 characters
                    # ex: 1102id=ilm_1_123
                    if len(message_str) < 16:
                        status = iot_error.INVALID_MESSAGE_FORMAT

                    # valid request message length
                    else:

                        # check request operation
                        if request_messages.get(message_operation, None):

                            # check message source
                            if sources.get(message_source, None):

                                msg_data_str = message_str[4:]

                                # validate message data
                                data_validation = auxiliary_tools.valid_query_data(msg_data_str)

                                # validate data
                                if data_validation[0]:

                                    # check for module id
                                    if data_validation[1]:
                                        status = iot_error.SUCCESS

                                    # missing module id
                                    else:
                                        status = iot_error.MISSING_MODULE_ID

                                # data length is insufficient
                                else:
                                    status = iot_error.INVALID_MESSAGE_FORMAT

                            # invalid message source
                            else:
                                status = iot_error.UNKNOWN_SOURCE

                        # unknown request
                        else:
                            status = iot_error.UNKNOWN_REQUEST

                # check for response message
                elif message_types.get(message_type, None) == RESPONSE:

                    # check response operation
                    if response_messages.get(message_operation):
                        status = iot_error.SUCCESS

                    # invalid response
                    else:
                        status = iot_error.UNKNOWN_RESPONSE

                # invalid message type
                else:
                    status = iot_error.UNKNOWN_MESSAGE_TYPE

            # no message source, so 4th character is id's 'i'
            elif message_source == 'i':
                status = iot_error.MISSING_MESSAGE_SOURCE

            # 4th character is not a number not an 'i', probably an invalid message format
            else:
                status = iot_error.INVALID_MESSAGE_FORMAT

        return status

    @classmethod
    def parse_message_string(cls, message_str):
        """
        Parses a message string, creating a new message object from the passed string
        :return: (iot_error, IOTMessage) status code for string parsing result
            and the message object from the parsed string
        """

        # transform message string into lower case
        message_str = message_str.strip().lower()

        # message object to save parsed message
        message = IOTMessage()

        # map message types codes to message types strings
        message_types = {v: k for (k, v) in cls._MESSAGE_TYPES.items()}

        # map requests codes to requests strings
        request_messages = {v: k for (k, v) in cls._REQUESTS.items()}

        # map responses codes to responses strings
        response_messages = {v: k for (k, v) in cls._RESPONSES.items()}

        # map message sources codes to message sources strings
        sources = {v: k for (k, v) in cls._SOURCES.items()}

        # string validation status
        string_validation = cls.validate_message_string(message_str)

        # check message string
        if string_validation.code == iot_error.SUCCESS.code:

            # get message type
            message_type = int(message_str[0])

            # get message operation
            message_operation = int(message_str[1:3])

            # get message source
            message_source = int(message_str[3])

            # an empty dict to save mesaage data
            msg_data = dict()

            # check for request message
            if message_types.get(message_type, None) == REQUEST:

                # set message type
                message.set_message_type(message_types.get(message_type))

                # set message operation
                message.set_operation(request_messages.get(message_operation))

                # set message source
                message.set_source(sources.get(message_source))

                # get data string
                data_str = message_str[4:]

                # split message data around '&'
                parsed_data = data_str.split("&")

                # iterate over key_n=value_n parameters
                for param in parsed_data:

                    # split parameters around '=' ino key, value pairs
                    param = param.split("=")

                    # add key:pair to data dictionary
                    msg_data[param[0]] = param[1]

                # add data dictionary to message
                message.set_data(msg_data)

                status = iot_error.SUCCESS

            # check for response message
            elif message_types.get(message_type, None) == RESPONSE:

                # set message type
                message.set_message_type(message_types.get(message_type))

                # set message operation
                message.set_operation(response_messages.get(message_operation))

                # set message source
                message.set_source(sources.get(message_source))

                # check for response data
                if len(message_str) > 4:

                    message_data = dict()

                    # get response message data
                    response_data_string = message_str[4:]

                    response_data_string = response_data_string.split("&")

                    for pair in response_data_string:

                        pair = pair.split("=")
                        message_data[pair[0]] = pair[1]

                    message.set_data(message_data)

                    status = iot_error.SUCCESS

        return string_validation, message

    def __str__(self):
        _message_string = "Message Info:\n\tType: {}\n\tOperation: {}\n\tSource: {}\n\tData: {}".format(
            self.get_message_type(),
            self.get_operation(),
            self.get_source(),
            self.get_data()
        )
        return _message_string


if __name__ == '__main__':

    test_cases = 1

    if test_cases == 1:

        # uninitialized request
        test_request = IOTMessage()
        print(">>> uninitialized message")
        print(test_request)
        print(test_request.validate_message_fields())
        print("-------------------------------------")

        # initialized request
        test_request.set_message_type(REQUEST)
        test_request.set_operation(ADD_NODE)
        test_request.set_source(REMOTE_MODULE)
        test_request.set_data(
            {
                "id": "ilm_001_123",
                "state": "on",
            }
        )
        print(">>> request message")
        print(test_request)
        print(test_request.validate_message_fields())
        print("-------------------------------------")

        # initialized response
        test_response = IOTMessage()
        test_response.set_message_type(RESPONSE)
        test_response.set_operation(SUCCESS)
        test_response.set_source(REMOTE_MODULE)
        test_response.set_data(
            {
                "reason": iot_error.SUCCESS.string,
            }
        )
        print(">>> response message")
        print(test_response)
        print(test_response.validate_message_fields())
        print("-------------------------------------")

        # invalid message type
        invalid_request = IOTMessage()
        invalid_request.set_message_type("InvalidType")
        invalid_request.set_source(REMOTE_MODULE)
        invalid_request.set_operation(ADD_NODE)
        invalid_request.set_data(
            {
                "id": "ilm_001_12345",
                "state": "on",
            }
        )
        print(">>> invalid message type")
        print(invalid_request)
        print(invalid_request.validate_message_fields())
        print("-------------------------------------")

        # invalid request operation
        invalid_request = IOTMessage()
        invalid_request.set_message_type(REQUEST)
        invalid_request.set_source(REMOTE_MODULE)
        invalid_request.set_operation("InvalidOperation")
        invalid_request.set_data(
            {
                "id": "ilm_001_12345",
                "state": "on",
            }
        )
        print(">>> invalid request operation")
        print(invalid_request)
        print(invalid_request.validate_message_fields())
        print("-------------------------------------")

        # invalid response operation
        invalid_request = IOTMessage()
        invalid_request.set_message_type(RESPONSE)
        invalid_request.set_source(REMOTE_MODULE)
        invalid_request.set_operation("InvalidOperation")
        invalid_request.set_data(
            {
                "reason": iot_error.SUCCESS.string,
            }
        )
        print(">>> invalid response operation")
        print(invalid_request)
        print(invalid_request.validate_message_fields())
        print("-------------------------------------")

        # missing ID
        invalid_request = IOTMessage()
        invalid_request.set_message_type(REQUEST)
        invalid_request.set_source(REMOTE_MODULE)
        invalid_request.set_operation(ADD_NODE)
        invalid_request.set_data(
            {
                "state": "on",
            }
        )
        print(">>> missing ID")
        print(invalid_request)
        print(invalid_request.validate_message_fields())
        print("-------------------------------------")

        # invalid request operation
        invalid_request = IOTMessage()
        invalid_request.set_message_type(REQUEST)
        invalid_request.set_operation(ADD_NODE)
        invalid_request.set_data(
            {
                "id": "ilm_001_12345",
                "state": "on",
            }
        )
        print(">>> missing source")
        print(invalid_request)
        print(invalid_request.validate_message_fields())
        print("-------------------------------------")

        # stringfy add_node request
        request = IOTMessage()
        request.set_message_type(REQUEST)
        request.set_source(REMOTE_MODULE)
        request.set_operation(ADD_NODE)
        request.set_data(
            {
                "id": "ilm_001_12345",
                "state": "on",
            }
        )
        print(">>> add node request stringfy test")
        print(request)
        print(request.validate_message_fields())
        print(request.stringfy())
        print("-------------------------------------")

        # atringfy removew_node request
        request = IOTMessage()
        request.set_message_type(REQUEST)
        request.set_source(REMOTE_MODULE)
        request.set_operation(REMOVE_NODE)
        request.set_data(
            {
                "id": "ilm_001_12345",
            }
        )
        print(">>> remove node request stringfy test")
        print(request)
        print(request.validate_message_fields())
        print(request.stringfy())
        print("-------------------------------------")

        # stringfy data update request
        request = IOTMessage()
        request.set_message_type(REQUEST)
        request.set_source(REMOTE_MODULE)
        request.set_operation(UPDATE_DATA)
        request.set_data(
            {
                "id": "ilm_001_12345",
                "state": "on",
            }
        )
        print(">>> update data request stringfy test")
        print(request)
        print(request.validate_message_fields())
        print(request.stringfy())
        print("-------------------------------------")

        # stringfy success response
        response = IOTMessage()
        response.set_message_type(RESPONSE)
        response.set_source(REMOTE_MODULE)
        response.set_operation(SUCCESS)
        response.set_data(
            {
                "reason": iot_error.SUCCESS.string
            }
        )
        print(">>> update data request stringfy test")
        print(response)
        print(response.validate_message_fields())
        print(response.stringfy())
        print("-------------------------------------")

    elif test_cases == 2:

        # validate request string
        message_string = "1102id=ilm_1_123"
        print("validate request string")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # validate response string
        message_string = "2101"
        print("validate response string")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # invalid message string (not response nor string)
        message_string = "3101"
        print("invalid message type string")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # invalid request string
        message_string = "1502id=ilm_1_123"
        print("invalid request string")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # invalid response string
        message_string = "2991"
        print("invalid response string")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # invalid request string (missing source)
        message_string = "150id=ilm_1_123"
        print("invalid request string (missing source)")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # invalid response string (missing source)
        message_string = "299"
        print("invalid response string (missing source)")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # invalid request (insufficient data)
        message_string = "1101id=ilm_123"
        print("invalid request string (insufficient data)")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

        # invalid request (no ID)
        message_string = "1301state=on&power=off"
        print("invalid request string (missing ID)")
        print(IOTMessage.validate_message_string(message_string))
        print(*IOTMessage.parse_message_string(message_string))
        print("-------------------------------------")

