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
		target += "\x00"

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

#create dictionary
dictionary = []
for i in xrange(0,256):
	foo = "A"* 15 + chr(i)
	bar = ECB_Encrypt(foo,rand_key)
	dictionary.append(binascii.hexlify(bar))
#create random prepend
num_bytes = random.randint(0,128)
rand_prepend = os.urandom(num_bytes)

base = binascii.hexlify(ECB_Encrypt("B"*16,rand_key))

for i in xrange(0,16):

	ptxt = rand_prepend + "B"*32 + "B"*i + string	
	ctxt = ECB_Encrypt(pad(ptxt,16),rand_key) 
	result = binascii.hexlify(ctxt).split(base)

	if len(result) == 3:
		break

	#print result

sol = ""
for i in xrange(0,len(string)):

	for j in xrange(0,16):

		ptxt = rand_prepend + "B"*32 + "B"*j + "A"*15 + string[i:]	
		ctxt = ECB_Encrypt(pad(ptxt,16),rand_key) 
		result = binascii.hexlify(ctxt).split(base)

		if len(result) == 3:
			ctxt = result[2]
			break

	for j in xrange(0,256):

		if ctxt[0:32] == dictionary[j]:
			sol += chr(j)

print sol
#print result