from Crypto.Hash import HMAC
import time
def HMAC_wrapper(key,text):
	h = HMAC.new(key)
	h.update(text)

	return h.hexdigest()

def insecure_compare(a,b):

	if len(a) != len(b):
		print "len mismatch"
		return 1
	for i in xrange(0,len(a)):
		if a[i] != b[i]:
			#print "comparing " + a[i] + " " + b[i]
			return 1
		time.sleep(0.05)
	return 0

def server_sim(text,signature):

	key = "YELLOW SUBMARINE"
	text_hash = HMAC_wrapper(key,text)

	if insecure_compare(text_hash,signature) == 0:
		return "OK"
	else:
		return "ERROR"

myhash = HMAC_wrapper("YELLOW SUBMARINE","test")
print myhash

before = time.time()
test_str = "d" + "0"*31
insecure_compare(myhash,test_str)
print time.time() - before

before = time.time()
test_str = "cb" + "0"*30
insecure_compare(myhash,test_str)
print time.time() - before

sol = ""

for i in xrange(0,0xff):
	for j in xrange(0,0xff):
		diff = 0
		before = time.time()
		test_str = chr(i) + chr(j) + "0"*30
		server_sim("test",test_str)
		diff = time.time() - before
		#print diff
		if diff < 0.11 and diff > 0.055: 
			#print chr(i)
			sol += chr(i)
			break

print sol
for _ in xrange(0,120):
	for j in xrange(0,0xff):
		diff = 0
		before = time.time()
		foo = 31 - len(sol)
		test_str = sol + chr(j) + "0"*foo
		server_sim("test",test_str)
		diff = time.time() - before
		#print diff, chr(j)

		if diff < 0.11 + 0.5*len(sol) and diff > 0.06*len(sol): 
			print chr(j)
			sol += chr(j)
			break

print sol