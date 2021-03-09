class Gate:
    def __init__(self):
        self.op = ''
        self.in1 = ''
        self.in2 = ''
        self.out = ''
        self.table = []

    '''
    Compute the output of this gate against two bits of input. 
    '''

    def run(self, i1, i2):
        output_bit = None
        if self.op == 'OR':
            output_bit = i1 or i2
        elif self.op == 'AND':
            output_bit = i1 and i2
        elif self.op == 'XOR':
            output_bit = i1 ^ i2
        else:
            raise ValueError("Gate {} has an invalid binary operation ({})".format(self, self.op))
        return output_bit

    def __str__(self):
        return "{} <- {} {} {}".format(self.out, self.in1, self.op, self.in2)
