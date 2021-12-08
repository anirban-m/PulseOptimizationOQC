import numpy
from Operation import Operation
class random_one_qubit_circuit_instructions:
    '''
    This class creates a random circuit of a user-defined
    depth using the basis gates 
    '''
    
    
    def __init__(self,depth=10):
        basis_gates=['X','Y','Z']#,'cz']
        self.circ_str='qubits 2'
        for i in range(depth):
            gate=basis_gates[numpy.random.randint(len(basis_gates))]
            param=(2*numpy.random.rand(1)[0]-1)*numpy.pi
            qr=0#numpy.random.randint(0,2)
            op_str=gate+'({:0.10f})'.format(param)+' '+'['+str(qr)+']'
            gate_op=Operation(op_str)
            self.gate_str=gate_op.__str__()
            self.circ_str=self.circ_str+';\n'+self.gate_str   