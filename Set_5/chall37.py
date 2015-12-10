#sending 0 as the Client A value causes Server_S = 0, 
#if the Client sets Client_S to 0, the server authenticates the client
#regardless of the password.

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Hash import HMAC

import random
import os
import struct
import math
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

server_N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
server_g = 2
server_k = 3
server_p = "YELLOW SUBMARINE"

client_N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
client_g = 2
client_k = 3
client_I = "sedlaa@rpi.edu"
client_p = "YELLOW "

#Server Init code
random.seed()

server_salt = os.urandom(16)
h = SHA256.new()
h.update(server_salt + server_p)
xH = h.digest()
x = int(xH.encode("hex"),16)

server_v = modexp(server_g,x,server_N)

#send I, A to Server
server_I = client_I

client_a = struct.unpack("<I",os.urandom(4))[0] % client_N
client_A = 0
server_A = client_A
#send salt ,B from server to client
client_salt = server_salt

server_b = struct.unpack("<I",os.urandom(4))[0] % server_N
server_B = server_k*server_v + modexp(server_g,server_b,server_N)
client_B = server_B
#server and client compute string uH = SHA256(A|B), and u

h = SHA256.new()

h.update(str(server_A) + str(server_B))
uH = h.digest()

server_u = int(uH.encode("hex"),16)

h = SHA256.new()
h.update(str(client_A) + str(client_B))
uH = h.digest()

client_u = int(uH.encode("hex"),16)

#Client does some calculations

h = SHA256.new()
h.update(client_salt + client_p)
xH = h.digest()

x = int(xH.encode("hex"),16)

#client_S = modexp(client_B - client_k * pow(client_g,x),client_a + client_u * x,client_N)
client_S = 0
print "client S =",client_S
h = SHA256.new()
h.update(str(client_S))
client_K = h.digest()

server_S = modexp(server_A * modexp(server_v,server_u,server_N),server_b,server_N)
print "server S =", server_S
h = SHA256.new()
h.update(str(server_S))
server_K = h.digest()

#Client send HMAC-SHA256(K,salt)
client_hash = hmac.new(str(client_K),client_salt,hashlib.sha256).digest()

server_hash_from_client = client_hash
#Server send ok if HMAC validates

server_hash = hmac.new(str(server_K),server_salt,hashlib.sha256).digest()

if server_hash_from_client == server_hash:
	print "OK"
else: 
	print "ERROR"

