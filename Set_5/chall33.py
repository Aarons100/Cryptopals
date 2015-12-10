import random
import os
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


random.seed()

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

a = struct.unpack("<I",os.urandom(4))[0] % p
b = struct.unpack("<I",os.urandom(4))[0] % p

#A = pow(g,a) % p
A = modexp(g,a,p)
B = modexp(g,b,p)
#B = pow(g,b) % p

#s1 = pow(B,a) % 37
s1 = modexp(B,a,p)
s2 = modexp(B,a,p)
#s2 = pow(A,b,p) % 37

print s1 - s2