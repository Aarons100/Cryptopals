from Crypto.Util import number
import random
import binascii
import struct
import math

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

ptxt = "Hello World!"
ptxt_int = int(ptxt.encode("Hex"),16)
print hex(ptxt_int)
random.seed()

e_list = [3,5,7]
n_list = []
ctxt_list = []

#server encrypting same ptxt 3 times with 3 different public keys
for i in xrange(0,3):

	while 1:

		p = number.getPrime(64)
		q = number.getPrime(64)

		n = p * q

		et = (p-1)*(q-1)
		#print et
		e = e_list[i]

		d = modinv(e,et)
		if d != -1:
			break

	n_list.append(n)
	
	#print ptxt_int
	ctxt = modexp(ptxt_int,e,n)
	ctxt_list.append(ctxt)

#list of 3 captured public keys, and 3 ctxts
#print e_list
#print n_list
#print ctxt_list

print "n's = ",n_list
print "public key e = ",e_list
print "ctxt = ", ctxt_list

c_0 = ctxt_list[0] % n_list[0]
c_1 = ctxt_list[1] % n_list[1]
c_2 = ctxt_list[2] % n_list[2]

m_s_0 = n_list[1] * n_list[2]
m_s_1 = n_list[0] * n_list[2]
m_s_2 = n_list[0] * n_list[1]

N_012 = n_list[0] * n_list[1] * n_list[2]

r0 = c_0 * m_s_0 * modinv(m_s_0,n_list[0]) % N_012
r1 = c_1 * m_s_1 * modinv(m_s_1,n_list[1]) % N_012
r2 = c_2 * m_s_2 * modinv(m_s_2,n_list[2]) % N_012

result = r0 + r1 + r2

result = int(pow(result,1./3.))
print result
print ptxt_int

#print binascii.unhexlify(hex(modexp(ctxt,d,n))[2:-1])