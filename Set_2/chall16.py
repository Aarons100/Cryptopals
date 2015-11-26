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

def unpad(plaintext):
	pad = ord(plaintext[-1])
	all_padding = plaintext[-pad:]
	for byte in all_padding:
		if ord(byte) != pad:
			print "mismatch"
			break
	return plaintext[0:-len(all_padding)]

def CBC_Encrypt(target,key, IV):

	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.encrypt(target)

def CBC_Decrypt(target,key,IV):

	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.decrypt(target)

def encrypt(user_input, rand_key, IV):

	result = "comment1=cooking%20MCs;userdata=" + user_input + ";comment2=%20like%20a%20pound%20of%20bacon"
	result = pad(result,16)

	return CBC_Encrypt(result, rand_key,IV)

def print_string(inp):

	foo = 0
	for i in inp:
		print foo, hex(ord(i)), i
		foo +=1
		if foo % 16 == 0:
			print
	print inp

def decrypt(ctxt, rand_key, IV):
	ptxt = CBC_Decrypt(ctxt,rand_key,IV)
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
	return result

random.seed()
rand_key = "A"*16
IV = "B"*16

output = encrypt("AAAAAAAAAAAAAAAA",rand_key,IV)
flipbits = binascii.unhexlify("52d5cbe5e1e99128abc61a")
flipbit = output[33]
new_ctxt = output[0:33] + flipbits + output[44:]

print len(output), len(new_ctxt)

for i in flipbit:
	print hex(ord(i))
print_string(new_ctxt)
diff = decrypt(new_ctxt,rand_key,IV)

