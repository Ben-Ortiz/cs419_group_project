import socket
import select
import csv
import sys
import pandas as pd
from messenger import support



IP = sys.argv[1]
PORT = int(sys.argv[2])
HEADER_SIZE = 10



if __name__ == "__main__":  

    # Server Initialization
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((IP, PORT))
    print("Server started")
    print("Waiting for client request..")
    server_socket.listen()

    connections = {server_socket: 'server'} # active connections
    active_clients = {} # active users


    while True:
        # select() returns three new lists, containing subsets of the contents of the lists passed in.
        # All of the sockets in the readable list have incoming data buffered and available to be read.
        # All of the sockets in the writable list have free space in their buffer and can be written to.
        # The sockets returned in exceptional have had an error (the actual definition of “exceptional condition” depends on the platform).

        # Get list of sockets which are ready to be read through select()
        read_sockets, write_sockets, err_sockets = select.select(connections, [], connections)

        for conn in read_sockets:

            # Handle New Connections to the Server
            if conn == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                client_socket, client_address = server_socket.accept()
                data = support.recieve_message(client_socket, HEADER_SIZE)
                header = support.unpackage_message(data['header'])
                lib = support.unpackage_message(data['data'])
                user = lib["src"]
                password = lib["data"]

                accounts = pd.read_csv("data/accounts.csv", index_col=0)
                user_check = user in accounts.index
                if not user_check:
                    print("Username not valid")
                    failure = {"type":"login_check", "src":"server", "dest":"user", "data":False, "is_encrypted":False}
                    packet = support.package_message(failure, HEADER_SIZE)
                    client_socket.send(packet)

                    continue

                valid = accounts.loc[user, "password"]

                if user is False or password != valid:
                    print("user validation failed")
                    failure = {"type":"login_check", "src":"server", "dest":"user", "data":False, "is_encrypted":False}
                    packet = support.package_message(failure, HEADER_SIZE)
                    client_socket.send(packet)

                    continue
                connections[client_socket] = user
                active_clients[user] = client_socket

                print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user}")
                success = {"type":"login_check", "src":"server", "dest":"user", "data":True, "is_encrypted":False}
                packet = support.package_message(success, HEADER_SIZE)
                client_socket.send(packet)

                continue

            # Handle Messages Sent to the Server
            data = support.recieve_message(conn, HEADER_SIZE)
            if not data:
                print("User disconnected")
                del active_clients[connections[conn]]
                del connections[conn]
                continue
            header = support.unpackage_message(data['header'])
            lib = support.unpackage_message(data['data'])
            recipient = lib["dest"]

            if lib["type"] == "message":
                # Store message in conversations.csv
                # Open conversations.csv in append mode
                with open('conversations.csv', mode='a') as conversations:
                    writer = csv.writer(conversations, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                    writer.writerow([lib['src'], lib['dest'], lib['data']])
                    conversations.close()

                # Search connections to see if recipient user is active
                if recipient in active_clients:
                    # Send message to user
                    print(f"Sending message from {lib['src']} to {recipient}")
                    support.send_message(lib, active_clients[recipient], HEADER_SIZE)

                # Otherwise store message in messages.csv
                else:
                    with open('messages.csv', mode='a') as messages:
                        writer = csv.writer(messages, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                        writer.writerow([lib['src'], lib['dest'], lib['data']])
                        messages.close()

                continue

        for conn in err_sockets:
            del active_clients[connections[conn]]
            del connections[conn]