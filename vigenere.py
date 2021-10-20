import sys
import random

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#debug variables to test various components
DEBUG_VIG = 1
DEBUG_RANDOM_KEY = 0


#vigenere encryption algorithm with a non-random key
def encrypt(m, k, is_rand_key):
    
    ct = ''                 #empty string to store ciphertext
    k_idx = 0               #index of the key letter in LETTERS
    c_idx = 0               #index of the character to encrypt in LETTERS
    k_loc = 0               #where in the key we currently are
    new_c_val = 0           #index of the new encrypted character
    k_len = len(k)          #length of the key

    for c in m:

        if c.upper() in LETTERS:                            #ignore non-letter characters

            c_idx = LETTERS.find(c.upper())                 #get the index of the letter to encrypt

            if is_rand_key:                                 #check what type of key is being used
                k_idx = int(k[k_loc])                       #key is random sequence of numbers
            else:
                k_idx = LETTERS.find(k[k_loc].upper())      #key is letters

            new_c_val = (c_idx + k_idx) % 26                

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
def decrypt(m, k, is_rand_key):
    
    pt = ''
    k_idx = 0
    c_idx = 0
    k_loc = 0
    new_c_val = 0
    k_len = len(k)

    for c in m:
        if c.upper() in LETTERS:

            c_idx = LETTERS.find(c.upper())
            if is_rand_key:                                 
                k_idx = int(k[k_loc])                       
            else:
                k_idx = LETTERS.find(k[k_loc].upper())
            new_c_val = ((c_idx - k_idx) + 26) % 26         #this is only difference from encrypt algo

            if c.isupper():
                pt += LETTERS[new_c_val].upper()
            else:
                pt += LETTERS[new_c_val].lower()


            k_loc = (k_loc + 1) % k_len

        else:
            pt += c

    return pt

#generate a random sequence of n numbers
def get_rand_key(n):

    k = ''

    for __ in range(0, n):
        k += str(random.randint(1, 9))

    return k


def main():

    #this will test the encryption / decryption 
    if DEBUG_VIG == 1:
        n = 120
        k_letters = 'LUCKY'
        k_rand = get_rand_key(n)

        m = 'hello, my name is.'
        ct = encrypt(m, k_rand, True)
        pt = decrypt(ct, k_rand, True)

        print(f'| Message: {m} |\n| Ciphertext: {ct} |\n| Plaintext: {pt} |\n')

        print(k_rand)

    #this will test random key generator
    if DEBUG_RANDOM_KEY == 1:
        n = 120
        key = get_rand_key(n)
        print(key)
        


if __name__ == "__main__":
    main()
