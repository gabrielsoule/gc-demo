# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes, padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Padding

from bitstring import BitArray, Bits





'''
Utility class that abstracts away our crypto operations
'''

'''
Encrypt the bitstring message m with bitstring using AES in ECB mode. We employ SHA-256 to expand the key to 256 bits,
and use PKCS7 padding for the message.
ECB is not secure for long multi-block messages, but we are only encrypting labels in our GC implementation, which are generally
smaller than 256 bits, and do not contain repetitive sequences of characters

Returns a bitstring 
'''
# def encrypt(k, m):
#     digest = hashes.Hash(hashes.SHA256())
#     digest.update(k.bytes)
#     k_hash = digest.finalize() # hash k
#     # to verify whether a message was successfully decrypted, we check if these zeroes are present on the deciphered plaintext
#     # in a real life implementation, a proper verification method like HMAC might be employed.
#     m = m.copy() 
#     m.prepend(Bits(hex='0x0000'))
#     padder = padding.PKCS7(256).padder()
#     padded_m =  padder.update(m.bytes) + padder.finalize()
#     encryptor = Cipher(algorithms.AES(k_hash), modes.ECB(), backend=default_backend()).encryptor()
#     c_bytes = encryptor.update(padded_m) + encryptor.finalize()
#     c = BitArray(bytes=c_bytes)
#     return c

def encrypt(k, m):
    sha256 = SHA256.new(k.bytes) # since our labels may not be 128/256/512 bits, we hash them to derive an AES key
    k_hash = sha256.digest()

    # prepend zeroes to m; this is a very simple way to verify successful decryption of a message
    # It is only required for vanilla GC with no optimizations.
    # with point and permute, there is no need to guess and check by decrypting blindly.
    # in a real application proper authentication measures should be employed to mitigate tampering
    m = Bits(hex='0x0000') + m 

    padded_m = Padding.pad(m.bytes, 16, style='pkcs7')
    encryptor = AES.new(k_hash, AES.MODE_ECB) # again, for simplicity, use ECB - labels are generally smaller th
    # cipher.encrypt(padded_m)
    c = encryptor.encrypt(padded_m)
    return Bits(bytes=c)


def decrypt(k, c):
    sha256 = SHA256.new(k.bytes) # since our labels may not be 128/256/512 bits, we hash them to derive an AES key
    k_hash = sha256.digest()

    decryptor = AES.new(k_hash, AES.MODE_ECB)
    padded_m = decryptor.decrypt(c)
    m_bytes = Padding.unpad(padded_m, 16, style='pkcs7')
    m = Bits(bytes=m_bytes)
    if m[0:16] == '0x0000':
        return m[16:] 
    else:
       raise ValueError("Failed to decrypt message " + str(c) + " with key " + str(k)) 

# def decrypt(k, c):
#     digest = hashes.Hash(hashes.SHA256())
#     digest.update(k.bytes)
#     k = digest.finalize()

#     decryptor = Cipher(algorithms.AES(k), modes.ECB(), backend=default_backend()).decryptor()
#     padded_m = decryptor.update(c) + decryptor.finalize()
#     unpadder = padding.PKCS7(256).unpadder()
#     m_bytes = unpadder.update(padded_m) + unpadder.finalize()
#     m = BitArray(bytes=m_bytes)
#     if m[0:4] == '0x0':
#         return m
#     else:
#         raise ValueError("Failed to decrypt message " + str(c) + " with key " + str(k)) 



 