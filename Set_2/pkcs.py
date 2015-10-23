
myinput = raw_input("Input: ")

pad = 32 - (len(myinput) % 32)

for i in xrange(0,pad):
	myinput += "="

print myinput