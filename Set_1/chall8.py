from Crypto import Random
from Crypto.Cipher import AES
import base64

f = open('7.txt','r')
i = open('7.txt','r')

for line in f.readline():

	for line2 in i.readline():

f.close()

target = base64.b64decode(target)

key = b'YELLOW SUBMARINE'

cipher = AES.new(key, AES.MODE_ECB)

print cipher.decrypt(target)