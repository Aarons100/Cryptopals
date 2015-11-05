from Crypto.Cipher import AES
import base64
import random
import sys
import os
import binascii
import struct

def CTR_Encrypt(ptxt, key,secret):
	cipher = AES.new(key,AES.MODE_CTR, counter = lambda: secret)
	return cipher.encrypt(ptxt)

def CTR_Decrypt(ctxt,key):
	result = ""
	for i in xrange(0,4):
		secret = "\x00"*8 + struct.pack("B",i) + "\x00"*7
		AES_CTR = AES.new(key,AES.MODE_CTR, counter = lambda: secret)
		result += AES_CTR.decrypt(ctxt)[i*16:(i+1)*16]
	return result

string = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
string = base64.b64decode(string)

secret = "\x00"*8 + "\x03" + "\x00"*7
key = "YELLOW SUBMARINE"

ptxt = CTR_Decrypt(string,key)

print ptxt

test = CTR_Encrypt()