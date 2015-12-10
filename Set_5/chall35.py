#if MITM sets g = p, you can decrypt the plaintext with s = 0
#if MITM sets g = 0, B is set to 0, you can calculate server_s
# if MITM sets g = p-1, B is set to 1 or the modulus, you can calculate server_s

from Crypto.Cipher import AES
from Crypto.Hash import SHA

import random
import os
import struct
import math
import binascii

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

def CBC_Encrypt(target,key, IV):

	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.encrypt(target)

def CBC_Decrypt(target,key,IV):

	cipher = AES.new(key,AES.MODE_CBC,IV)
	return cipher.decrypt(target)

random.seed()
#init servervariables
server_p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
server_g = 2
server_a = struct.unpack("<I",os.urandom(4))[0] % server_p
server_A = modexp(server_g,server_a,server_p)

#Send p,g,A to mitm
MITM_p = server_p
MITM_g = server_g
MITM_A = server_A

#Send p,g,p to client

client_p = MITM_p
#client_g = MITM_g
client_g = MITM_p - 1
client_A = MITM_A

#Send B to MITM
client_b = struct.unpack("<I",os.urandom(4))[0] % client_p
client_B = modexp(client_g,client_b,client_p)

MITM_B = client_B

#send p to Server
print "MITM B = ",MITM_B
print "p = ",MITM_p
server_B = MITM_B

#send AES ciphertext to MITM
server_s = modexp(server_B,server_a,server_p)

h = SHA.new()
h.update(str(server_s))

server_key = h.digest()[0:16]
server_msg = "YELLOW SUBMARINE"
server_iv = os.urandom(16)
server_Ctxt = CBC_Encrypt(server_msg,server_key,server_iv) + server_iv
#actual send
MITM_Ctxt = server_Ctxt

#MITM attack GOES HERE ---------------------------------------

MITM_s = 0

h = SHA.new()
h.update(str(MITM_s))

MITM_key = h.digest()[0:16]
MITM_Ptxt = CBC_Decrypt(MITM_Ctxt[0:16],MITM_key,MITM_Ctxt[16:])

print "MITM PTXT: ",MITM_Ptxt

#-------------------------------------------------------------

#send Ctxt to client
client_Ctxt = MITM_Ctxt

#Decrypt, re-encrypt with new IV, send back
client_s = modexp(client_A,client_b,client_p)

h = SHA.new()
h.update(str(client_s))

client_key = h.digest()[0:16]
client_Ptxt = CBC_Decrypt(client_Ctxt[0:16],client_key,client_Ctxt[16:])
client_iv = os.urandom(16)

client_Ctxt_new = CBC_Encrypt(client_Ptxt,client_key,client_iv) + client_iv
#actual send
MITM_Ctxt_new = client_Ctxt_new

#relay from MITM to server

server_Ctxt_new = MITM_Ctxt_new