#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


import os


def main():

    # get parent dir
    pwd = os.getcwd()

    # string to save modules html
    loaded_mods_html = dict()

    # go to modules folder
    os.chdir("modules")

    # loop over modules dirs
    for module_folder in os.listdir("."):

        # change to module dir
        if os.path.isdir(module_folder):

            os.chdir(module_folder)

            # load module html file
            mod_html_file = module_folder[:3].lower()+".html"

            # load module html file
            with open(mod_html_file, "r") as fh:
                mod_html = fh.read().strip()

            # save module html file
            loaded_mods_html[module_folder] = mod_html

            os.chdir("..")

        # not a directory (a file, like info file)
        else:
            pass

    # return to pwd
    os.chdir(pwd)

    # concatenate modules html into a single string
    modules_html_str = ""

    # append modules html into div_mods_tag
    for module_folder in loaded_mods_html.keys():
        modules_html_str += loaded_mods_html[module_folder]

    # send resulting html
    print(modules_html_str)


print("Content-Type : text/html")
print('<meta charset="UTF-8">')
print()
main()
