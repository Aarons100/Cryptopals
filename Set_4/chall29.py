from struct import pack, unpack
import binascii

def sha1(data):
    """ Returns the SHA1 sum as a 40-character hex string """
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    def rol(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    # After the data, append a '1' bit, then pad data to a multiple of 64 bytes
    # (512 bits).  The last 64 bits must contain the length of the original
    # string in bits, so leave room for that (adding a whole padding block if
    # necessary).

    #print "length of input to SHA1:", len(data)

    if(len(data) % 64 == 0):
        padded_data = data
    else: 
        padding = chr(128) + chr(0) * (55 - len(data) % 64)
        if len(data) % 64 > 55:
            padding += chr(0) * (64 + 55 - len(data) % 64)
        padding = padding + pack('>Q', 8 * len(data))
        padded_data = data + padding

        #print "hash padding: ", binascii.hexlify(padding), "len =", len(padding)

    thunks = [padded_data[i:i+64] for i in range(0, len(padded_data), 64)]
    for thunk in thunks:
        w = list(unpack('>16L', thunk)) + [0] * 64
        for i in range(16, 80):
            w[i] = rol((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        # Main loop
        for i in range(0, 80):
            if 0 <= i < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i < 60:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif 60 <= i < 80:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = rol(a, 5) + f + e + k + w[i] & 0xffffffff, \
                            a, rol(b, 30), c, d

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def sha1_custom_args(data, var1,var2,var3,var4,var5):
    """ Returns the SHA1 sum as a 40-character hex string """

    h0 = var1
    h1 = var2
    h2 = var3
    h3 = var4
    h4 = var5

    def rol(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xffffffff

    # After the data, append a '1' bit, then pad data to a multiple of 64 bytes
    # (512 bits).  The last 64 bits must contain the length of the original
    # string in bits, so leave room for that (adding a whole padding block if
    # necessary).

    #print "length of input to SHA1:", len(data)

    if(len(data) % 64 == 0):
        padded_data = data
    else: 
        padding = chr(128) + chr(0) * (55 - len(data) % 64)
        if len(data) % 64 > 55:
            padding += chr(0) * (64 + 55 - len(data) % 64)
        padding = padding + pack('>Q', 8 * len(data))
        padded_data = data + padding

        #print "hash padding: ", binascii.hexlify(padding), "len =", len(padding)

    thunks = [padded_data[i:i+64] for i in range(0, len(padded_data), 64)]
    for thunk in thunks:
        w = list(unpack('>16L', thunk)) + [0] * 64
        for i in range(16, 80):
            w[i] = rol((w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16]), 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        # Main loop
        for i in range(0, 80):
            if 0 <= i < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i < 60:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif 60 <= i < 80:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = rol(a, 5) + f + e + k + w[i] & 0xffffffff, \
                            a, rol(b, 30), c, d

        h0 = h0 + a & 0xffffffff
        h1 = h1 + b & 0xffffffff
        h2 = h2 + c & 0xffffffff
        h3 = h3 + d & 0xffffffff
        h4 = h4 + e & 0xffffffff

    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def sim_client(in_string):
    key = "YELLOW SUBMARINE"

    myhash = sha1(key + in_string)
    return myhash

#cheated a little with pad len
def SHA1_verify(in_string, pad_len):

    key = "YELLOW SUBMARINE"

    mac = in_string[0:40]
    message = in_string[40:]

    testhash = sha1(key + message)

    if testhash != mac:
        print "string has been tampered with"
    else:
        print "valid message: " + message[0:-pad_len]

def MD_pad_create(data):

    padding = chr(128) + chr(0) * (55 - len(data) % 64)
    if len(data) % 64 > 55:
        padding += chr(0) * (64 + 55 - len(data) % 64)
    padding = padding + pack('>Q', 8 * len(data))
    return padding

client_hash = sim_client("comment1=cooking MCs;userdata=foo;comment2= like a pound of bacon")

padding = MD_pad_create("AAAABBBBCCCCDDDDcomment1=cooking MCs;userdata=foo;comment2= like a pound of bacon")

a = int(client_hash[0:8],16)
b = int(client_hash[8:16],16)
c = int(client_hash[16:24],16)
d = int(client_hash[24:32],16)
e = int(client_hash[32:40],16)

forged_padding = MD_pad_create(";admin=true")

forged_mac = sha1_custom_args(";admin=true" + forged_padding, a,b,c,d,e)

SHA1_verify(forged_mac + "comment1=cooking MCs;userdata=foo;comment2= like a pound of bacon" + padding + ";admin=true" + forged_padding, len(forged_padding))