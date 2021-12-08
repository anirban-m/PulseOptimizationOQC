import numpy
from Operation import Operation
class random_two_qubit_circuit_instructions:
    '''
    This class creates a random circuit of a user-defined
    depth using the basis gates 
    '''
    
    
    def __init__(self,depth=10):
        basis_gates=['X','Y','Z','CX']#,'cz']
        self.circ_str='qubits 2'
        for i in range(depth):
            gate=basis_gates[numpy.random.randint(len(basis_gates))]
            if (gate in ['X','Y','Z']):
                param=(2*numpy.random.rand(1)[0]-1)*numpy.pi
                qr=numpy.random.randint(0,2)
                op_str=gate+'({:0.10f})'.format(param)+' '+'['+str(qr)+']'
                gate_op=Operation(op_str)
                self.gate_str=gate_op.__str__()
            elif (gate in ['CX']):
                choice=numpy.random.randint(0,2)
                ctrl_bit,targ_bit=(0,1) if choice==0 else (1,0)
                op_str=gate+' '+'['+','.join([str(ctrl_bit),str(targ_bit)])+']'
                gate_op=Operation(op_str)
                self.gate_str=gate_op.__str__()
            self.circ_str=self.circ_str+';\n'+self.gate_str   