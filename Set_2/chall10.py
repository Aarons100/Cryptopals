from Crypto import Random
from Crypto.Cipher import AES
import base64
import sys

def pad(my_input,block_size):

	target = my_input
	pad = block_size - (len(target) % block_size)

	for i in xrange(0,pad):
		target += "\x00"

	return target

def ECB_Encrypt(target, key):

	target = pad(target,16)
	cipher = AES.new(key,AES.MODE_ECB)
	print cipher.encrypt(target)

def ECB_Decrypt(target, key):

	#target = pad(target,16)
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.decrypt(target)

#xor two byte sequences of same len
def xor(data,vector):
	result = ""
	for i in xrange(0,len(data)):
		result += chr(ord(data[i]) ^ ord(vector[i]))
	return result

def CBC_Decrypt(data,key,IV):

	#pad just in case
	data = pad(data,16)

	num_blocks = len(data)/16
	print "blocks:" , num_blocks
	result = ""
	for i in xrange(0,len(data),16):

		foo = ECB_Decrypt(data[i:i+16],key)
		result += xor(foo,IV)
		IV = data[i:i+16]
	return result

key = 'YELLOW SUBMARINE'
IV = "\x00"*16

data_file = sys.argv[1]

f = open(data_file,'r')
target = f.read()
f.close()

target = base64.b64decode(target)

print CBC_Decrypt(target,key,IV)
##cipher = AES.new(key,AES.MODE_CBC, IV)

##print cipher.decrypt(target)

#ECB_Decrypt(target, key)