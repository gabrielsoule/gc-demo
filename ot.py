import crypto_utils, bitstring, random
from Crypto.Util import number

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    return x % m

def RSA_OT(alice, bob):
    pass


'''
Simulates the simple OT scheme proposed in https://users-cs.au.dk/orlandi/simpleOT/
m1, m2 are the two messages; i is the index. In accordance with the writeup notation,
let Alice be the sender and Bob the receiver.
In a real implementation, we would employ twisted Edwards curves as the paper suggests.
Since this is a toy implementation, we will the multiplicative group of integers modulo p for some small prime p
so that computations can be verified manually without too much difficulty if desired.

This implementation is NOT cryptographically secure whatsoever;
it exists to demonstrate the simple OT protocol using a toy group (Z_p) with toy parameters (<2^16)

'''
def simplest_OT(m0, m1, i):
    print("OT: Alice, the sender, has messages m0 = {} and m1 = {}. Bob, the receiver wishes to receive message m{}.".format(m0, m1, i))
    # the finite group of integers upon which we operate; 65521 is the largest 16 bit prime. 
    # We use a group of prime order so that every element is a generator
    G = 65521 

    g = random.randint(2, G) # this value is agreed upon by both parties, and shared

    a = random.randint(2, 2 ** 16 - 1) # Sender (Alice's) secret a
    b = random.randint(2, 2 ** 16 - 1) # Receiver (Bob's) secret b

    print("OT: Alice generates a = {}, and keeps a secret from Bob".format(a))
    print("OT: Bob generates b = {}, and keeps b secret from Alice".format(b))


    A = (g ** a) % G
    print("OT: Alice transfers A = g^a = {} to Bob".format(A))
    B = 0
    if i == 0:
        B = (g ** b) % G
        print("OT: Since i = 0, Bob calculates B = g^b = {} and transfers it to Alice".format(B))
    elif i == 1:
        B = (((g ** b) % G) * A) % G
        print("OT: Since i = 0, Bob calculates B = Ag^b = {} and transfers it to Alice".format(B))
    else:
        raise ValueError("The receiver must choose an index from (0, 1)")
    
    k = (A ** b) % G
    print("OT: Bob transfers B to Alice, and computes k = A^b = {}".format(k))

    k0 = (B ** a) % G
    k1 = (((B * modinv(A, G) % G)) ** a) % G
    print("OT: Alice computes k0 = B^a = {}, kl (B/A)^a = {}".format(k0, k1))
    c0 = crypto_utils.encrypt(bitstring.Bits(uint=k0, length=2 ** 16), m0)
    c1 = crypto_utils.encrypt(bitstring.Bits(uint=k1, length=2 ** 16), m1)
    print("OT: Alice encrypts m0 with key k0 and transfers to Bob c0 = E(k0, m0) = {}".format(c0))
    print("OT: Alice encrypts m1 with key k1 and transfers to Bob c1 = E(k1, m1) = {}".format(c1))

    if i == 0:
        decrypted_c0 = crypto_utils.decrypt(bitstring.Bits(uint=k, length=2 ** 16), c0.bytes)
        print("OT: Bob successfully decrypts c0 to yield " + decrypted_c0.hex)
        # assert(decrypted_c0 == m0)
        return decrypted_c0
    else:
        decrypted_c1 = crypto_utils.decrypt(bitstring.Bits(uint=k, length=2 ** 16), c1.bytes)
        print("OT: Bob successfully decrypts c0 to yield " + decrypted_c1.hex)
        return decrypted_c1
        




