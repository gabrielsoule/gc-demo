import bitstring
import config
import os

'''
Generate a pair of labels for a wire.
It's important to use this function for generation,
since select bits for a wire's two labels must be different
for point-and-permute to work properly.

Since labels often come in pairs, it's generally best to use this method whenever possible.
'''


def generate_pair():
    if config.USE_POINT_PERMUTE:
        l1 = Label(bitstring.BitArray(os.urandom(16)), os.urandom(1)[0] & 1)
        l2 = Label(bitstring.BitArray(os.urandom(16)), not l1.pp_bit)
    else:
        l1 = Label(bitstring.BitArray(8 * config.CLASSIC_SECURITY_PARAMETER) + bitstring.BitArray(os.urandom(14)), 0)
        l2 = Label(bitstring.BitArray(8 * config.CLASSIC_SECURITY_PARAMETER) + bitstring.BitArray(os.urandom(14)), 0)

    # If Free-XOR is enabled, Alice generates the '1' label for a wire as the '0' label XORed with her secret R
    # Intuitively, this is secure: Bob only ever uncovers one of two possible labels for every wire. Bob cannot learn
    # about the other label without knowing R, and Bob cannot learn about R without knowing the other label, and
    # fortunately for Alice, Bob knows neither.
    # Note that if Bob is able to determine both labels for a wire, the protocol fails and everything blows up,
    # since with both labels Bob can uncover R.
    # This is one of the justifications for OT (instead of Alice just giving Bob both labels)
    if config.USE_FREE_XOR:
        l2.bits = l1.bits ^ config.R
        l2.bits[len(l2.bits) - 1] = not l1.bits[len(l1.bits) - 1]

    return l1, l2


'''
Decode a label's bitstring into a Label object. 
'''


def from_bitstring(bits):
    return Label(bits, bits[len(bits) - 1])
    #
    # if config.USE_POINT_PERMUTE:
    #     return Label(bits[0:config.LABEL_SIZE * 8], bitstring.Bits(bool=bits[config.LABEL_SIZE * 8]))
    # else:
    #     return Label(bits, 0)  # don't care about the select bit, it can be whatever


'''
Represents a Label for a certain wire. Since a label can have various metadata encoded within (such as select bits 
for point-and-permute), this class abstracts away some of that complexity. 

A label does not know which wire it corresponds to, or the semantic value it encodes. We let the two parties handle 
that in their own ways, as they would in a real world implementation. This adds some complexity, but it does nicely 
model who would know what information in a real-world scenario.

A label is represented as a 128-bit bitstring, whose last bit is the point-and-permute bit, resulting in a key space 
of 127 bits (2^127). If point-and-permute is not enabled, then the first 16 bits (by default) of a label are zero, 
which is used as a security parameter to verify proper decryption. In this case, the key space is 112 bits (2^112). 

'''


class Label:

    def __init__(self, bits, pp_bit):
        self.bits = bits
        self.pp_bit = pp_bit
        self.bits[len(self.bits) - 1] = pp_bit

    def __str__(self):
        if config.LABEL_BYTES_TO_PRINT > 0:
            label_string = "{}...".format(self.bits[0:config.LABEL_BYTES_TO_PRINT * 8].hex)
        else:
            label_string = str(self.bits.hex)

        if config.USE_POINT_PERMUTE:
            return "({}, pp_bit = {})".format(label_string, int(self.pp_bit))
        else:
            return str(self.bits.hex)

    '''
    Encode this label, and any associated metadata like select bits, as a single bitstring. 
    In our implementation, we encode the point-and-permute bit as the last bit of the bitstring
    Therefore, the true length of a label is one less than the given security parameter
    '''

    def to_bitstring(self):
        # update the bitstring value, in case the pp_bit has been messed with
        self.bits[len(self.bits) - 1] = self.pp_bit
        return self.bits
        # if config.USE_POINT_PERMUTE:
        #     # We want the bitstring to be a multiple of 8 bits long, so we can easily convert it into
        #     # bytes for encryption. We therefore append seven extra bits to the end of the bitstring form.
        #     return self.bits + self.pp_bit + bitstring.Bits(bin='0000000')
        # else:
        #     return self.bits

    def __eq__(self, other):
        if config.USE_POINT_PERMUTE:
            return self.bits == other.bits and self.pp_bit == other.pp_bit
        else:
            return self.bits == other.bits
