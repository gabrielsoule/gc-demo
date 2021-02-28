import bitstring, os, config, treelib, crypto_utils, circuit, random

class Alice:

    def __init__(self):
        self.circuit = circuit.Circuit() # the circuit which Alice will garble
        self.wire_labels = dict() # a mapping of each wire to its two labels (secret!)
        self.input_wires = dict() # the wires which Alice will supply input to, mapped to their corresponding inputs. Values of this dictionary are secret!

    def random_bitstring(self, k):
        raw_bytes = os.urandom(k)
        bits = bitstring.Bits(bytes=raw_bytes)       
        return bits

    def generate_labels(self):
        for w in self.circuit.wires:
            self.wire_labels[w] = (self.random_bitstring(config.LABEL_SIZE), self.random_bitstring(config.LABEL_SIZE))
            print("ALICE: Generating labels for wire {}: 0 = {}, 1 = {}".format(w, str(self.wire_labels[w][0].hex), str(self.wire_labels[w][1].hex)))

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
                print("    Encrypting label {} with ({}, {}), for {} = {} {} {}".format(lout.hex, l1.hex, l2.hex, output_bit, gate.op, selection[0], selection[1]))

                encrypted_label = crypto_utils.encrypt(l1, crypto_utils.encrypt(l2, lout))
                print("    Encrypted label: " + str(encrypted_label.hex))
                gate.table.append(encrypted_label)


    def permute_entries(self):
        for gate_id in self.circuit.tree.expand_tree(mode=treelib.Tree.DEPTH):
            gate = self.circuit.tree.get_node(gate_id).data
            print("ALICE: Shuffling garbled table for gate " + str(gate))
            random.shuffle(gate.table)
    
    def reveal_result(self, label):
        labels = self.wire_labels[self.circuit.tree.root]
        if labels[0] == label:
            print("Alice reveals the label {} for output wire {} equals: 0".format(label, self.circuit.tree.root))
        else:
            print("Alice reveals the label {} for output wire {} equals: 1".format(label, self.circuit.tree.root))
        
    
    

    