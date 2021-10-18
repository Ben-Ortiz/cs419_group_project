import sys

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEY = 'LUCKY'


#vigenere encryption algorithm 
def encrypt(m):
    
    ct = ''                 #empty string to store ciphertext
    k_idx = 0               #index of the key letter in LETTERS
    c_idx = 0               #index of the character to encrypt in LETTERS
    k_loc = 0               #where in the key we currently are
    new_c_val = 0           #index of the new encrypted character
    k_len = len(KEY)        #length of the key

    for c in m:

        if c.upper() in LETTERS:                            #ignore non-letter characters

            c_idx = LETTERS.find(c.upper())                 #get the index of the letter to encrypt
            k_idx = LETTERS.find(KEY[k_loc].upper())        #get the index of the key letter
            new_c_val = (c_idx + k_idx) % 26                #add the two indexes and take mod 26 to get new index

            if c.isupper():
                ct += LETTERS[new_c_val].upper()
            else:
                ct += LETTERS[new_c_val].lower()


            k_loc = (k_loc + 1) % k_len                     #update key location, note if (k_loc + 1) == k_len then k_loc will be 0

        else:
            ct += c

    return ct

#vigenere decryption algorithm
#everything here is the same as encryption except we subtract the indexes, add 26, and take mod 26 to decrypt
def decrypt(m):
    
    pt = ''
    k_idx = 0
    c_idx = 0
    k_loc = 0
    new_c_val = 0
    k_len = len(KEY)

    for c in m:
        if c.upper() in LETTERS:

            c_idx = LETTERS.find(c.upper())
            k_idx = LETTERS.find(KEY[k_loc].upper())
            new_c_val = ((c_idx - k_idx) + 26) % 26         #this is only difference from encrypt algo

            if c.isupper():
                pt += LETTERS[new_c_val].upper()
            else:
                pt += LETTERS[new_c_val].lower()


            k_loc = (k_loc + 1) % k_len

        else:
            pt += c

    return pt


def main():

    m = 'hello, my name is.'
    ct = encrypt(m)
    pt = decrypt(ct)

    print(f'| Message: {m} |\n| Ciphertext: {ct} |\n| Plaintext: {pt} |\n')


if __name__ == "__main__":
    main()
