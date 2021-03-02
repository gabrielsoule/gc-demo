# gc-demo

gc-demo is a demonstrative implementation of garbled circuits, intended to accompany the tutorial found here: (https://www.notion.so/Garbled-Circuits-A-Tutorial-Introduction-b278c5ffe0114921be59de91074016ff). The application simulates the GC protocol between two parties, Alice and Bob, for a circuit specified by the user. The code is well documented and easy to understand, and the structure of the program follows closely the structure of the written tutorial. Each step of the protocol is displayed during execution.  

A number of common GC optimizations are implemented and can be enabled or disabled at will, such as point-and-permute, GRR3, and free-XOR. As of writing (3/2/2021), the application is a work in progress, so only P&P has been implemented so far. 

## Usage

Usage is simple. Run the program from the terminal, and follow the prompts. An example session on a very simple input circuit, with all GC optimizations disabled, is given below:

```
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
1,1
The remaining input wires, ['c', 'd']  must be supplied by Bob. Please enter a sequence of 0s and 1s corresponding to his input wires, separated by commas.
0,1

Successfully generated the following circuit: 
g <- e AND f
├── e <- a AND b
└── f <- c AND d

ALICE: Generating labels for wire g: 0 = ce97, 1 = f97b
ALICE: Generating labels for wire e: 0 = 842c, 1 = 942c
ALICE: Generating labels for wire f: 0 = cb9e, 1 = 10af
ALICE: Generating labels for wire a: 0 = bf98, 1 = cca1
ALICE: Generating labels for wire c: 0 = 28b3, 1 = 3f50
ALICE: Generating labels for wire b: 0 = 4853, 1 = 3854
ALICE: Generating labels for wire d: 0 = 1da8, 1 = 4b8c
ALICE: Garbling gate g <- e AND f 
    Encrypting label ce97 with 842c, cb9e, for 0 = 0 AND 0
    Encrypted label: d513346035d15b8a55a7f7a65777dbdb2ecd0a0bd53a93a77be0fd19bcf1fdaf
    Encrypting label ce97 with 842c, 10af, for 0 = 0 AND 1
    Encrypted label: efd88fe926b0a77d3522b89eb5e24e8e5d48f34fb8c575a1f78063dd13585b9c
    Encrypting label ce97 with 942c, cb9e, for 0 = 1 AND 0
    Encrypted label: 0cf08ff3521eb02a2853316d3b0e803b093325e14967a93c2f48ac4d864b55d0
    Encrypting label f97b with 942c, 10af, for 1 = 1 AND 1
    Encrypted label: 030bc5bf7ae7553e84a85ee32be5f57387ac8682293e4e01354eca0310ed727f
ALICE: Garbling gate e <- a AND b 
    Encrypting label 842c with bf98, 4853, for 0 = 0 AND 0
    Encrypted label: 3019d488fe0197f7decf0e4c4b37cbcd2eb827475b12c70f34964f13bffa9380
    Encrypting label 842c with bf98, 3854, for 0 = 0 AND 1
    Encrypted label: bc59d68913d705fa2f200cdfbf758695f26ca396f1b49e58f18e30f090f46d9a
    Encrypting label 842c with cca1, 4853, for 0 = 1 AND 0
    Encrypted label: 7378b30c4d80eb29055ebc3a91ee5e0c150a5ffbbf8d8a759aa6faafe1c79090
    Encrypting label 942c with cca1, 3854, for 1 = 1 AND 1
    Encrypted label: d6b00ce825ce971235677e0b8520a86817ed943663ce663210b99318927051a6
ALICE: Garbling gate f <- c AND d 
    Encrypting label cb9e with 28b3, 1da8, for 0 = 0 AND 0
    Encrypted label: d0ea95341b9e4679a5ac0273d654e184611eb23c776ed0fb7d3b8cb1ad4f599d
    Encrypting label cb9e with 28b3, 4b8c, for 0 = 0 AND 1
    Encrypted label: 4231aaf8fea05d3cc7970cbf782651c65de4021b0547027d9660758d5bd5dd45
    Encrypting label cb9e with 3f50, 1da8, for 0 = 1 AND 0
    Encrypted label: 260e17cc0c02651f48c6c80c86954d38583da38cdfb9c81a61e1295a0f705326
    Encrypting label 10af with 3f50, 4b8c, for 1 = 1 AND 1
    Encrypted label: 9e9aac488fd235b191ad55b218c50137d043b81f6c1835f9be1b8714d0e76881
ALICE: Randomly shuffling garbled table for gate g <- e AND f
ALICE: Randomly shuffling garbled table for gate e <- a AND b
ALICE: Randomly shuffling garbled table for gate f <- c AND d
OT: Alice, the sender, has messages m0 = 28b3 and m1 = 3f50. Bob, the receiver wishes to receive message m0.
OT: Alice generates a = 18838, and keeps a secret from Bob
OT: Bob generates b = 21706, and keeps b secret from Alice
OT: Alice transfers A = g^a = 18711 to Bob
OT: Since i = 0, Bob calculates B = g^b = 37239 and transfers it to Alice
OT: Bob transfers B to Alice, and computes k = A^b = 41118
OT: Alice computes k0 = B^a = 41118, kl (B/A)^a = 57505
OT: Alice encrypts m0 with key k0 and transfers to Bob c0 = E(k0, m0) = 0xf263ad60bca9ace0e8bdebe51266d1e4
OT: Alice encrypts m1 with key k1 and transfers to Bob c1 = E(k1, m1) = 0x3a09e4c4fc1bd304ff18f818c3b512ab
OT: Bob successfully decrypts c0 to yield 28b3
OT: Alice, the sender, has messages m0 = 1da8 and m1 = 4b8c. Bob, the receiver wishes to receive message m1.
OT: Alice generates a = 87, and keeps a secret from Bob
OT: Bob generates b = 63792, and keeps b secret from Alice
OT: Alice transfers A = g^a = 10415 to Bob
OT: Since i = 0, Bob calculates B = Ag^b = 6267 and transfers it to Alice
OT: Bob transfers B to Alice, and computes k = A^b = 8328
OT: Alice computes k0 = B^a = 61260, kl (B/A)^a = 8328
OT: Alice encrypts m0 with key k0 and transfers to Bob c0 = E(k0, m0) = 0xfd9858d0d0a8ae0b4ab27d41ccd39b16
OT: Alice encrypts m1 with key k1 and transfers to Bob c1 = E(k1, m1) = 0x16c535ab28857c2632f2e705588ccad6
OT: Bob successfully decrypts c0 to yield 4b8c
BOB: Evaluating gate e <- a AND b with input wire labels a = cca1, b = 3854
BOB: Failed to decrypt 3019d488fe0197f7decf0e4c4b37cbcd2eb827475b12c70f34964f13bffa9380! Trying next entry...
BOB: Successfully decrypted label 942c for wire e
BOB: Evaluating gate f <- c AND d with input wire labels c = 28b3, d = 4b8c
BOB: Successfully decrypted label cb9e for wire f
BOB: Evaluating gate g <- e AND f with input wire labels e = 942c, f = cb9e
BOB: Failed to decrypt efd88fe926b0a77d3522b89eb5e24e8e5d48f34fb8c575a1f78063dd13585b9c! Trying next entry...
BOB: Failed to decrypt d513346035d15b8a55a7f7a65777dbdb2ecd0a0bd53a93a77be0fd19bcf1fdaf! Trying next entry...
BOB: Successfully decrypted label ce97 for wire g
Alice reveals the label ce97 for output wire g equals: 0
```