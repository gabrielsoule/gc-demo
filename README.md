# gc-demo

gc-demo is a demonstrative implementation of garbled circuits, intended to accompany the tutorial found here: (https://www.notion.so/Garbled-Circuits-A-Tutorial-Introduction-b278c5ffe0114921be59de91074016ff). The application simulates the GC protocol between two parties, Alice and Bob, for a circuit specified by the user. The code is well documented and easy to understand, and the structure of the program follows closely the structure of the written tutorial. Each step of the protocol is displayed during execution.  

A number of common GC optimizations are implemented and can be enabled or disabled at will, such as point-and-permute, GRR3, and free-XOR. As of writing (3/4/20), GRR3 has not yet been implemented. More advanced optimizations, such as FleXOR, GRR2, and Half-AND will be added eventually.

## Usage
Run the program from the command line, and follow the prompts to simulate a GC exchange. The command-line flags that can be enabled are:

```
optional arguments:
  -h, --help            show this help message and exit
  -pp POINT_PERMUTE, --point-permute POINT_PERMUTE
                        enable the point-and-permute optimization
  --free-xor FREE_XOR   enable the free-XOR optimization
```

Below is a transcript of a sample session with the point-and-permute optimization enabled.

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
1,1
The remaining input wires, ['c', 'd']  must be supplied by Bob. Please enter a sequence of 0s and 1s corresponding to his input wires, separated by commas.
1,0

Successfully generated the following circuit:
g <- e AND f
├── e <- a AND b
└── f <- c AND d

ALICE: Generating labels for wire a: 0 = (d9d9, pp_bit = 0), 1 = (62e8, pp_bit = 1)
ALICE: Generating labels for wire b: 0 = (2716, pp_bit = 1), 1 = (063d, pp_bit = 0)
ALICE: Garbling gate e <- a AND b
ALICE: Generating labels for wire e: 0 = (3968, pp_bit = 0), 1 = (4922, pp_bit = 1)
    Encrypting label (3968, pp_bit = 0) with (d9d9, pp_bit = 0), (2716, pp_bit = 1), for 0 = 0 AND 0
    Encrypted label: 9622b7bd6b138108e55e0aee7e53ce3bcc4cd0b4a4d21f15f39b7ff3e2165723
    Encrypting label (3968, pp_bit = 0) with (d9d9, pp_bit = 0), (063d, pp_bit = 0), for 0 = 0 AND 1
    Encrypted label: 50bf89c7c98f0b5a3e4de3b0b5604d195eaa410d4bf5fb0f43a6221347c3cc86
    Encrypting label (3968, pp_bit = 0) with (62e8, pp_bit = 1), (2716, pp_bit = 1), for 0 = 1 AND 0
    Encrypted label: 623d0d21a8a49c643e0f039d33eec9960eaffb5d8afe11dc1b05ff757bb83c54
    Encrypting label (4922, pp_bit = 1) with (62e8, pp_bit = 1), (063d, pp_bit = 0), for 1 = 1 AND 1
    Encrypted label: 011bf3cf86fc3ff0f7d64257cbcfb9ca5be1459c67938d78070c992153ea0d22
ALICE: Generating labels for wire c: 0 = (6279, pp_bit = 0), 1 = (f138, pp_bit = 1)
ALICE: Generating labels for wire d: 0 = (06c2, pp_bit = 0), 1 = (85da, pp_bit = 1)
ALICE: Garbling gate f <- c AND d
ALICE: Generating labels for wire f: 0 = (7f2d, pp_bit = 1), 1 = (ed62, pp_bit = 0)
    Encrypting label (7f2d, pp_bit = 1) with (6279, pp_bit = 0), (06c2, pp_bit = 0), for 0 = 0 AND 0
    Encrypted label: 6ca9c44df088b831f9ccd1560eea85acbbd1c9d835f9442626b6f1a1ff21af8a
    Encrypting label (7f2d, pp_bit = 1) with (6279, pp_bit = 0), (85da, pp_bit = 1), for 0 = 0 AND 1
    Encrypted label: 5c51a2e979649c973e54064833ba35f98e428a3f6e985d65a444a5b733fe3055
    Encrypting label (7f2d, pp_bit = 1) with (f138, pp_bit = 1), (06c2, pp_bit = 0), for 0 = 1 AND 0
    Encrypted label: b805d7a8e9c494af902f93ad9055bf45af9025547da629080007aef57c34f17c
    Encrypting label (ed62, pp_bit = 0) with (f138, pp_bit = 1), (85da, pp_bit = 1), for 1 = 1 AND 1
    Encrypted label: ceca127bd8abde25a9e4d6c976e507addd9266c7af0ed08b8bbce7f3cc5e113b
ALICE: Garbling gate g <- e AND f
ALICE: Generating labels for wire g: 0 = (63e2, pp_bit = 0), 1 = (1880, pp_bit = 1)
    Encrypting label (63e2, pp_bit = 0) with (3968, pp_bit = 0), (7f2d, pp_bit = 1), for 0 = 0 AND 0
    Encrypted label: 0e86cc70d1dfdd6e1b9536cb7fdc73aa64b54b1c219327eb46c9fba6ecfae6e2
    Encrypting label (63e2, pp_bit = 0) with (3968, pp_bit = 0), (ed62, pp_bit = 0), for 0 = 0 AND 1
    Encrypted label: 87567e4a2d29935d12663ad67aeb9ac196a39e15a4ddf865ebab94b29a96087b
    Encrypting label (63e2, pp_bit = 0) with (4922, pp_bit = 1), (7f2d, pp_bit = 1), for 0 = 1 AND 0
    Encrypted label: 356d1fbcc7928798be6ff1654f4c0e8196caff880f00173bcb438a60b51826ec
    Encrypting label (1880, pp_bit = 1) with (4922, pp_bit = 1), (ed62, pp_bit = 0), for 1 = 1 AND 1
    Encrypted label: 9081ccb68a394822633899ecc77f2a495c353ad6c94990226a1e0d398bfa4333
ALICE: Shuffling garbled table according to select bits. The final order is:
    00: 87567e4a2d29935d12663ad67aeb9ac196a39e15a4ddf865ebab94b29a96087b
    01: 0e86cc70d1dfdd6e1b9536cb7fdc73aa64b54b1c219327eb46c9fba6ecfae6e2
    10: 9081ccb68a394822633899ecc77f2a495c353ad6c94990226a1e0d398bfa4333
    11: 356d1fbcc7928798be6ff1654f4c0e8196caff880f00173bcb438a60b51826ec
ALICE: Shuffling garbled table according to select bits. The final order is:
    00: 50bf89c7c98f0b5a3e4de3b0b5604d195eaa410d4bf5fb0f43a6221347c3cc86
    01: 9622b7bd6b138108e55e0aee7e53ce3bcc4cd0b4a4d21f15f39b7ff3e2165723
    10: 011bf3cf86fc3ff0f7d64257cbcfb9ca5be1459c67938d78070c992153ea0d22
    11: 623d0d21a8a49c643e0f039d33eec9960eaffb5d8afe11dc1b05ff757bb83c54
ALICE: Shuffling garbled table according to select bits. The final order is:
    00: 6ca9c44df088b831f9ccd1560eea85acbbd1c9d835f9442626b6f1a1ff21af8a
    01: 5c51a2e979649c973e54064833ba35f98e428a3f6e985d65a444a5b733fe3055
    10: b805d7a8e9c494af902f93ad9055bf45af9025547da629080007aef57c34f17c
    11: ceca127bd8abde25a9e4d6c976e507addd9266c7af0ed08b8bbce7f3cc5e113b
OT: Alice, the sender, has messages m0 = (6279, pp_bit = 0) and m1 = (f138, pp_bit = 1). Bob, the receiver wishes to receive message m1.
OT: Alice generates a = 53695, and keeps a secret from Bob
OT: Bob generates b = 59718, and keeps b secret from Alice
OT: Alice transfers A = g^a = 62033 to Bob
OT: Since i = 0, Bob calculates B = Ag^b = 63903 and transfers it to Alice
OT: Bob transfers B to Alice, and computes k = A^b = 42335
OT: Alice computes k0 = B^a = 35603, kl (B/A)^a = 42335
OT: Alice encrypts m0 with key k0 and transfers to Bob c0 = E(k0, m0) = 0x47c89c2ef8571d5c9b1d92d2151863d8
OT: Alice encrypts m1 with key k1 and transfers to Bob c1 = E(k1, m1) = 0xb70655b915cbddfff448bd287f6d33af
OT: Bob successfully decrypts c0 to yield (f138, pp_bit = 1)
OT: Alice, the sender, has messages m0 = (06c2, pp_bit = 0) and m1 = (85da, pp_bit = 1). Bob, the receiver wishes to receive message m0.
OT: Alice generates a = 29113, and keeps a secret from Bob
OT: Bob generates b = 26801, and keeps b secret from Alice
OT: Alice transfers A = g^a = 13041 to Bob
OT: Since i = 0, Bob calculates B = g^b = 708 and transfers it to Alice
OT: Bob transfers B to Alice, and computes k = A^b = 51631
OT: Alice computes k0 = B^a = 51631, kl (B/A)^a = 22276
OT: Alice encrypts m0 with key k0 and transfers to Bob c0 = E(k0, m0) = 0x9d160cda8559a45fc03995d703d5e059
OT: Alice encrypts m1 with key k1 and transfers to Bob c1 = E(k1, m1) = 0x1508e47ea4400245e98f0638903cb315
OT: Bob successfully decrypts c0 to yield (06c2, pp_bit = 0)
BOB: Evaluating gate e <- a AND b with input wire labels a = (62e8, pp_bit = 1), b = (063d, pp_bit = 0)
BOB: Using point-and-permute. 10 = 2; decrypting entry 2 with ciphertext 0x011bf3cf86fc3ff0f7d64257cbcfb9ca5be1459c67938d78070c992153ea0d22
BOB: Successfully decrypted label (4922, pp_bit = 1) for wire e
BOB: Evaluating gate f <- c AND d with input wire labels c = (f138, pp_bit = 1), d = (06c2, pp_bit = 0)
BOB: Using point-and-permute. 10 = 2; decrypting entry 2 with ciphertext 0xb805d7a8e9c494af902f93ad9055bf45af9025547da629080007aef57c34f17c
BOB: Successfully decrypted label (7f2d, pp_bit = 1) for wire f
BOB: Evaluating gate g <- e AND f with input wire labels e = (4922, pp_bit = 1), f = (7f2d, pp_bit = 1)
BOB: Using point-and-permute. 11 = 3; decrypting entry 3 with ciphertext 0x356d1fbcc7928798be6ff1654f4c0e8196caff880f00173bcb438a60b51826ec
BOB: Successfully decrypted label (63e2, pp_bit = 0) for wire g
Alice reveals the label (63e2, pp_bit = 0) for output wire g equals: 0

```