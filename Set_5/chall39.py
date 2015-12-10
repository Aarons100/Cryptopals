from Crypto.Util import number
import random

def modexp ( g, u, p ):
	"""computes s = (g ^ u) mod p
	args are base, exponent, modulus
	(see Bruce Schneier's book, _Applied Cryptography_ p. 244)"""
	s = 1
	while u != 0:
		if u & 1:
			s = (s * g)%p
		u >>= 1
		g = (g * g)%p;
	return s

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
    else:
        return x % m

random.seed()

while 1:

	p = number.getPrime(64)
	q = number.getPrime(64)

	n = p * q

	et = (p-1)*(q-1)
	#print et
	e = 3

	d = modinv(e,et)
	if d != -1:
		break

print d

print "p = ",p
print "q = ",q

print "public key e = ",e
print "private key d = ",d
ptxt = 42
ctxt = modexp(ptxt,e,n)

print ctxt

print modexp(ctxt,d,n)