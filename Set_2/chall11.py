from Crypto import Random
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

def detect(ctxt):
	return 0

for i in xrange(0,10):
	print "Run #",i+1

	target = "A"*50
	foo = "=" * (5+ ord(os.urandom(1)) % 6)
	target = foo + target + foo

	target = pad(target,16)

	rand_key = os.urandom(16)
	IV = os.urandom(16)

	if (ord(os.urandom(1)) % 2):
		print "\tUsing ECB\t"
		result = ECB_Encrypt(target,rand_key)
	else:	
		print "\tUsing CBC"
		result = CBC_Encrypt(target,rand_key,IV)
	bar = binascii.hexlify(result)
	if result[16:32] == result[32:48]:
		print "\tFound ECB"
	else:
		print "\tFound CBC"
