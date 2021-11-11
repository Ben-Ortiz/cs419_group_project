from os import system, name
import json

"""
Function that clears the terminal of all text rendered
"""
def clear():
    if name == 'nt':
        system('cls') # Windows Command
    else:
        system('clear') # Linux/Mac OS Command


def package_message(lib, HEADER_SIZE):

    """
    Takes a python library and returns a json object
    """

    package = json.dumps(lib).encode("utf-8")
    header = f"{len(package):<{HEADER_SIZE}}".encode("utf-8")
    message = header + package

    return message


def unpackage_message(package):

    """
    Takes a json object and returns a python library
    """

    return json.loads(package.decode("utf-8"))