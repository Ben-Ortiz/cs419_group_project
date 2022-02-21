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

                    accounts = pd.read_csv("data/accounts.csv")
                    key = accounts['key'].loc[(accounts['username'] == user)]

                    connections[client_socket] = user
                    active_clients[user] = client_socket

                    print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username {user}")
                    success = {"type":"account_creation", "src":"server", "dest":"user", "data":int(key.item()), "is_encrypted":False}
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

                # Store message in conversations.csv
                conversations = pd.read_csv("data/conversations.csv")
                new_msg = {'to' : dict['dest'], 'from' : dict['src'], 'message' : convo_msg}
                conversations = conversations.append(new_msg, ignore_index=True)
                conversations.to_csv("data/conversations.csv", index = False)

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

            if dict['type'] == 'get_convo':
                accounts = pd.read_csv("data/accounts.csv")
                src_key = accounts['key'].loc[(accounts['username'] == dict['src'])]
                dest_key = accounts['key'].loc[(accounts['username'] == dict['data'])]
                curr_user = dict['src']
                user2 = dict['data']
                conversations = pd.read_csv("data/conversations.csv")
                msgs = conversations.loc[ ( conversations['to'] == curr_user) & (conversations['from'] == user2 ) | (conversations['to'] == user2) & (conversations['from'] == curr_user)]

                msgs['decrypted_msg'] = msgs.apply(lambda x : ed.decrypt(x['message'], int(src_key.item()), True) if x['from'] == curr_user else ed.decrypt(x['message'], int(dest_key.item()), True), axis = 1)
                msgs['decrypted_msg'] = msgs.apply(lambda x : '<' + x['from'] + '>' + x['decrypted_msg'] if x['from'] == user2 else '<you>' + x['decrypted_msg'], axis = 1)

                m_list = list(msgs['decrypted_msg'])
                curr_out_string = ''
                prev_out_string = ''
                m_count = 0

                for m in m_list:
                    prev_out_string = curr_out_string
                    curr_out_string += m

                    if len(curr_out_string) > 1000:
                        curr_out_string = prev_out_string
                        break

                encrypted_out_string = ed.encrypt(curr_out_string, int(src_key.item()), True)

                print(f"Sending conversation between {dict['src']} and {dict['data']} to {dict['src']}")
                new_packet = {"type":"conversation_response", "src":"server", "dest": dict['src'], "data": encrypted_out_string, "is_encrypted":False}
                support.send_message(new_packet, active_clients[new_packet['dest']], HEADER_SIZE)

                

        for conn in err_sockets:
            del active_clients[connections[conn]]
            del connections[conn]