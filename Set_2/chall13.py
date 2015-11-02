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

def ECB_Decrypt(target, key):

	#target = pad(target,16)
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(target)

def parse_function(my_input):
	result = "{\n"
	foo = my_input.split("&")

	for i in xrange(0,len(foo)):
		result +="\t" + foo[i].replace("=",": '") + "'\n"
	result += "}"
	return result

def profile_for(in_string):
	foo = "email=" + in_string + "&uid=" + str(random.randint(0,99)) + "&role=user"
	return foo

random.seed()

string = profile_for("aarons104@gmail.com")

rand_key = os.urandom(16)
print binascii.hexlify(ECB_Encrypt(pad(string,16),rand_key))
dictionary = []

for i in xrange(0,256):

	foo = "A"*15 + chr(i)
	bar = ECB_Encrypt(foo,rand_key)
	dictionary.append(binascii.hexlify(bar))

sol = ""
for i in xrange(0,len(string)):

	ptxt = "A"*15+ string[i]
	ptxt = pad(ptxt, 16)

	ctxt = binascii.hexlify(ECB_Encrypt(ptxt,rand_key))
	print ctxt
	for i in xrange(0,256):

		if ctxt[0:32] == dictionary[i]:
			sol += chr(i)

print sol

sol = sol[0:len(sol)-4]
sol += "admin"
print sol

adm_cipher = ECB_Encrypt(pad(sol,16),rand_key)

ciph = ECB_Decrypt(adm_cipher,rand_key)

print parse_function(ciph)