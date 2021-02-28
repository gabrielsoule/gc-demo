import treelib
import queue
import gc

class Circuit:
     
    def __init__(self):
        self.tree = treelib.Tree()
        self.wires = set() # set of all wires; this is for convienience
    
    '''
    Transforms a table of output wires -> gate objects into a binary tree representing the circuit, whose nodes are gates
    In our tree, the root will be the LAST gate in the circuit (whose output wire is the final output)
    treelib wants each node to have a name, identifier, and data object.
    We will use a description of the gate (c <- a OP b) as the name, and the gate's output wire identifier as a 

    In each iteration of the while loop, we process an existing gate node by creating nodes for the (up to) two gates whose
    outputs are the gate's input. 
    '''
    def build(self, output_wire, gates):
        q = queue.Queue()
        q.put(output_wire)
        last_gate = gates[output_wire]
        self.tree.create_node(str(last_gate), output_wire, data=last_gate)
        while not q.empty():
            out = q.get()
            self.wires.add(out)
            parent_gate = gates[out] # the gate whose output wire is on top of the queue
            self.wires.add(parent_gate.in1)
            self.wires.add(parent_gate.in2)

            # if the 6
            if parent_gate.in1 in gates: 
                in1_gate = gates[parent_gate.in1]
                self.tree.create_node(str(in1_gate), in1_gate.out, data=in1_gate, parent=parent_gate.out)
                q.put(in1_gate.out)

            if parent_gate.in2 in gates: 
                in2_gate = gates[parent_gate.in2]
                self.tree.create_node(str(in2_gate), in2_gate.out, data=in2_gate, parent=parent_gate.out)
                q.put(in2_gate.out)

        
