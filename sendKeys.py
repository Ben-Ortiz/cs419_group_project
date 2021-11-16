import numpy as np

"""
Diffie-Hellman Key Exchange inspired key exchange from client to server

given p and g (known to outsiders)
where p and g are prime numbers
and g is a primtive root modulo number of p
example:
p = 29
g = {2,3,8,10,11,14,15,18,19,21,26,27}

p = 29
g = 3

client has a key a 
server has a key b

client uses g, a, and p to create A
A = (g**a) % p

server uses g, b, and p to create B
B = (g**b) % p

client shares A to server
server shares B to client

client takes B from server to create shared A
shared A = (B**a) % p
server takes A from client to create shared B
shared B = (A**b) % p

shared A should equal shared B
shared A == Shared B
which would mean they are now able to connect

"""

def main():
    #TODO ask messenger team about how I would send keys from client to server if I have one implemented
    # print("test")

    # key = np.random.randint(0, high = (2**64) - 1, dtype='uint64')
    # key = key.item()


    p = 23
    g = 19

    keyClient = np.random.randint(0, high = (2**64) - 1, dtype='uint64')
    keyServer = np.random.randint(0, high = (2**64) - 1, dtype='uint64')

    A = (g**keyClient) % p
    B = (g**keyServer) % p

    print(A)
    print(B)


if __name__ == "__main__":
    main()