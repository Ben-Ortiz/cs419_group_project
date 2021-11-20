# Common/helper functions

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


def package_message(dict, HEADER_SIZE):

    """
    Takes a python dictionary containing message paramaters and returns a json object that can be sent across sockets
    """

    package = json.dumps(dict).encode("utf-8")
    header = f"{len(package):<{HEADER_SIZE}}".encode("utf-8")
    message = header + package

    return message


def unpackage_message(package):

    """
    Takes a json object and returns a python dictionary
    """

    return json.loads(package.decode("utf-8"))


def send_message(dict, sock, HEADER_SIZE):
		
    """
    Creates json object from dictionary, then sends json across the socket
    """

    sock.sendall(package_message(dict, HEADER_SIZE))


def recieve_message(sock, HEADER_SIZE):

    """
    Recieves a single message from a socket
    
    Returns the package header and the message dictionary as json objects
    """

    try:
        message_header = sock.recv(HEADER_SIZE)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())

        data = sock.recv(message_length)

        return {"header": message_header, "data": data}

    except:
        return False