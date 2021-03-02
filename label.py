import bitstring
import config
import os

'''
Generate a pair of labels for a wire.
It's important to use this function for generation,
since select bits for a wire's two labels must be different
for point-and-permute to work properly.
'''


def generate_pair():
    # generate a random select bit
    l1 = Label(bitstring.Bits(os.urandom(config.LABEL_SIZE)), bitstring.Bits(bin=str(os.urandom(1)[0] & 1)))
    l2 = Label(bitstring.Bits(os.urandom(config.LABEL_SIZE)), l1.pp_bit ^ '0b1')  # invert the other label's select bit
    return l1, l2


'''
Decode a label's bitstring into a Label object.
Essentially this method extracts the select bit from the bitstring.
'''


def from_bitstring(bits):
    if config.USE_POINT_PERMUTE:
        return Label(bits[0:config.LABEL_SIZE * 8], bitstring.Bits(bool=bits[config.LABEL_SIZE * 8]))
    else:
        return Label(bits, 0)  # don't care about the select bit, it can be whatever


'''
Represents a Label for a certain wire. Since a label can have various metadata encoded within (such as select bits 
for point-and-permute), this class abstracts away some of that complexity. 

A label does not know which wire it corresponds to, or the semantic value it encodes. We let the two parties handle 
that in their own ways, as they would in a real world implementation. 
'''


class Label:

    def __init__(self, bits, pp_bit):
        self.bits = bits
        self.pp_bit = pp_bit

    def __str__(self):
        if config.USE_POINT_PERMUTE:
            return "({}, pp_bit = {})".format(self.bits.hex, self.pp_bit.bin)
        else:
            return str(self.bits.hex)

    '''
    Encode this label, and any associated metadata like select bits, as a single bitstring.
    Useful for encryption.
    '''

    def to_bitstring(self):
        if config.USE_POINT_PERMUTE:
            # We want the bitstring to be a multiple of 8 bits long, so we can easily convert it into
            # bytes for encryption. We therefore append seven extra bits to the end of the bitstring form.
            return self.bits + self.pp_bit + bitstring.Bits(bin='0000000')
        else:
            return self.bits

    def __eq__(self, other):
        return self.bits == other.bits and self.pp_bit == other.pp_bit