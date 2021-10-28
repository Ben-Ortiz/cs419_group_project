import sys
import random
import string

#string of all printable characters
PRINTABLE_CHARS = string.printable

#debug variables to test various components
DEBUG_VIG = 1
DEBUG_RANDOM_KEY = 0
DEBUG_INSERT_RAND_LETTERS = 0
DEBUG_TEST_LETTER = 0
DEBUG_MAP_MSG = 0

#map string to values
def map_str_to_num(s):

    s_list = []
    s_idx = 0

    for x in s:
        if x in PRINTABLE_CHARS:
            s_idx = PRINTABLE_CHARS.find(x)
            s_list.append(s_idx) 
    return s_list

#sum elements of list and return mod 100
def compute_check_sum(m_list):
    c_sum = sum(m_list) % 100
    return c_sum

#grab last letter of msg and return value
def get_check_sum(m_list):
    c = m_list[-1:]
    return PRINTABLE_CHARS.find(c)

#map values to characters
def map_num_to_str(num_list):   
    s = ''
    for x in num_list:
        s += PRINTABLE_CHARS[x]     
    return s

#vigenere encryption algorithm
#m - the message you want to encrypt
#k - a list of keys you want to use to encrypt m, the algo will select 1 at random
#insert_chars - whether or not you want to insert random letters every other character
def encrypt(m, k, insert_chars):

    c_list = []             #empty list for cipher values
    k_idx = 0               #index of the key letter in PRINTABLE_CHARS
    new_c_val = 0           #index of the new encrypted character
    k_list_len = len(k)     #numbers of keys in the key list
    ct = ''                 #empty output string

    #randomely choose a key from a list of keys passed in to encrypt with
    key_select = random.randint(0, k_list_len - 1)
    key = k[key_select]
    k_len = len(key)

    #map the key and msg to their indexes for encryption
    m_list = map_str_to_num(m)
    k_list = map_str_to_num(key)

    for x in m_list:
        new_c_val = (x + k_list[k_idx]) % len(PRINTABLE_CHARS)      #calculate new ciphertext value
        c_list.append(new_c_val)
        k_idx = (k_idx + 1) % k_len         #update location in key, us mod so if msg longer than key we loop back                   

    #map value list back to string
    ct = map_num_to_str(c_list)

    if insert_chars:
        ct = insert_rand_chars(ct)                              #make every other character a random letter

    #compute and insert check sum
    c_sum = compute_check_sum(m_list)
    ct += PRINTABLE_CHARS[c_sum]

    return ct

#vigenere decryption algorithm
#inputs are the same as for encryption
def decrypt(m, keys, insert_chars):

    #get the checksum and remove checksome from ciphertext
    c_sum = get_check_sum(m)
    ct = m[:len(m) - 1]
    if insert_chars:
        ct = strip_rand_chars(m)      #remove every other character as we know they are garbage

    #need to decrypt for each key in list till the checksums match
    for k in keys:

        msg_list = []           
        k_idx = 0               
        new_c_val = 0           
        k_len = len(k)
        msg = ''

        m_list = map_str_to_num(ct)
        k_list = map_str_to_num(k)
        
        for x in m_list:

            new_c_val = ((x - k_list[k_idx]) + len(PRINTABLE_CHARS)) % len(PRINTABLE_CHARS)
            msg_list.append(new_c_val)

            k_idx = (k_idx + 1) % k_len     #do the opposite of encryption

        msg = map_num_to_str(msg_list)

        msg_c_sum = compute_check_sum(msg_list)     #get the checksum of the message we decrypted

        if msg_c_sum == c_sum:              
            return msg              #we found the right key

    return -1

#generate a random key
#n - the length of the key you want to generate
def get_rand_key(n):

    k = ''

    for __ in range(0, n):
        k += random.choice(string.printable)
    return k
    

#make every other character in a string a random character
def insert_rand_chars(m):

    new_list = []
    new_m = ""

    for c in m:
        new_char = random.choice(string.printable)
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
        n = 10
        key_list = [get_rand_key(n), get_rand_key(n)]

        m = 'hello my name is josh'
        ct = encrypt(m, key_list, True)
        pt = decrypt(ct, key_list, True)

        print(f'| Message: {m} |\n| Ciphertext: {ct} |\n| Plaintext: {pt} |')

        print(f'| Key: {key_list} |')

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

    if DEBUG_MAP_MSG:

        m = "h"
        m_list = map_str_to_num(m)
        k = get_rand_key(10)
        k_list = map_str_to_num(k)
        
        print(m_list)
        print(k_list)

        print(map_num_to_str(m_list))

        c = encrypt(m, k, False)
        msg = decrypt(c, k, False)

        print(c)
        print(msg)

    print("Done!")


if __name__ == "__main__":
    main()
