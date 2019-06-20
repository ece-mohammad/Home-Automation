#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import re
import json
import iot_error


def update(args):
    """
    Update ilm module data and  html files
    :param args: module data as keyword, value pairs
    :return: (iot_error) module data update error code
    """

    # update status
    status = iot_error.FAILED

    # get module html file
    module_html_file = args["module_html_file"]

    # get module data file
    module_data_file = args["module_data_file"]

    # load module data
    with open(module_data_file, 'r') as fh:
        local_module_data = json.loads(fh.read().strip())

    # check if state has changed
    if args.get("state", None):

        # check state value
        if args["state"] in ("on", "off"):

            # if value changed
            if args["state"] != local_module_data["state"]:
                local_module_data["state"] = args["state"]

                # write data to json file
                with open(module_data_file, 'w') as df:
                    df.write(json.dumps(local_module_data).strip())

                # update module html file
                with open(module_html_file, 'r') as hf:
                    mod_html = hf.read().strip()

                # check_pattern
                on_button = re.compile('(<input id="on_button".+?)(checked|unchecked)>')
                off_button = re.compile('(<input id="off_button".+?)(checked|unchecked)>')

                # modify on button tag
                if args["state"] == "on":
                    mod_html = re.sub(on_button, "\\1checked>", mod_html)
                    mod_html = re.sub(off_button, "\\1unchecked>", mod_html)

                # modify off button tag
                elif args["state"] == "off":
                    mod_html = re.sub(on_button, "\\1unchecked>", mod_html)
                    mod_html = re.sub(off_button, "\\1checked>", mod_html)

                # write new html to mod_html file
                with open(module_html_file, 'w') as mh:
                    mh.write(mod_html)

                status = iot_error.SUCCESS

            # if state didn't change
            else:
                status = iot_error.SUCCESS

        # invalid state value
        else:
            status = iot_error.INVALID_DATA_FILED_VALUE

    # if missing STATE parameter
    else:
        status = iot_error.MISSING_MODULE_ARGS

    return status


if __name__ == '__main__':
    pass

