#!/usr/bin.env python3


__version__ = 1.2
__author__ = "Mohammad Mohsen"


def validate_ip4(ip):
    """
    Validates a given IP
    :param ip:
    :return:  (boolean) True if the given IP is valid, otherwise False
    """
    ip = ip.strip().split(".")
    return all([(octet.isdigit() and "0" <= octet <= "255") for octet in ip]) and len(ip) == 4


def valid_query_data(query_string):
    """
    Validate a query string in the form key_1=value_1&key_2=value_2&...&key_n=value_n
    :param query_string: data string to validate, must have at least 1 key, value pair
    :return: (boolean) True if valid, False otherwise
    """
    # split query string around '&'
    query_string = query_string.strip().split("&")

    # validation result
    correct = False
    valid = False

    # check length
    if len(query_string) >= 1:

        # data length is sufficient
        valid = True

        # iterate over query_string split parts : (key_n=value_n)
        for pair in query_string:

            # split key_n=value_n around '=' and look for id key, if found, break the iteration
            # and set correct to True
            if pair.split("=")[0] == "id":

                correct = True
                break

    return valid, correct


if __name__ == '__main__':

    print(validate_ip4("192.168.137.1"))
    print(validate_ip4("255.255.255.255"))
    print(validate_ip4("0.0.0.0"))
    print(validate_ip4("192.168.1"))
    print(validate_ip4("192.168.137..1"))
    print(validate_ip4("192.168..1"))
    print(validate_ip4("192.168.1.256"))
    print(validate_ip4("192.168.1.-1"))
    print(validate_ip4("192.168.1.ff"))

