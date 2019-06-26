#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import json
import iot_error
import time
from datetime import date


def update(args):
    """
    Update access module data and  html files
    :param args: (dict) module data as keyword, value pairs
    :return: (iot_error) module data update error code
    """

    # status
    status = iot_error.FAILED

    # check update action
    update_action = args.get("action")

    # get module data file
    module_data_file = args.get("module_data_file")

    # get module data
    with open(module_data_file, "r") as fh:
        module_data = json.loads(fh.read().strip())

    # get user name
    user_name = args.get("name").capitalize()

    # check for add action
    if update_action == "add":

        # add user name
        if user_name not in module_data["users"]:

            # add user name
            module_data["users"].append(user_name)
            module_data["users"].sort()

            status = iot_error.SUCCESS

        # if name already exists
        else:
            status = iot_error.FAILED

    # check for remove action
    elif update_action == "remove":

        # remove user name
        if user_name in module_data["users"]:

            # remove user name
            module_data["users"].remove(user_name)
            status = iot_error.SUCCESS

        # if name is not found
        else:
            status = iot_error.FAILED

    # check for login action
    elif update_action == "login":

        # check username is registered before
        if user_name in module_data["users"]:

            access = "success"
            status = iot_error.SUCCESS

        # if username is not registered
        else:
            access = "failed"
            status = iot_error.FAILED

        # get current time
        current_time = time.strftime("%H:%M:%S")

        # get current date
        current_date = date.today().strftime("%d/%m/%Y")

        # set login date and time
        log = "{} {}, name: {}, access: {}".format(
            current_date,
            current_time,
            user_name.capitalize(),
            access
        )

        # add access to to module data
        module_data["access_log"].append(log)

        module_data["access_log"].sort(reverse=True)

        # limit access log to 100 entries
        module_data["access_log"] = module_data["access_log"][:100]

    print("Updated Module data:", module_data)

    # update module data file
    with open(module_data_file, 'w') as fh:
        fh.write(json.dumps(module_data).strip())

    return status


if __name__ == '__main__':
    pass

