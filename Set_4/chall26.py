from Crypto.Cipher import AES
import base64
import random
import sys
import os
import binascii
import math
import struct

def AES_CTR(ptxt,key,nonce):
	keystream = ""
	cipher = AES.new(key,AES.MODE_ECB)
	block_len = int(math.ceil(len(ptxt)/16))
	if len(ptxt) % 16:
		block_len += 1

	for i in xrange(0,block_len):
		target = nonce + struct.pack("<I",i) + "\x00"*4 
		keystream += cipher.encrypt(target)

	result = ""
	for i in xrange(0,len(ptxt)):
		result += chr(ord(ptxt[i]) ^ ord(keystream[i]))

	return result

def encrypt(user_input, rand_key, nonce):

	result = "comment1=cooking%20MCs;userdata=" + user_input + ";comment2=%20like%20a%20pound%20of%20bacon"

	return AES_CTR(result,rand_key,nonce)

def print_string(inp):

	foo = 0
	for i in inp:
		print foo, hex(ord(i)), i
		foo +=1
		if foo % 16 == 0:
			print
	print inp

def decrypt(ctxt, rand_key, nonce):
	ptxt = AES_CTR(ctxt,rand_key,nonce)
	print
	print_string(ptxt)
	print
	ptxt = ptxt.split(";")
	result = []	
	for i in ptxt:
		result.append(i.split("="))
	print result

	for i in result:
		if i[0] == "admin":
			if i[1] == "true":
				print "admin found"
	return result;

random.seed()
rand_key = "YELLOW SUBMARINE"
mynonce = "\x00"*8

output = encrypt("AAAAAAAAAAAAAAAA",rand_key,mynonce)
flipbits = binascii.unhexlify("16c1eaa678150a3fb1afd21d")
flipbit = output[32]
new_ctxt = output[0:32] + flipbits + output[44:]

print len(output), len(new_ctxt)
#print_string(new_ctxt)
for i in flipbit:
	print hex(ord(i))
print_string(new_ctxt)
#decrypt(ou,rand_key,IV)
diff = decrypt(new_ctxt,rand_key,mynonce)
