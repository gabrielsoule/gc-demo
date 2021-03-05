class Gate:
    def __init__(self):
        self.op = ''
        self.in1 = ''
        self.in2 = ''
        self.out = ''
        self.table = []

    def __str__(self):
        return "{} <- {} {} {}".format(self.out, self.in1, self.op, self.in2)