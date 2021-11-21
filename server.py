import socket
import select
import sys
import pandas as pd
import support
import encrypt_decrypt_final as ed



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

    connections = {server_socket: 'server'} # active connections, key=socket, value=username
    active_clients = {} # active users, key=username, value=socket


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
                dict = support.unpackage_message(data['data'])
                user = dict["src"]
                password = dict["data"]
                accounts = pd.read_csv("data/accounts.csv")
                user_check = user in list(accounts['username'])

                # Handle new account creation
                if dict['type'] == "account_creation":
                    if user_check:
                        print("Username already taken")
                        failure = {"type":"account_creation", "src":"server", "dest":"user", "data":False, "is_encrypted":False}
                        packet = support.package_message(failure, HEADER_SIZE)
                        client_socket.send(packet)

                        continue

                    key = ed.gen_key()

                    new_acc = {'username' : user, 'password' : password, 'key' : key}
                    accounts = accounts.append(new_acc, ignore_index=True)
                    accounts.to_csv("data/accounts.csv", index = False)
                    #accounts.to_csv("data/accounts.csv", sep='\t', encoding='utf-8')

                    connections[client_socket] = user
                    active_clients[user] = client_socket

                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user}")
                    success = {"type":"account_creation", "src":"server", "dest":"user", "data":key, "is_encrypted":False}
                    packet = support.package_message(success, HEADER_SIZE)
                    client_socket.send(packet)

                    continue


                # Handle account login
                if dict['type'] == "login_check":
                    if not user_check:
                        print("Username not valid")
                        failure = {"type":"login_check", "src":"server", "dest":"user", "data":False, "is_encrypted":False}
                        packet = support.package_message(failure, HEADER_SIZE)
                        client_socket.send(packet)

                        continue

                    valid = accounts['password'].loc[(accounts['username'] == user)]

                    if user is False or password != valid.item():
                        print("user validation failed")
                        failure = {"type":"login_check", "src":"server", "dest":"user", "data":False, "is_encrypted":False}
                        packet = support.package_message(failure, HEADER_SIZE)
                        client_socket.send(packet)

                        continue

                    key = accounts['key'].loc[(accounts['username'] == user)] #placeholder value so the rest of the code works

                    connections[client_socket] = user
                    active_clients[user] = client_socket

                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user}")
                    success = {"type":"login_check", "src":"server", "dest":"user", "data":int(key.item()), "is_encrypted":False}
                    packet = support.package_message(success, HEADER_SIZE)
                    client_socket.send(packet)

                    continue

                else:
                    print("Some weird error happened.")
                    continue

            # Handle Messages Sent to the Server
            data = support.recieve_message(conn, HEADER_SIZE)
            if not data:
                print("User disconnected")
                del active_clients[connections[conn]]
                del connections[conn]
                continue
            header = support.unpackage_message(data['header'])
            dict = support.unpackage_message(data['data'])

            if dict['type'] == "message":
                accounts = pd.read_csv("data/accounts.csv")
                src_key = accounts['key'].loc[(accounts['username'] == dict['src'])]
                dest_key = accounts['key'].loc[(accounts['username'] == dict['dest'])]
                convo_msg = dict['data']

                decrypted_source = ed.decrypt(dict['data'], int(src_key.item()), True)
                encrypted_dest = ed.encrypt(decrypted_source, int(dest_key.item()), True)
                dict['data'] = encrypted_dest

                # Search connections to see if recipient user is active
                if dict["dest"] in active_clients:
                    # Send message to user
                    print(f"Sending message from {dict['src']} to {dict['dest']}")
                    support.send_message(dict, active_clients[dict['dest']], HEADER_SIZE)

                # Otherwise store message in messages.csv
                else:
                    messages = pd.read_csv("data/messages.csv", index_col=0)
                    messages.append([dict['dest'], dict['src'], dict['data']])

                continue

            if dict['type'] == "delete_user":
                #TODO Send package to user that will disconnect them


                # Remove user from active sockets
                if dict["data"] in active_clients:
                    print(f"Removing user {dict['src']}")
                    del connections[active_clients[dict["data"]]]
                    del active_clients[dict["data"]]

                # Remove user from accounts dataframe
                #TODO idk how to do this

            if dict['type'] == "reset":
                #TODO Send package to ever user that will disconnect them

                connections = {server_socket: 'server'}
                active_clients = {}

        for conn in err_sockets:
            del active_clients[connections[conn]]
            del connections[conn]