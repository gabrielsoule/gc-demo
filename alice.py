import os
import random

import bitstring
import treelib

import circuit
import config
import crypto_utils
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

        # the random R value for free-XOR. Only used if free-XOR is enabled

        if config.USE_FREE_XOR:
            if config.USE_POINT_PERMUTE:
                self.R = bitstring.Bits(bytes=os.urandom(16))
            else:
                # if we are using free-xor and NOT using point-and-permute, we need to to make sure R has the proper
                # zero bits just like the labels, otherwise things get messed up!
                self.R = bitstring.Bits(bytes=bytes(config.CLASSIC_SECURITY_PARAMETER)) + bitstring.Bits(
                    bytes=os.urandom(16 - config.CLASSIC_SECURITY_PARAMETER))
            config.R = self.R
            print("ALICE: Generating random R = {}".format(self.R.hex))

    def generate_labels(self):
        for w in self.circuit.wires:
            self.wire_labels[w] = label.generate_pair()
            print("ALICE: Generating labels for wire {}: 0 = {}, 1 = {}".format(w, self.wire_labels[w][0],
                                                                                self.wire_labels[w][1]))

    '''
    Generate labels for wires, and garble gates accordingly. We do this by recursively garbling the current gate's
    two parent gates, and then garbling the current gate.
    
    In the writeup, we generate labels (in no specific order) for each wire, and once all labels are generated THEN 
    we garble the gates (in no specific order) according to these labels. In this implementation, however, 
    we generate labels and garble gates at the same time, and we do so in an ordered depth-first fashion. 
    
    The reason for this discrepancy is that when Free-XOR is enabled, an XOR gate's output wire labels depend on the 
    input wire labels. And those input wires may be the output wires for another gate, and so on and so forth. This 
    imposes a dependency structure on the circuit in which gates cannot be garbled until their preceding gates have been 
    garbled. Therefore, we cannot generate labels and garble gates in any order we like; a hierarchical label 
    generation/garbling process is required. '''

    def garble_gates(self):
        self.garble_gate(self.circuit.tree.root)

    '''
    Recursively garble a gate. Returns a pair label of labels corresponding to the gate's output wire. 
    This method is similar to the evaluator's recursive evaluation method; both traverse the tree in the same way.
    '''

    def garble_gate(self, wire):
        gate_node = self.circuit.tree.get_node(wire)

        # in the tree, gates are identified by the identifiers of their output wires.
        # if the gate corresponding to this wire exists, evaluate it recursively,
        # otherwise the wire must be an input wire
        if gate_node:
            gate = gate_node.data
            in1_labels = self.garble_gate(gate.in1)
            in2_labels = self.garble_gate(gate.in2)
            if gate.op == 'XOR' and config.USE_FREE_XOR:
                return self.garble_gate_free_XOR(gate, in1_labels, in2_labels)
            else:
                if config.USE_GRR3:
                    return self.garble_gate_grr3(gate, in1_labels, in2_labels)
                else:
                    return self.garble_gate_standard(gate, in1_labels, in2_labels)
        else:
            labels = label.generate_pair()
            self.wire_labels[wire] = labels
            print("ALICE: Generating labels for wire {}: 0 = {}, 1 = {}".format(wire, labels[0], labels[1]))
            return labels  # wire is an input wire, so just generate a fresh pair of labels

    '''
    Garble a gate using the GRR3 optimization. Compatible with Free-XOR. 
    '''

    def garble_gate_grr3(self, gate, in1_labels, in2_labels):
        pass

    '''
    Garble a XOR gate using the free-XOR technique. 
    '''

    def garble_gate_free_XOR(self, gate, in1_labels, in2_labels):
        out_labels = label.generate_pair()
        print("ALICE: Generating labels for wire {}: 0 = {}, 1 = {}".format(gate.out, out_labels[0], out_labels[1]))
        out_labels[0].bits = in1_labels[0].bits ^ in2_labels[0].bits
        out_labels[1].bits = out_labels[0].bits ^ self.R
        out_labels[0].pp_bit = in1_labels[0].pp_bit ^ in2_labels[0].pp_bit
        out_labels[1].pp_bit = in1_labels[0].pp_bit ^ in2_labels[0].pp_bit ^ True
        self.wire_labels[gate.out] = out_labels
        return out_labels

    '''
    Garble a gate using the standard vanilla approach. No frills! 
    '''

    def garble_gate_standard(self, gate, in1_labels, in2_labels):
        print("ALICE: Garbling gate {} ".format(gate))
        gate.table = []
        out_labels = label.generate_pair()  # grab us a fresh set of labels
        print("ALICE: Generating labels for wire {}: 0 = {}, 1 = {}".format(gate.out, out_labels[0], out_labels[1]))
        self.wire_labels[gate.out] = out_labels
        for selection in [(0, 0), (0, 1), (1, 0), (1, 1)]:  # for each possible input configuration...
            # grab the labels corresponding to that configuration
            l1 = in1_labels[selection[0]]
            l2 = in2_labels[selection[1]]
            output_bit = None
            if gate.op == 'OR':
                output_bit = selection[0] or selection[1]
            elif gate.op == 'AND':
                output_bit = selection[0] and selection[1]
            elif gate.op == 'XOR':
                output_bit = selection[0] ^ selection[1]
            else:
                raise ValueError("Gate {} has an invalid binary operation ({})".format(gate, gate.op))
            lout = out_labels[output_bit]
            print(
                "    Encrypting label {} with {}, {}, for {} = {} {} {}".format(lout, l1, l2, output_bit,
                                                                                selection[0], gate.op,
                                                                                selection[1]))
            encrypted_label = crypto_utils.encrypt(l1, crypto_utils.encrypt(l2, lout))
            self.encrypted_entries[encrypted_label] = (l1, l2)  # cache ciphertext -> keys, to make it easier to p&p
            print("    Encrypted label: " + str(encrypted_label.hex))
            gate.table.append(encrypted_label)
        return out_labels

    # Legacy gate garbling function
    # def garble_gates(self):
    #     for gate_id in self.circuit.tree.expand_tree(mode=treelib.Tree.DEPTH):
    #         gate = self.circuit.tree.get_node(gate_id).data
    #         print("ALICE: Garbling gate {} ".format(gate))
    #         gate.table = []
    #         for selection in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    #             l1 = self.wire_labels[gate.in1][selection[0]]
    #             l2 = self.wire_labels[gate.in2][selection[1]]
    #             output_bit = None
    #             if gate.op == 'OR':
    #                 output_bit = selection[0] or selection[1]
    #             elif gate.op == 'AND':
    #                 output_bit = selection[0] and selection[1]
    #             elif gate.op == 'XOR':
    #                 output_bit = selection[0] ^ selection[1]
    #             else:
    #                 raise ValueError("Gate {} has an invalid binary operation ({})".format(gate, gate.op))
    #
    #             lout = self.wire_labels[gate.out][output_bit]
    #             print(
    #                 "    Encrypting label {} with {}, {}, for {} = {} {} {}".format(lout, l1, l2, output_bit,
    #                                                                                 selection[0], gate.op,
    #                                                                                 selection[1]))
    #             encrypted_label = crypto_utils.encrypt(l1, crypto_utils.encrypt(l2, lout))
    #             self.encrypted_entries[encrypted_label] = (l1, l2)
    #             print("    Encrypted label: " + str(encrypted_label.hex))
    #             gate.table.append(encrypted_label)

    def permute_entries(self):
        for gate_id in self.circuit.tree.expand_tree(mode=treelib.Tree.DEPTH):
            gate = self.circuit.tree.get_node(gate_id).data

            #  if it is not the case that the gate is XOR AND we are using free-xor, then process normally
            if not (gate.op == 'XOR' and config.USE_FREE_XOR):
                if config.USE_POINT_PERMUTE:
                    gate.table = sorted(gate.table,
                                        key=lambda entry:
                                        2 * self.encrypted_entries[entry][0].pp_bit + self.encrypted_entries[entry][
                                            1].pp_bit)
                    print("ALICE: Shuffling garbled table according to select bits. The final order is:")
                    for e in gate.table:
                        print("    {}{}: {}".format(self.encrypted_entries[e][0].pp_bit,
                                                    self.encrypted_entries[e][1].pp_bit, e.hex))
                else:
                    print("ALICE: Randomly shuffling garbled table for gate " + str(gate))
                    random.shuffle(gate.table)
            else:
                print("ALICE: Nothing to permute for gate {}; XOR gates under free-XOR have no entries".format(gate))

    def reveal_result(self, l):
        labels = self.wire_labels[self.circuit.tree.root]
        if labels[0] == l:
            print("Alice reveals the label {} for output wire {} equals: 0".format(l, self.circuit.tree.root))
        elif labels[1] == l:
            print("Alice reveals the label {} for output wire {} equals: 1".format(l, self.circuit.tree.root))
        else:
            raise ValueError("The output label Bob computed, {}, does not match either of the output labels ({}, "
                             "{}). This should never happen.".format(l, labels[0], labels[1]))
