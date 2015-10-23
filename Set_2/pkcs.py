
myinput = raw_input("Input: ")
padlen = int(raw_input("Block Size: "))

pad = padlen - (len(myinput) % padlen)

for i in xrange(0,pad):
	myinput += "="

print myinput