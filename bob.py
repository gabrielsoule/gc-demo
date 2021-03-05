import config, ot, treelib, crypto_utils, label


class Bob:

    def __init__(self):
        # the garbled circuit that Bob will evaluate
        self.circuit = treelib.Tree()

        # the wires which Bob will supply input to, mapped to their boolean values.
        # Values of this dictionary are secret!
        self.input_wires = dict()

        # a mapping of wire identifiers to wire labels, which Bob will progressively fill out during evaluation
        # wire identifier -> wire label
        self.known_labels = dict()

    '''
    Simulate a series of oblivious transfers in which Bob requests labels
    corresponding to his input from Alice
    '''

    def request_labels(self, alice):
        for wire in self.input_wires:
            if config.USE_SIMPLEST_OT:
                # in a real application, Bob wouldn't be able to access Alice's wires like this...
                # this is just a simulation.
                label = ot.simplest_OT(alice.wire_labels[wire][0], alice.wire_labels[wire][1], self.input_wires[wire])
                # print("BOB: assigns label {} to wire {}".format(label, wire)) 
                self.known_labels[wire] = label

    def evaluate(self):
        return self._evaluate(self.circuit.tree.root)

    '''
    Helper function for recursive evaluation of a garbled circuit.
    Evaluates the label of the specfied wire.
    If the wire corresponds to the output of a gate,
    it evaluates that gate based on the (recursively evaluated)
    values of the gate's two input wires.
    Otherwise, the wire is an input wire, and it returns that wire's label.
    '''

    def _evaluate(self, wire):
        gate_node = self.circuit.tree.get_node(wire)

        # in the tree, gates are identified by the identifiers of their output wires.
        # if the gate corresponding to this wire exists, evaluate it recursively, 
        # otherwise the wire must be an input wire
        if gate_node:
            gate = gate_node.data
            l1 = self._evaluate(gate.in1)
            l2 = self._evaluate(gate.in2)
            out_label = None
            print("BOB: Evaluating gate {} with input wire labels {} = {}, {} = {}".format(str(gate), gate.in1, l1,
                                                                                           gate.in2, l2))
            if config.USE_FREE_XOR and gate.op == "XOR":
                out_label = self._evaluate_gate_free_XOR(gate, l1, l2)
            else:
                if config.USE_POINT_PERMUTE:
                    out_label = self._evaluate_gate_pp(gate, l1, l2)
                else:
                    out_label = self._evaluate_gate(gate, l1, l2)
            print("BOB: Successfully decrypted label {} for wire {}".format(out_label, wire))
            self.known_labels[wire] = out_label
            return out_label
        else:  # this
            return self.known_labels[wire]

    '''
    Evaluate a gate classically, without P&P/GRR3/FREE-XOR/ETC
    Bob will try and decrypt up to four entries in the table.
    '''

    def _evaluate_gate(self, gate, l1, l2):
        out_label = None
        for entry in gate.table:
            try:
                out_label = label.from_bitstring(crypto_utils.decrypt(l2, crypto_utils.decrypt(l1, entry)))
                break
            except ValueError as e:
                print("BOB: Failed to decrypt {}! Trying next entry...".format(entry.hex))
        if out_label is None:
            print(
                "ERROR: Bob was unable to decrypt all four encrypted entries of gate {}. This should never happen. Terminating program...".format(
                    str(gate)))
        return out_label

    '''
    Evaluate a gate using the point-and-permute optimization.
    '''

    def _evaluate_gate_pp(self, gate, l1, l2):
        # as we learned in the section on point-and-permute,
        # we select the (2 * r1 + r2)th entry in the table
        label_index = l1.pp_bit[0] * 2 + l2.pp_bit[0]
        print("BOB: Using point-and-permute. {}{} = {}; decrypting entry {} with ciphertext {}".format(
            l1.pp_bit.bin, l2.pp_bit.bin,
            label_index, label_index, gate.table[label_index]))
        return label.from_bitstring(crypto_utils.decrypt(l2, crypto_utils.decrypt(l1, gate.table[label_index])))

    '''
    Evaluate a gate using the free-XOR optimization.
    '''

    def _evaluate_gate_free_XOR(self, gate, l1, l2):
        out_label = label.from_bitstring(l1.to_bitstring() ^ l2.to_bitstring())
        print("BOB: Using Free-XOR; computing {} XOR {} = {}".format(l1, l2, out_label))
        return label.from_bitstring(l1.to_bitstring() ^ l2.to_bitstring())  # it's that easy!
