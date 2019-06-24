#!/usr/bin/env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


class Module(object):

    def __init__(self, **kwargs):

        self._name = kwargs.get("name", None)

        assert isinstance(self._name, str) and len(self._name) >= 9 and self._name.count('_') == 2

        module_name = self._name.split("_")

        self._type = module_name[0]
        self._version = module_name[1].zfill(3)
        self._id = module_name[2]

        del module_name

    def get_module_name(self):
        return self._name

    def set_module_type(self, module_type):
        if module_type is not None:
            self._type = module_type

    def get_module_type(self):
        return self._type

    def set_module_id(self, module_id):
        if module_id is not None:
            self._id = module_id

    def get_module_id(self):
        return self._id

    def set_module_version(self, version):
        if version is not None:
            self._version = version

    def get_module_version(self):
        return self._version

    def __str__(self):
        return "Module type: {}, version: {}, id: {}".format(self._type, self._version, self._id)


if __name__ == '__main__':

    tm = Module(
        name="ilm_01_12345"
    )

    print(tm)
    print(tm.get_module_name())

    print("type: {}\nversion: {}\nid: {}\n".format(tm.get_module_type(), tm.get_module_version(), tm.get_module_id()))

