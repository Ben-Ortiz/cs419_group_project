import sys
import random
import string

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#A-0, B-1, C-2, D-3, E-4, F-5, G-6, H-7, I-8, J-9, K-10, L-11, M-12, 
#N-13, O-14, P-15, Q-16, R-17, S-18, T-19, U-20, V-21, W-22, X-23, Y-24, Z-25

#debug variables to test various components
DEBUG_VIG = 1
DEBUG_RANDOM_KEY = 0
DEBUG_INSERT_RAND_LETTERS = 0
DEBUG_TEST_LETTER = 0

#takes 2 letters and returns what lette they encrypt into
def test_letter(a, b):

    if a.upper() in LETTERS and b.upper() in LETTERS:

        a_idx = LETTERS.find(a.upper())
        b_idx = LETTERS.find(b.upper())

        new_c_val = (a_idx + b_idx) % 26

        return LETTERS[new_c_val].upper()


    else:
        print("Invalid values passed to test_letter!\n")
        exit


#vigenere encryption algorithm
#m - the message you want to encrypt
#k - the key you want to use to encrypt m
#key_type - the type of key you;re using: 1 for letters, 2 for numbers
#insert_chars - whether or not you want to insert random letters every other character
def encrypt(m, k, key_type, insert_chars):
    
    ct = ''                 #empty string to store ciphertext
    k_idx = 0               #index of the key letter in LETTERS
    c_idx = 0               #index of the character to encrypt in LETTERS
    k_loc = 0               #where in the key we currently are
    new_c_val = 0           #index of the new encrypted character
    k_len = len(k)          #length of the key

    for c in m:

        if c.upper() in LETTERS:                            #ignore non-letter characters

            c_idx = LETTERS.find(c.upper())                

            if key_type == 1:            
                k_idx = LETTERS.find(k[k_loc].upper())                                 
            elif key_type == 2:
                k_idx = int(k[k_loc])
            else:
                print("Invalid key type passed to encrypt!\n")
                exit                                        

            new_c_val = (c_idx + k_idx) % 26                

            if c.isupper():
                ct += LETTERS[new_c_val].upper()
            else:
                ct += LETTERS[new_c_val].lower()


            k_loc = (k_loc + 1) % k_len                     #update key location, note if (k_loc + 1) == k_len then k_loc will be 0

        else:
            ct += c

    if insert_chars:
        ct = insert_rand_chars(ct)                              #make every other character a random letter

    return ct

#vigenere decryption algorithm
#everything here is the same as encryption except we subtract the indexes, add 26, and take mod 26 to decrypt
def decrypt(m, k, key_type, insert_chars):
    
    pt = ''
    k_idx = 0
    c_idx = 0
    k_loc = 0
    new_c_val = 0
    k_len = len(k)
    msg = m

    if insert_chars:
        msg = strip_rand_chars(m)      #remove every other character as we know they are garbage


    for c in msg:
        if c.upper() in LETTERS:

            c_idx = LETTERS.find(c.upper())

            if key_type == 1:            
                k_idx = LETTERS.find(k[k_loc].upper())                                 
            elif key_type == 2:
                k_idx = int(k[k_loc])
            else:
                print("Invalid key type passed to encrypt!\n")
                exit

            new_c_val = ((c_idx - k_idx) + 26) % 26         #do the opposite of the encryption algo

            if c.isupper():
                pt += LETTERS[new_c_val].upper()
            else:
                pt += LETTERS[new_c_val].lower()


            k_loc = (k_loc + 1) % k_len

        else:
            pt += c

    return pt

#generate a random key
#pass 1 to get a key of letters, pass 2 to get a key of numbers
#n - the length of the key you want to generate
def get_rand_key(n, type):

    k = ''

    if type == 1:

        for __ in range(0, n):
            k += random.choice(string.ascii_uppercase)
        
        return k
    
    elif type == 2:

        for __ in range(0, n):
            k += str(random.randint(1, 9))

        return k

    else:
        
        print("Invalid key type passed to get_rand_key!\n")
        exit
        

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
        key = get_rand_key(n, 1)

        m = 'hello my name is josh'
        ct = encrypt(m, key, 1, True)
        pt = decrypt(ct, key, 1, True)

        print(f'| Message: {m} |\n| Ciphertext: {ct} |\n| Plaintext: {pt} |')

        print(f'| Key: {key} |')

    #this will test random key generator
    if DEBUG_RANDOM_KEY == 1:
        n = 120
        key = get_rand_key(n, 1)
        print(key)

    #this will test the random letter inserter
    if DEBUG_INSERT_RAND_LETTERS == 1:
        m = "suck it"
        s = insert_rand_chars(m, 1)
        print(s)
        print(strip_rand_chars(s))

    #this will test the test_letter function
    if DEBUG_TEST_LETTER:
        print(test_letter('s', 'u'))
        print(test_letter('u', 's'))


if __name__ == "__main__":
    main()
