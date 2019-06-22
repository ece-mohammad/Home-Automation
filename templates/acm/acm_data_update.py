#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import json
import iot_error
import iot_message
import time
import datetime


def update(args):
    """
    Update access module data and  html files
    :param args: (dict) module data as keyword, value pairs
    :return: (iot_error) module data update error code
    """

    status = iot_error.FAILED

    print(args)


if __name__ == '__main__':
    pass

