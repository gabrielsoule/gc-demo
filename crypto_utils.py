# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes, padding
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util import Padding

import bitstring
import label

'''
Encrypt a label/bitstring using AES in ECB mode. We employ SHA-256 to expand the key to 256 bits, and use PKCS7 padding for the message.
ECB is not secure for long multi-block messages, but we are only encrypting labels in our GC implementation, which are generally
smaller than 256 bits, and do not contain repetitive sequences of characters. 

Returns a bitstring. 
'''


def encrypt(k, m):
    if type(m) == label.Label:
        m = m.to_bitstring()
    if type(k) == label.Label:
        k = k.to_bitstring()
    sha256 = SHA256.new(k.bytes)  # since our labels may not be 128/256/512 bits, we hash them to derive an AES key
    k_hash = sha256.digest()

    # prepend zeroes to m; this is a very simple way to verify successful decryption of a message
    # It is only required for vanilla GC with no optimizations.
    # with point and permute, there is no need to guess and check by decrypting blindly.
    # in a real application proper authentication measures should be employed to mitigate tampering
    m = bitstring.Bits(hex='0x0000') + m

    padded_m = Padding.pad(m.bytes, 16, style='pkcs7')
    encryptor = AES.new(k_hash,
                        AES.MODE_ECB)  # again, for simplicity, use ECB - labels are generally smaller than blocks
    c = encryptor.encrypt(padded_m)
    return bitstring.Bits(bytes=c)


'''
Corresponding decryption function for encrypt(k, m)
'''


def decrypt(k, c):
    if type(k) == label.Label:
        k = k.to_bitstring().bytes
    if type(k) == bitstring.Bits:
        k = k.bytes
    if type(c) == bitstring.Bits:
        c = c.bytes
    sha256 = SHA256.new(k)  # since our labels may not be 128/256/512 bits, we hash them to derive an AES key
    k_hash = sha256.digest()

    decryptor = AES.new(k_hash, AES.MODE_ECB)
    padded_m = decryptor.decrypt(c)
    m_bytes = Padding.unpad(padded_m, 16, style='pkcs7')
    m = bitstring.Bits(bytes=m_bytes)
    if m[0:16] == '0x0000':
        return m[16:]
    else:
        raise ValueError("Failed to decrypt message " + str(c) + " with key " + str(k))
