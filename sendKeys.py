import numpy as np

"""
Diffie-Hellman Key Exchange from wikipedia inspired key exchange from client to server  

public number is randomly generated

keyClient(Alice) randomly generates a number
keyServer(Bob) randomly generates a number


Alice mods their randomly generated number to the public number
A = keyClient % publicNumber

Bob mods their randomly generated number to the public number
B = keyServer % publicNumber

Alice sends their number to Bob
Bob sends their number to Alice

Alice has Bobs number (B) and adds it with their key(keyClient) 
sharedA = B + keyClient

Bob has Alices number (A) and adds it with their key(keyServer)
sharedB = A + keyServer

A loop runs until sharedA == sharedB
if they are equal the client is able to connect with the server
"""

def keyExchange():
    while(1):

        publicNumber = np.random.randint(0, high = (2**64) - 1, dtype='uint64')

        keyClient = np.random.randint(0, high = (2**64) - 1, dtype='uint64') # sent to server
        keyServer = np.random.randint(0, high = (2**64) - 1, dtype='uint64') # sent to client

        A = keyClient % publicNumber # sent to server
        B = keyServer % publicNumber # sent to client

        sharedA = B + keyClient
        sharedB = A + keyServer
        if sharedA == sharedB:
            return True

def main():
    #TODO ask messenger team about how I would send keys from client to server if I have one implemented

    if(keyExchange):
        print("keys are equal from client and server, connection may begin")


if __name__ == "__main__":
    main()