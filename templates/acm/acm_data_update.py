#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import json
import iot_error
import iot_message


def update(args):
    """
    Update rfa module data and  html files
    :param args: (dict) module data as keyword, value pairs
    :return: (iot_error) module data update error code
    """

    status = iot_error.FAILED
    message = iot_message.IOTMessage()

    if args:

        # get module data
        mod_data_file = args["mod_data_file"]

        # load module data
        with open(mod_data_file, 'r') as fh:
            mod_data = json.loads(fh.read().strip())

        if not mod_data.get("db", None):
            mod_data["db"] = list()

        # validate ACTION and NAME data fields
        if args.get("action", None) and args.get("name", None):

            args["name"] = args["name"].lower()

            # if ACTION is add
            if args["action"] == "add" and args["name"] not in mod_data["db"]:
                mod_data["db"].append(args.get("name"))
                status = iot_error.SUCCESS

            # if ACTION is remove
            elif args["action"] == "remove" and args["name"] in mod_data["db"]:
                mod_data["db"].remove(args.get("name"))
                status = iot_error.SUCCESS

            # invalid ACTION value
            else:
                status = iot_error.INVALID_DATA_FILED_VALUE

            with open(mod_data_file, 'w') as fh:
                fh.write(json.dumps(mod_data))

            # check status code
            if status.code == iot_error.SUCCESS.code:

                message.set_message_type(iot_message.REQUEST)
                message.set_operation(iot_message.UPDATE_NODE_DATA)
                message.set_data(
                    {
                        "id": args["id"],
                        "name": ("+" if args["action"] == "add" else "-") + args["name"],
                    }
                )

            # status is not success
            else:
                pass

        # if missing ACTION parameter
        else:
            status = iot_error.MISSING_MODULE_ARGS

    # if data is None
    else:
        status = iot_error.MISSING_MODULE_ARGS

    return status, message


if __name__ == '__main__':
    pass

