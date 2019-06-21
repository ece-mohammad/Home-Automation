#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


from collections import namedtuple


"""     Simple class for IOT Error codes        """
_ERROR_CODES = namedtuple("ErrorCode", "string code")

"""     general error codes     """
SUCCESS = _ERROR_CODES("Success", 10)
FAILED = _ERROR_CODES("Failed", 20)
INVALID_MESSAGE_FORMAT = _ERROR_CODES("InvalidMessageFormat", 30)

"""      message specific error codes       """
INVALID_MESSAGE_OBJECT = _ERROR_CODES("InvalidMessageObject", 40)
UNKNOWN_MESSAGE_TYPE = _ERROR_CODES("UnknownMessageType", 41)
UNKNOWN_REQUEST = _ERROR_CODES("UnknownRequest", 42)
UNKNOWN_RESPONSE = _ERROR_CODES("UnknownResponse", 43)

"""     module specific error codes     """
UNSUPPORTED_MODULE = _ERROR_CODES("UnsupportedModule", 44)
UNSUPPORTED_MODULE_VERSION = _ERROR_CODES("UnsupportedModuleVersion", 45)
UNREGISTERED_MODULE = _ERROR_CODES("UnregisteredModule", 46)
MISSING_MODULE_ID = _ERROR_CODES("MissingModuleID", 47)
MISSING_MESSAGE_SOURCE = _ERROR_CODES("MissingSource", 48)
UNKNOWN_SOURCE = _ERROR_CODES("UnknownSource", 49)
MISSING_MODULE_ARGS = _ERROR_CODES("MissingModuleArgs", 50)
INVALID_DATA_FILED_VALUE = _ERROR_CODES("InvalidDataFieldValue", 51)

"""     Internal Errors     """
MISSING_MODULE_HTML_TEMPLATE = _ERROR_CODES("MissingModuleHTMLTemplate", 70)
MISSING_MODULE_DATA_TEMPLATE = _ERROR_CODES("MissingModuleDataTemplate", 71)
MISSING_MODULE_HTML_FILE = _ERROR_CODES("MissingModuleHTMLFile", 72)
MISSING_MODULE_DATA_FILE = _ERROR_CODES("MissingModuleDataFile", 73)
MISSING_MODULE_IP = _ERROR_CODES("MissingModuleIP", 74)
MISSING_MODULE_INFO_FILE = _ERROR_CODES("MissingModuleInfoFile", 75)


if __name__ == '__main__':

    err = SUCCESS
    print(err.string)
    print(err.code)

