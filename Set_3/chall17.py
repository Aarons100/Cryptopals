from Crypto.Cipher import AES
import base64
import random
import sys
import os
import binascii
import struct

class PKCS7Encoder():
	"""
	Technique for padding a string as defined in RFC 2315, section 10.3,
	note #2
	"""
	class InvalidBlockSizeError(Exception):
		pass

	def __init__(self, block_size=16):
		if block_size < 2 or block_size > 255:
			raise PKCS7Encoder.InvalidBlockSizeError('The block size must be between 2 and 255, inclusive')
		self.block_size = block_size

	def encode(self, text):
		text_length = len(text)
		amount_to_pad = self.block_size - (text_length % self.block_size)
		if amount_to_pad == 0:
			amount_to_pad = self.block_size
		pad = chr(amount_to_pad)
		return text + pad * amount_to_pad

	def decode(self, text):
		pad = ord(text[-1])

		all_padding = text[-pad:]
		for byte in all_padding:
			if ord(byte) != pad:
				#print "mismatch"
				return 1
		return 0

def CBC_Encrypt(target,key, IV):

	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.encrypt(target)

def CBC_Decrypt(target,key,IV):

	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.decrypt(target)

def client_sim(rand_key, IV):

	encoder = PKCS7Encoder()

	strings = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
	"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
	"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
	"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
	"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
	"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
	"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
	"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
	"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
	"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]

	target_string = strings[random.randint(0,9)]
	target_string = base64.b64decode(target_string)
	target_string = encoder.encode(target_string)

	return CBC_Encrypt(target_string,rand_key,IV)

def server_sim(ctxt, rand_key, IV):

	ptxt = CBC_Decrypt(ctxt,rand_key,IV)
	encoder = PKCS7Encoder()
	result = encoder.decode(ptxt)

	return result

random.seed()

rand_key = os.urandom(16)
IV = os.urandom(16)
Intermediate_ctxt = []
client_data = client_sim(rand_key,IV)

result = server_sim(client_data,rand_key,IV)
"""
num_blocks = len(client_data)/16
print "blocks",num_blocks

for i in xrange((num_blocks-1)*16,(num_blocks-2)*16,-1):
	for j in xrange(0,255):

		foo = client_data[0:i] + struct.pack("B",j) + client_data[i+1:]

		result = server_sim(foo,rand_key,IV)

		if result == 0:
			Intermediate_ctxt.append(struct.pack("B",j))
			break
for i in xrange(len(client_data)-1,-1,-1):

	print chr(ord(Intermediate_ctxt[i % 16]) ^ ord(client_data[i]))
"""