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
            # in a real application, Bob wouldn't be able to access Alice's wires like this...
            # this is just a simulation.
            label = ot.simplest_OT(alice.wire_labels[wire][0], alice.wire_labels[wire][1], self.input_wires[wire])
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
                if config.USE_GRR3:
                    out_label = self._evaluate_gate_grr3(gate, l1, l2)
                elif config.USE_POINT_PERMUTE:
                    out_label = self._evaluate_gate_pp(gate, l1, l2)
                else:
                    out_label = self._evaluate_gate_standard(gate, l1, l2)
            print("BOB: Successfully decrypted label {} for wire {}".format(out_label, wire))
            self.known_labels[wire] = out_label
            return out_label
        else:  # this
            return self.known_labels[wire]

    '''
    Evaluate a gate classically, without P&P/GRR3/FREE-XOR/ETC
    Bob will try and decrypt up to four entries in the table.
    '''

    def _evaluate_gate_standard(self, gate, l1, l2):
        out_label = None
        for entry in gate.table:
            try:
                candidate = crypto_utils.decrypt(l2, crypto_utils.decrypt(l1, entry))
                # with the AES implementation we are using, it seems that the padding check
                # functions as a way to verify correct decryption, since if a message isn't padded right that probably
                # means we don't have the right keys. But it's still good practice to verify the label is correct anyway.
                if candidate[0:config.CLASSIC_SECURITY_PARAMETER * 8].int == 0:
                    out_label = label.from_bitstring(candidate)
                    break
                else:
                    raise ValueError()
            except ValueError:
                print("BOB: Failed to decrypt {}! Trying next entry...".format(entry.hex))
        if out_label is None:
            print(
                "ERROR: Bob was unable to decrypt all four encrypted entries of gate {}. This should never happen. "
                "Terminating program...".format(
                    str(gate)))
        return out_label

    '''
    Evaluate a gate using the point-and-permute optimization.
    '''

    def _evaluate_gate_grr3(self, gate, l1, l2):
        if l1.pp_bit == l2.pp_bit == 0:
            return label.from_bitstring(crypto_utils.decrypt(l2, crypto_utils.decrypt(l1, bytes(16))))
        else:
            return self._evaluate_gate_pp(gate, l1, l2)

    def _evaluate_gate_pp(self, gate, l1, l2):
        # as we learned in the section on point-and-permute,
        # we select the (2 * r1 + r2)th entry in the table
        label_index = l1.pp_bit * 2 + l2.pp_bit
        print("BOB: Using point-and-permute. {}{} = {}; decrypting entry {} with ciphertext {}".format(
            int(l1.pp_bit), int(l2.pp_bit),
            label_index, label_index, gate.table[label_index]))
        return label.from_bitstring(crypto_utils.decrypt(l2, crypto_utils.decrypt(l1, gate.table[label_index])))

    '''
    Evaluate a gate using the free-XOR optimization.
    '''

    def _evaluate_gate_free_XOR(self, gate, l1, l2):
        out_label = label.from_bitstring(l1.to_bitstring() ^ l2.to_bitstring())
        print("BOB: Using Free-XOR; computing {} XOR {} = {}".format(l1, l2, out_label))
        return out_label  # it's that easy!
