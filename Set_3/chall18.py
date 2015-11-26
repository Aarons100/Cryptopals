from Crypto.Cipher import AES
import base64
import random
import sys
import os
import binascii
import struct
import math

def AES_CTR(ptxt,key,nonce):
	keystream = ""
	cipher = AES.new(key,AES.MODE_ECB)
	block_len = int(math.ceil(len(ptxt)/16))
	if len(ptxt) % 16:
		block_len += 1
	print "block count:", block_len

	for i in xrange(0,block_len):

		target = nonce + struct.pack("<I",i) + "\x00"*4
		#print binascii.hexlify(target) 
		keystream += cipher.encrypt(target)
	result = ""
	for i in xrange(0,len(ptxt)):
		result += chr(ord(ptxt[i]) ^ ord(keystream[i]))

	return result

string = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
string = base64.b64decode(string)

key = "YELLOW SUBMARINE"
nonce = "\x00"*8

print binascii.hexlify(string)
result = AES_CTR(string,key,nonce)
print result

resultB = AES_CTR(result,key,nonce)

print binascii.hexlify(resultB)

print AES_CTR(resultB,key,nonce)
"""
secret = "\x00"*8 + "\x03" + "\x00"*7
key = "YELLOW SUBMARINE"

ptxt = CTR_Decrypt(string,key)

print ptxt

test = CTR_Encrypt()
"""
