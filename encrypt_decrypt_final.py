import sys
import random
import string
import numpy as np

#string of all printable characters
PRINTABLE_CHARS = string.printable
#base64 character table
base64_table = (string.ascii_uppercase+string.ascii_lowercase+string.digits+'+/')

#maximum allowed message length
MAX_MSG_LEN = 500
#the length of every ct
MAX_CT_LEN = 2 * (MAX_MSG_LEN + 12) + 12

#debug variables to test various components
DEBUG_VIG = 0
DEBUG_RANDOM_KEY = 0
DEBUG_INSERT_RAND_LETTERS = 0
DEBUG_TEST_LETTER = 0
DEBUG_MAP_MSG = 0
TEST_VIG = 1

#generates a key
def gen_key():
    key = np.random.randint(0, high = (2**64) - 1, dtype='uint64')
    key = key.item()
    return key


#base64 encoder
def encode_64(v):
    bit_string = format(v, '064b')
    chunks_6bit = [bit_string[bits:bits+6] for bits in range(0,len(bit_string),6)]
    padding_amount = ( 6 - len(chunks_6bit[len(chunks_6bit)-1]) )
    chunks_6bit[len(chunks_6bit)-1] += padding_amount * '0'
    encoded = ''.join([base64_table[int(bits,2)] for bits in chunks_6bit])
    encoded += int(padding_amount/2) * '='
    return encoded

#base64 decoder
def decode_64(m):
    l = list(m)
    l = [format(base64_table.find(x), '06b') for x in l]
    l.pop()
    str_bin = ''.join(l)
    str_bin = str_bin[:len(str_bin) - 2]
    decoded = int(str_bin, 2)
    return decoded

#pads the ciphertext with random characters
def pad_ct(ct):
    
    s = ct
    while len(s) < MAX_CT_LEN - 12:
        s += random.choice(string.printable)
    return s

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

#xors the key with the message vector to get the seed for the PRNG
def key_xor(k, v):
    z = k ^ v
    return get_key(MAX_MSG_LEN, z)

#gets the message length from the encrypted text
def get_mlen(ct):
    
    m_len_str = ct[MAX_CT_LEN - 12: MAX_CT_LEN]
    
    return decode_64(m_len_str)

#generate a random key
#n - the length of the key you want to generate
def get_rand_key(n):

    k = ''

    for __ in range(0, n):
        k += random.choice(string.printable)
    return k

#seeds the random number generator and generates the key used to encrypt the message
def get_key(n, s):

    random.seed(s)
    key_num_list = []

    for __ in range(0, n + 1):
        i = random.randint(0, 99)
        key_num_list.append(i)
    
    return map_num_to_str(key_num_list)

#generates a random message of length n
def gen_rand_msg(n):
    m = ''
    for __ in range(n):
        m += random.choice(string.printable)
    return m


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


#vigenere encryption algorithm
#m - the message you want to encrypt
#k - a list of keys you want to use to encrypt m, the algo will select 1 at random
#insert_chars - whether or not you want to insert random letters every other character
def encrypt(m, k, insert_chars):

    v = np.random.randint(0, high = (2**64) - 1, dtype='uint64')
    v = v.item()
    key = key_xor(k, v)

    c_list = []             #empty list for cipher values
    k_idx = 0               #index of the key letter in PRINTABLE_CHARS
    new_c_val = 0           #index of the new encrypted character
    k_len = len(key)        #numbers of keys in the key list
    ct = ''                 #empty output string
    m_len = len(m)          #len of msg to send

    

    #map the key and msg to their indexes for encryption
    m_list = map_str_to_num(m)
    k_list = map_str_to_num(key)

    for x in m_list:
        new_c_val = (x + k_list[k_idx]) % len(PRINTABLE_CHARS)      #calculate new ciphertext value
        c_list.append(new_c_val)
        k_idx = (k_idx + 1) % k_len         #update location in key, us mod so if msg longer than key we loop back                   

    #map value list back to string
    ct = map_num_to_str(c_list)

    vector_encoded = encode_64(v)           #encode the vector we used to seed PNRG in base 64
    ct += vector_encoded

    if insert_chars:
        ct = insert_rand_chars(ct)                              #make every other character a random letter

    ct = pad_ct(ct)                         #pad ct with random characters

    m_len_encoded = encode_64(m_len)        #encode msg length in base 64
    ct += m_len_encoded

    return ct

#vigenere decryption algorithm
#inputs are the same as for encryption
def decrypt(m, k, insert_chars):

    ct = m

    m_len = get_mlen(ct)               #get the msg length

    ct_len = 2 * (m_len + 12) + 1      #get length of ct without padding or msg len

    ct = ct[0 : ct_len]                #chop off padding and msg len

    if insert_chars:
        ct = strip_rand_chars(ct)      #remove every other character as we know they are garbage

    v = decode_64(ct[m_len : len(ct)])      #decode the vector 

    ct = ct[0 : m_len]                      #chop off the vector

    key = key_xor(k, v)                     #get the original key by v xor key

    msg_list = []           
    k_idx = 0               
    new_c_val = 0           
    k_len = len(key)
    msg = ''

    m_list = map_str_to_num(ct)
    k_list = map_str_to_num(key)
    
    for x in m_list:

        new_c_val = ((x - k_list[k_idx]) + len(PRINTABLE_CHARS)) % len(PRINTABLE_CHARS)
        msg_list.append(new_c_val)

        k_idx = (k_idx + 1) % k_len

    msg = map_num_to_str(msg_list)

    return msg

def main():

    #this will test the encryption / decryption 
    if DEBUG_VIG == 1:
        key = np.random.randint(0, high = (2**64) - 1, dtype='uint64')
        key = key.item()

        m = gen_rand_msg(1)
        ct = encrypt(m, key, True)
        pt = decrypt(ct, key, True)

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

    if TEST_VIG:
        
        
        total_succeses = 0
        total_errors = 0

        for i in range(500):

            errors = 0
            succeses = 0

            for __ in range(1000):
                m = gen_rand_msg(i)
                key = gen_key()
                ct = encrypt(m, key, True)
                pt = decrypt(ct, key, True)
                if m == pt:
                    succeses += 1
                else:
                    errors += 1

            if succeses == 1000:
                total_succeses += 1
            else:
                total_errors += 1

            print(f"Done with messages of length: {i}")
            print(f'| Successes: {total_succeses} | Errors: {total_errors} |')

        


    print("Done!")


if __name__ == "__main__":
    main()
