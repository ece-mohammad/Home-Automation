#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import re
import json
import iot_error
from module import Module


def update(args):
    """
    Update rfa module data and  html files
    :param args: (dict) module data as keyword, value pairs
    :return: (iot_error) module data update error code
    """

    status = iot_error.FAILED

    if args:

        # get module name
        module_name = args.get("id")

        # module instance
        module = Module(name=module_name)

        # load module data
        with open(mod_data_file, 'r') as fh:
            mod_data = json.loads(fh.read().strip())

        # check if state has changed
        if args.get("state", None):

            # check state value
            if args["state"] in ("on", "off"):

                # if value changed
                if args["state"] != mod_data["state"]:
                    mod_data["state"] = args["state"]

                    # write data to json file
                    with open(mod_data_file, 'w') as df:
                        df.write(json.dumps(mod_data).strip())

                    # update module html file
                    with open(mod_html_file, 'r') as hf:
                        mod_html = hf.read().strip()

                    # check_pattern
                    on_button = re.compile('(<input id="on_button".+?)(checked|unchecked)>')
                    off_button = re.compile('(<input id="off_button".+?)(checked|unchecked)>')

                    # modify button tags
                    if args["state"] == "on":
                        mod_html = re.sub(on_button, "\\1checked>", mod_html)
                        mod_html = re.sub(off_button, "\\1unchecked>", mod_html)

                    elif args["state"] == "off":
                        mod_html = re.sub(on_button, "\\1unchecked>", mod_html)
                        mod_html = re.sub(off_button, "\\1checked>", mod_html)

                    # invalid data field value
                    else:
                        status = iot_error.INVALID_DATA_FILED_VALUE

                    # write new html to mod_html file
                    with open(mod_html_file, 'w') as mh:
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

    # if data is None
    else:
        status = iot_error.MISSING_MODULE_ARGS

    return status


if __name__ == '__main__':
    pass

