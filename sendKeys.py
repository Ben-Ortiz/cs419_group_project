#Diffie-Hellman Key Exchange inspired key exchange from client to server

def main():
    #TODO ask messenger team about how I would send keys from client to server if I have one implemented
    print("test")

    key = np.random.randint(0, high = (2**64) - 1, dtype='uint64')
    key = key.item()

    print(key)

if __name__ == "__main__":
    main()