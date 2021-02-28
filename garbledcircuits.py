from bitstring import *
from alice import Alice
from bob import Bob
from circuit import Circuit
import random
import ot

AND = "AND"
OR = "OR"
XOR = "XOR"

# How many bits should each label be?
LABEL_SIZE = 16 

# Since we are using AES and the evaluator needs to know whether decryption is successful,
# we append a number of zero bits to each label. 
SECURITY_PARAMETER = 16 

wires = dict()

# Simple container class for a garbled gate.
# We often use the identifier for a gate's output wire to uniquely identify the gate,
# since every gate has a unique output wire. 
class LogicGate:
    

    def __init__(self):
        self.op = ""
        self.in1 = ""
        self.in2 = ""
        self.out = ""
        self.table = []

    def __str__(self):
        return "{} <- {} {} {}".format(self.out, self.in1, self.op, self.in2)

# We're going to map the output wire identifier of each gate to the gate itself
# This makes our tree construction much more efficient!
gates = dict()

alice = Alice()
bob = Bob()

def main():
    # In this implementation we store wires as strings, whose values are those supplied by the user. 
    # These strings uniquely identify the corresponding wire. Not to be confused with labels, for which there are 
    # two for every unique wire!
    print("Welcome! Please define your circuit by entering a sequence of logic gate specifications of the form \"z = x OP y\", where:") 
    print(" - x and y are identifiers that uniquely specify the gate's two input wires, ")
    print(" - z is an identifier that uniquely specifies the gate's output wire")
    print(" - OP is the gate operation, which is one of \"and\", \"or\", \"xor\"")
    print("Please enter one logic gate per line. When you are finished defining gates and are ready to proceed, please enter a blank line.")
    out_wires = []
    in_wires = []
    while True:
        gate_info = input()
        if not gate_info:
            break
        gate_info = gate_info.split()
        gate = LogicGate()
        if gate_info[3] == "and":
            gate.op = AND
        elif gate_info[3] == "or":
            gate.op = OR
        elif gate_info[3] == "xor":
            gate.op = XOR
        else: 
            raise ValueError("Operation must be one of \"and\", \"or\", \"xor\"")

        gate.in1 = gate_info[2]
        gate.in2 = gate_info[4]
        gate.out = gate_info[0]
        
        gates[gate.out] = gate

        wires[gate.in1] = ""
        wires[gate.in2] = ""
        wires[gate.out] = ""

        in_wires.append(gate.in1)
        in_wires.append(gate.in2)
        out_wires.append(gate.out)

        wires[gate_info[0]] = ""
        wires[gate_info[2]] = ""
        wires[gate_info[4]] = ""


    input_wires = []
    output_wires = []

    for w in wires: # select the wires that are ONLY input and ONLY output
        if w in in_wires and w not in out_wires:
            input_wires.append(w)
        if w in out_wires and w not in in_wires:
            output_wires.append(w)
    

    
    print("Detected the following INPUT wires:  " + str(input_wires))
    print("Detected the following OUTPUT wires: " + str(output_wires))


    alice_wires = []
    alice_wire_values = []
    bob_wires = []
    bob_wire_values = []

    print("Among the input wires " + str(input_wires)  + ", which are supplied by Alice, the garbler? Please enter the wire identifiers seperated by commas.")
    alice_wires = input().split(",")

    if len(alice_wires) > 0: # Alice has at least one input
        print("What are Alice's boolean input values? Please enter a sequence of 0s and 1s corresponding to her input wires, separated by commas.")
        alice_wire_values = list(map(int, input().split(",")))

        # ...therefore, the remaining inputs must be owned by Bob
        for w in input_wires:
            if w not in alice_wires:
                bob_wires.append(w)
        
        if len(bob_wires) > 0:
            print("The remaining input wires, " + str(bob_wires), " must be supplied by Bob. Please enter a sequence of 0s and 1s corresponding to his input wires, separated by commas.")
            bob_wire_values = list(map(int, input().split(",")))
        else:
            print("Assuming all inputs are supplied by Alice, and Bob only evaluates.")

    else: # Alice has no inputs; all inputs must be owned by Bob
        print("Assuming all inputs are supplied by Bob, the evaluator. What are Bob's boolean input values? Please enter a sequence of 0s and 1s corresponding to his input wires, separated by commas.")
        bob_input_values = input().split(",")

    #TODO Instead of exiting, handle bad user input gracefully.
    assert(len(alice_wires) == len(alice_wire_values))
    assert(len(bob_wire_values) == len(bob_wire_values))
    
    alice.input_wires = dict(zip(alice_wires, alice_wire_values))
    bob.input_wires = dict(zip(bob_wires, bob_wire_values))
    
    
    print()
    print("Successfully generated the following circuit: ")
    circuit = Circuit()
    # at the moment, we only support one output wire; hence output_wires[0]
    # but the infrastructure is in place to change this, if we so desire
    # to do this, we would likely have to represent the circuit as a digraph instead of a tree
    # and reimplement our construction and evaluation algorithms accordingly 
    circuit.build(output_wires[0], gates) 
    circuit.tree.show()

    # Give the circuit to Alice to garble
    alice.circuit = circuit

    # Instruct Alice to generate labels
    alice.generate_labels()

    # Instruct Alice to garble gates using the generated labels
    alice.garble_gates()

    # Instruct Alice to permute the garbled tables 
    alice.permute_entries()

    # Transfer the circuit to Bob
    bob.circuit = alice.circuit 
    
    for wire in alice.input_wires:
        # Transfer the labels corresponding to Alice's input to Bob
        bob.known_labels[wire] = alice.wire_labels[wire][alice.input_wires[wire]]
    
    # Simulate OT between Alice and Bob so that Bob can acquire labels corresponding to his input
    bob.request_labels(alice)
    
    # Instruct Bob to evaluate the circuit
    result = bob.evaluate()
    
    # Instruct Alice to reveal the result of Bob's computation
    alice.reveal_result(result)

    

    
    

    






    




    # print("ALICE: Generating random labels for all wires...")
    # for w in wires:
    #     alice.wires_0[w] = random_bitstring(LABEL_SIZE)
    #     alice.wires_1[w] = random_bitstring(LABEL_SIZE)
    #     print("  {} = (0, 1) => ({}, {})".format(w, alice.wires_0[w], alice.wires_1[w]))
    




main()