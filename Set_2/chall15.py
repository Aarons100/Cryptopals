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
 
string = "ICE ICE BABY\x01\x02\x03\x04"

unpad(string)

string = "ICE ICE BABY"
string = pad(string,16)

string = unpad(string)

print string