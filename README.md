# gc-demo

gc-demo is a demonstrative implementation of garbled circuits, intended to accompany the tutorial found here: (https://www.notion.so/Garbled-Circuits-A-Tutorial-Introduction-b278c5ffe0114921be59de91074016ff). The application simulates the GC protocol between two parties, Alice and Bob, for a circuit specified by the user. The code is well documented and easy to understand, and the structure of the program follows closely the structure of the written tutorial. Each step of the protocol is displayed during execution.  

A number of common GC optimizations are implemented and can be enabled or disabled at will, such as point-and-permute, GRR3, and free-XOR. More advanced optimizations, such as FleXOR, GRR2, and Half-AND will be added eventually.

## Usage
Run `main.py` program from the command line, and follow the prompts to simulate a GC exchange. The command-line flags that can be enabled are:

```
optional arguments:
  -h, --help            show this help message and exit
  -pp POINT_PERMUTE, --point-permute POINT_PERMUTE
                        enable the point-and-permute optimization
  --free-xor FREE_XOR   enable the free-XOR optimization
```

Below is a transcript of a sample session with the point-and-permute optimization (and no other optimizations) enabled. The circuit evaluated is the same as the one evaluated in the corresponding tutorial linked above.

```
Optimization enabled: point-and-permute
Welcome! Please define your circuit by entering a sequence of logic gate specifications of the form "z = x OP y", where:
 - x and y are identifiers that uniquely specify the gate's two input wires,
 - z is an identifier that uniquely specifies the gate's output wire
 - OP is the gate operation, which is one of "and", "or", "xor"
Please enter one logic gate per line. When you are finished defining gates and are ready to proceed, please enter a blank line.
e = a and b
f = c and d
g = e and f

Detected the following INPUT wires:  ['a', 'b', 'c', 'd']
Detected the following OUTPUT wires: ['g']
Among the input wires ['a', 'b', 'c', 'd'], which are supplied by Alice, the garbler? Please enter the wire identifiers seperated by commas.
a,b
What are Alice's boolean input values? Please enter a sequence of 0s and 1s corresponding to her input wires, separated by commas.
0,1
The remaining input wires, ['c', 'd']  must be supplied by Bob. Please enter a sequence of 0s and 1s corresponding to his input wires, separated by commas.
1,1

Successfully generated the following circuit:
g <- e AND f
├── e <- a AND b
└── f <- c AND d


Alice generates labels for the circuit, and garbles gates accordingly:
ALICE: Generating labels for wire a: 0 = (0ce9..., pp_bit = 1), 1 = (291b..., pp_bit = 0)
ALICE: Generating labels for wire b: 0 = (8ca4..., pp_bit = 1), 1 = (da4c..., pp_bit = 0)
ALICE: Garbling gate e <- a AND b
ALICE: Generating labels for wire e: 0 = (1f5e..., pp_bit = 1), 1 = (16d8..., pp_bit = 0)
    Encrypting label (1f5e..., pp_bit = 1) with (0ce9..., pp_bit = 1), (8ca4..., pp_bit = 1), for 0 = 0 AND 0
    Encrypted label: 68cc2b6ddfadece531a0604ce3b00ba0
    Encrypting label (1f5e..., pp_bit = 1) with (0ce9..., pp_bit = 1), (da4c..., pp_bit = 0), for 0 = 0 AND 1
    Encrypted label: 969b1fb44922c58fc8d3990dd5b19957
    Encrypting label (1f5e..., pp_bit = 1) with (291b..., pp_bit = 0), (8ca4..., pp_bit = 1), for 0 = 1 AND 0
    Encrypted label: d58651783c9a8aa6affa9913065ebbe4
    Encrypting label (16d8..., pp_bit = 0) with (291b..., pp_bit = 0), (da4c..., pp_bit = 0), for 1 = 1 AND 1
    Encrypted label: 08e2e6857d3d5295e7a43290b1bac7df
ALICE: Generating labels for wire c: 0 = (ad74..., pp_bit = 1), 1 = (d36a..., pp_bit = 0)
ALICE: Generating labels for wire d: 0 = (7353..., pp_bit = 0), 1 = (ef1a..., pp_bit = 1)
ALICE: Garbling gate f <- c AND d
ALICE: Generating labels for wire f: 0 = (258c..., pp_bit = 0), 1 = (ad2d..., pp_bit = 1)
    Encrypting label (258c..., pp_bit = 0) with (ad74..., pp_bit = 1), (7353..., pp_bit = 0), for 0 = 0 AND 0
    Encrypted label: 820c67a5ebf9320d2c1cd1c05f497dc5
    Encrypting label (258c..., pp_bit = 0) with (ad74..., pp_bit = 1), (ef1a..., pp_bit = 1), for 0 = 0 AND 1
    Encrypted label: 4d1f393177c98ad7467be7003d2a2fd1
    Encrypting label (258c..., pp_bit = 0) with (d36a..., pp_bit = 0), (7353..., pp_bit = 0), for 0 = 1 AND 0
    Encrypted label: baa7cbb2c5ff6e2e056d9a05dd0e92b9
    Encrypting label (ad2d..., pp_bit = 1) with (d36a..., pp_bit = 0), (ef1a..., pp_bit = 1), for 1 = 1 AND 1
    Encrypted label: 52d008eddf63ef6a7327028d82b1cbd5
ALICE: Garbling gate g <- e AND f
ALICE: Generating labels for wire g: 0 = (7bf8..., pp_bit = 0), 1 = (9ebe..., pp_bit = 1)
    Encrypting label (7bf8..., pp_bit = 0) with (1f5e..., pp_bit = 1), (258c..., pp_bit = 0), for 0 = 0 AND 0
    Encrypted label: d545f01258f587ba460c10dac80584bc
    Encrypting label (7bf8..., pp_bit = 0) with (1f5e..., pp_bit = 1), (ad2d..., pp_bit = 1), for 0 = 0 AND 1
    Encrypted label: a6dd033055afb14ea7b3a2966096776c
    Encrypting label (7bf8..., pp_bit = 0) with (16d8..., pp_bit = 0), (258c..., pp_bit = 0), for 0 = 1 AND 0
    Encrypted label: 4297f67f1b438033f2f05f143d874d56
    Encrypting label (9ebe..., pp_bit = 1) with (16d8..., pp_bit = 0), (ad2d..., pp_bit = 1), for 1 = 1 AND 1
    Encrypted label: 77e2889e5c1dcac85d04c3ac16473a94

Alice permutes the entries in each garbled gate's garbled truth table:
ALICE: Shuffling garbled table according to select bits. The final order is:
    00: 4297f67f1b438033f2f05f143d874d56
    01: 77e2889e5c1dcac85d04c3ac16473a94
    10: d545f01258f587ba460c10dac80584bc
    11: a6dd033055afb14ea7b3a2966096776c
ALICE: Shuffling garbled table according to select bits. The final order is:
    00: 08e2e6857d3d5295e7a43290b1bac7df
    01: d58651783c9a8aa6affa9913065ebbe4
    10: 969b1fb44922c58fc8d3990dd5b19957
    11: 68cc2b6ddfadece531a0604ce3b00ba0
ALICE: Shuffling garbled table according to select bits. The final order is:
    00: baa7cbb2c5ff6e2e056d9a05dd0e92b9
    01: 52d008eddf63ef6a7327028d82b1cbd5
    10: 820c67a5ebf9320d2c1cd1c05f497dc5
    11: 4d1f393177c98ad7467be7003d2a2fd1

Alice transfers the circuit to Bob.

Bob uses OT to request from Alice labels corresponding to his input bits:
OT: Alice, the sender, has messages m0 = (ad74..., pp_bit = 1) and m1 = (d36a..., pp_bit = 0). Bob, the receiver wishes to receive message m1.
OT: Alice generates a = 19113, and keeps a secret from Bob
OT: Bob generates b = 17381, and keeps b secret from Alice
OT: Alice transfers A = g^a = 35500 to Bob
OT: Since i = 0, Bob calculates B = Ag^b = 17147 and transfers it to Alice
OT: Bob transfers B to Alice, and computes k = A^b = 28153
OT: Alice computes k0 = B^a = 20573, kl (B/A)^a = 28153
OT: Alice encrypts m0 with key k0 and transfers to Bob c0 = E(k0, m0) = 0x8e09905df9bbc1f1c59dc6c2a82087bb
OT: Alice encrypts m1 with key k1 and transfers to Bob c1 = E(k1, m1) = 0xaca002b38e969824e39500bcdf7fc21b
OT: Bob successfully decrypts c0 to yield (d36a..., pp_bit = 0)
OT: Alice, the sender, has messages m0 = (7353..., pp_bit = 0) and m1 = (ef1a..., pp_bit = 1). Bob, the receiver wishes to receive message m1.
OT: Alice generates a = 36150, and keeps a secret from Bob
OT: Bob generates b = 15195, and keeps b secret from Alice
OT: Alice transfers A = g^a = 45455 to Bob
OT: Since i = 0, Bob calculates B = Ag^b = 60103 and transfers it to Alice
OT: Bob transfers B to Alice, and computes k = A^b = 12009
OT: Alice computes k0 = B^a = 15918, kl (B/A)^a = 12009
OT: Alice encrypts m0 with key k0 and transfers to Bob c0 = E(k0, m0) = 0xe4e1c66bf854abfcdcee8600aed5ad07
OT: Alice encrypts m1 with key k1 and transfers to Bob c1 = E(k1, m1) = 0x4474af7dbb2700036a4c27fe7d630140
OT: Bob successfully decrypts c0 to yield (ef1a..., pp_bit = 1)

Bob proceeds to evaluate the circuit:
BOB: Evaluating gate e <- a AND b with input wire labels a = (0ce9..., pp_bit = 1), b = (da4c..., pp_bit = 0)
BOB: Using point-and-permute. 10 corresponds to entry 2; decrypting entry 2 with ciphertext 0x969b1fb44922c58fc8d3990dd5b19957
BOB: Successfully decrypted label (1f5e..., pp_bit = 1) for wire e
BOB: Evaluating gate f <- c AND d with input wire labels c = (d36a..., pp_bit = 0), d = (ef1a..., pp_bit = 1)
BOB: Using point-and-permute. 01 corresponds to entry 1; decrypting entry 1 with ciphertext 0x52d008eddf63ef6a7327028d82b1cbd5
BOB: Successfully decrypted label (ad2d..., pp_bit = 1) for wire f
BOB: Evaluating gate g <- e AND f with input wire labels e = (1f5e..., pp_bit = 1), f = (ad2d..., pp_bit = 1)
BOB: Using point-and-permute. 11 corresponds to entry 3; decrypting entry 3 with ciphertext 0xa6dd033055afb14ea7b3a2966096776c
BOB: Successfully decrypted label (7bf8..., pp_bit = 0) for wire g

Alice reveals the value of the label that Bob computed as the circuit's output:
Alice reveals the label (7bf8..., pp_bit = 0) for output wire g equals: 0

```