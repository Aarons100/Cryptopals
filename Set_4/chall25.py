from Crypto.Cipher import AES
import base64
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

def AES_CTR_EDIT(ctxt, key, nonce, offset, new_ptxt):
	keystream = ""
	cipher = AES.new(key,AES.MODE_ECB)
	block_len = int(math.ceil(len(ctxt)/16))
	if len(ptxt) % 16:
		block_len += 1

	for i in xrange(0,block_len):
		target = nonce + struct.pack("<I",i) + "\x00"*4
		keystream += cipher.encrypt(target)

	result = ""

	for i in xrange(0,offset):
		result += ctxt[i]
	for i in xrange(0,len(new_ptxt)):
		result += chr(ord(new_ptxt[i]) ^ ord(keystream[offset+i]))
	for i in xrange(offset+len(new_ptxt),len(ctxt)):
		result += ctxt[i]

	return result	
	
#open input
f = open("./25.txt","r")
ctxt = f.read()
f.close()
#aes ECB decrypt
ctxt = base64.b64decode(ctxt)
key = 'YELLOW SUBMARINE'
cipher = AES.new(key, AES.MODE_ECB)
ptxt = cipher.decrypt(ctxt)
#CTR encrypt
mynonce = "\x00"*8
ctr_ctxt = AES_CTR(ptxt,key,mynonce)

print AES_CTR_EDIT(ctr_ctxt,key,mynonce,0,ctr_ctxt)
