import circuit
import config
import crypto_utils
import random
import treelib
import label


class Alice:

    def __init__(self):
        self.circuit = circuit.Circuit()  # the circuit which Alice will garble
        # a mapping of each wire to its two labels (secret!)
        self.wire_labels = dict()

        # the wires which Alice will supply input to, mapped to their corresponding inputs. 
        # Values of this dictionary are secret!
        self.input_wires = dict()

        # a mapping of encrypted values to entry pairs. We cache this so that, if point-and-permute is enabled we can
        # sort encrypted values according to their select bits without having to decrypt. We intentionally garble
        # gates separately from permuting gates, and do it after encryption, to match the accompanying written
        # tutorial.
        self.encrypted_entries = dict()

    def generate_labels(self):
        for w in self.circuit.wires:
            self.wire_labels[w] = label.generate_pair()
            print("ALICE: Generating labels for wire {}: 0 = {}, 1 = {}".format(w, self.wire_labels[w][0],
                                                                                self.wire_labels[w][1]))

    def garble_gates(self):
        for gate_id in self.circuit.tree.expand_tree(mode=treelib.Tree.DEPTH):
            gate = self.circuit.tree.get_node(gate_id).data
            print("ALICE: Garbling gate {} ".format(gate))
            gate.table = []
            for selection in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                l1 = self.wire_labels[gate.in1][selection[0]]
                l2 = self.wire_labels[gate.in2][selection[1]]
                output_bit = None
                if gate.op == 'OR':
                    output_bit = selection[0] or selection[1]
                elif gate.op == 'AND':
                    output_bit = selection[0] and selection[1]
                elif gate.op == 'XOR':
                    output_bit = selection[0] ^ selection[1]
                else:
                    raise ValueError("Gate {} has an invalid binary operation ({})".format(gate, gate.op))

                lout = self.wire_labels[gate.out][output_bit]
                print(
                    "    Encrypting label {} with {}, {}, for {} = {} {} {}".format(lout, l1, l2, output_bit,
                                                                                    selection[0], gate.op,
                                                                                    selection[1]))
                encrypted_label = crypto_utils.encrypt(l1, crypto_utils.encrypt(l2, lout))
                self.encrypted_entries[encrypted_label] = (l1, l2)
                print("    Encrypted label: " + str(encrypted_label.hex))
                gate.table.append(encrypted_label)

    def permute_entries(self):
        for gate_id in self.circuit.tree.expand_tree(mode=treelib.Tree.DEPTH):
            gate = self.circuit.tree.get_node(gate_id).data
            if config.USE_POINT_PERMUTE:
                gate.table = sorted(gate.table,
                                    key=lambda entry:
                                    2 * self.encrypted_entries[entry][0].pp_bit.bin + self.encrypted_entries[entry][
                                        1].pp_bit.bin)
                print("ALICE: Shuffling garbled table according to select bits. The final order is:")
                for e in gate.table:
                    print("    {}{}: {}".format(self.encrypted_entries[e][0].pp_bit.bin,
                                                self.encrypted_entries[e][1].pp_bit.bin, e.hex))
            else:
                print("ALICE: Randomly shuffling garbled table for gate " + str(gate))
                random.shuffle(gate.table)

    def reveal_result(self, l):
        labels = self.wire_labels[self.circuit.tree.root]
        if labels[0] == l:
            print("Alice reveals the label {} for output wire {} equals: 0".format(l, self.circuit.tree.root))
        elif labels[1] == l:
            print("Alice reveals the label {} for output wire {} equals: 1".format(l, self.circuit.tree.root))
        else:
            raise ValueError("The output label Bob computed, {}, does not match either of the output labels ({}, "
                             "{}). This should never happen.".format(l, labels[0], labels[1]))
