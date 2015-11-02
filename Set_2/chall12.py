from Crypto.Cipher import AES
import base64
import random
import sys
import os
import binascii

def pad(my_input,block_size):

	target = my_input
	pad = block_size - (len(target) % block_size)
	for i in xrange(0,pad):
		target += "\x04"

	return target

def ECB_Encrypt(target, key):

	cipher = AES.new(key,AES.MODE_ECB)
	return cipher.encrypt(target)

def CBC_Encrypt(target,key, IV):

	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.encrypt(target)

random.seed()

string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
string = base64.b64decode(string)
rand_key = os.urandom(16)

dictionary = []

for i in xrange(0,256):

	foo = "A"* 15 + chr(i)
	bar = ECB_Encrypt(foo,rand_key)
	dictionary.append(binascii.hexlify(bar))

sol = ""
for i in xrange(0,len(string)):

	ptxt = "A"*15 + string[i]
	ptxt = pad(ptxt, 16)

	ctxt = binascii.hexlify(ECB_Encrypt(ptxt,rand_key))

	for j in xrange(0,256):

		if ctxt[0:32] == dictionary[j]:
			sol += chr(j)

print sol