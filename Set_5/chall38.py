from Crypto.Hash import SHA256

import random
import os
import struct
import binascii
import hmac
import hashlib

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

#server Init stuff
server_N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
server_g = 2
server_k = 3
server_p = "YELLOW SUBMARINE"

client_N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
client_g = 2
client_k = 3
client_I = "sedlaa@rpi.edu"
client_p = "YELLOW SUBMARINE"

random.seed()
server_salt = os.urandom(16)
#x = SHA256(salt|password)
h = SHA256.new()
h.update(server_salt + server_p)
xH = h.digest()
x = int(xH.encode("hex"),16)
#v = g**x % n
server_v = modexp(server_g,x,server_N)

#Client send I, A = g**a % n, to Server
client_a = struct.unpack("<I",os.urandom(4))[0] % client_N
client_A = modexp(client_g,client_a,client_N)
#actual send
server_I = client_I
server_A = client_A

#S->C: salt, B = g**b % n, u = 128 bit random number
server_u = os.urandom(16)
server_b = struct.unpack("<I",os.urandom(4))[0] % server_N
server_B = modexp(server_g,server_b,server_N)

#actual sending:
client_u = server_u
client_B = server_B
client_salt = server_salt

#Client compute x = SHA256(salt|password),S = B**(a + ux) % n,K = SHA256(S)

h = SHA256.new()
h.update(client_salt + client_p)
xH = h.digest()
x = int(xH.encode("hex"),16)

client_u = int(client_u.encode("hex"),16)

client_S = modexp(client_B,client_a + client_u *x,client_N)

h = SHA256.new()
h.update(str(client_S))
client_K = h.digest()

#Server compute S = (A * v ** u)**b % n, K = SHA256(S)
server_u = int(server_u.encode("hex"),16)
server_S = modexp(server_A *modexp( server_v,server_u,server_N),server_b,server_N)

h = SHA256.new()
h.update(str(server_S))
server_K = h.digest()

#C->S Send HMAC-SHA256(K, salt)
client_hash = hmac.new(str(client_K),client_salt,hashlib.sha256).digest()

server_hash_from_client = client_hash
#Server send ok if HMAC validates

server_hash = hmac.new(str(server_K),server_salt,hashlib.sha256).digest()

if server_hash_from_client == server_hash:
	print "OK"
else: 
	print "ERROR"