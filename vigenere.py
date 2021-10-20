import sys
import random
import string

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#debug variables to test various components
DEBUG_VIG = 1
DEBUG_RANDOM_KEY = 0
DEBUG_INSERT_RAND_LETTERS = 0


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

    ct = insert_rand_chars(ct)                              #make every other character a random letter

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

    stripped_msg = strip_rand_chars(m)      #remove every other character as we know they are garbage


    for c in stripped_msg:
        if c.upper() in LETTERS:

            c_idx = LETTERS.find(c.upper())
            if is_rand_key:                                 
                k_idx = int(k[k_loc])                       
            else:
                k_idx = LETTERS.find(k[k_loc].upper())
            new_c_val = ((c_idx - k_idx) + 26) % 26         #do the opposite of the encryption algo

            if c.isupper():
                pt += LETTERS[new_c_val].upper()
            else:
                pt += LETTERS[new_c_val].lower()


            k_loc = (k_loc + 1) % k_len

        else:
            pt += c

    return pt

#generate a random sequence of n numbers for use as a key
def get_rand_key(n):

    k = ''

    for __ in range(0, n):
        k += str(random.randint(1, 9))

    return k

#make every other character in a string a random character
def insert_rand_chars(m):

    m_list = list(m)
    new_list = []
    new_m = ""

    for c in m:
        new_char = random.choice(string.ascii_lowercase)
        new_list.append(c + new_char)

    new_m = ''.join(new_list)

    return new_m

#remove every other character from a string
def strip_rand_chars(m):

    split_string = [m[i:i+2] for i in range(0, len(m), 2)]
    for i in range(0, len(split_string)):
        split_string[i] = split_string[i][:-1]

    return ''.join(split_string)


def main():

    #this will test the encryption / decryption 
    if DEBUG_VIG == 1:
        n = 120
        k_letters = 'LUCKY'
        k_rand = get_rand_key(n)

        m = 'hello, my name is.'
        ct = encrypt(m, k_rand, True)
        pt = decrypt(ct, k_rand, True)

        print(f'| Message: {m} |\n| Ciphertext: {ct} |\n| Plaintext: {pt} |')

        print(f'| Key: {k_rand} |')

    #this will test random key generator
    if DEBUG_RANDOM_KEY == 1:
        n = 120
        key = get_rand_key(n)
        print(key)

    #this will test the random letter inserter
    if DEBUG_INSERT_RAND_LETTERS == 1:
        m = "hello my name is"
        s = insert_rand_chars(m, 1)
        print(s)
        print(strip_rand_chars(s))


if __name__ == "__main__":
    main()
