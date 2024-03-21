import Crypto.Util.Padding
import Crypto.Cipher.AES
import Crypto.Random
import hashlib

def generate_key(password:bytes)->bytes:
	salt=Crypto.Random.get_random_bytes(16)
	key=hashlib.pbkdf2_hmac('sha256',password,salt,65536,32)
	return salt+key

def generate_key_with_given_salt(password:bytes,salt:bytes)->bytes:
	key=hashlib.pbkdf2_hmac('sha256',password,salt,65536,32)
	return key

def encode(plain_text:bytes,key:bytes)->bytes:
	block_size=Crypto.Cipher.AES.block_size
	iv=Crypto.Random.get_random_bytes(block_size)
	cipher=Crypto.Cipher.AES.new(key,Crypto.Cipher.AES.MODE_CBC,iv)
	text=cipher.encrypt(Crypto.Util.Padding.pad(plain_text,block_size))
	return iv+text

def decode(cipher_text:bytes,key:bytes)->bytes:
	block_size=Crypto.Cipher.AES.block_size
	iv=cipher_text[:block_size]
	cipher=Crypto.Cipher.AES.new(key,Crypto.Cipher.AES.MODE_CBC,iv)
	text=Crypto.Util.Padding.unpad(cipher.decrypt(cipher_text[block_size:]),block_size)
	return text
