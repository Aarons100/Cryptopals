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
				print "padding mismatch"
				return text[:-pad]
		return text[:-pad]

def CBC_Encrypt(target,key, IV):
	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.encrypt(target)

def CBC_Decrypt(target,key,IV):
	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.decrypt(target)

rand_key = "YELLOW SUBMARINE"
IV = rand_key

ctxt = CBC_Encrypt("F"*16 + "G"*16 + "H"*16,rand_key,IV)

#print binascii.hexlify(ctxt)
ctxt_1 = ctxt[0:16]
ctxt_2 = ctxt[16:32]
ctxt_3 = ctxt[32:48]

new_ctxt = ctxt_1 + "\x00"*16 + ctxt_1

newest_ptxt = CBC_Decrypt(new_ctxt,rand_key,IV)

for i in xrange(0,len(newest_ptxt)):

	if ord(newest_ptxt[i]) > 0x7f:
		print "nonascii found"

		key = ""
		for i in xrange(0,16):
			key += chr(ord(newest_ptxt[i]) ^ ord(newest_ptxt[i+32]))

		print "key = ", key
		break