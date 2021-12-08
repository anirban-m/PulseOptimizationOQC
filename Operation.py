from basis_gates import I,X,Y,Z,CX,CZ
import numpy
import re




class Operation:
    '''
    This class takes as input a quantum operation 
    defined on the two qubits as a string
    and then replaces the matrix form of the gates from the basis class
    '''
    def __init__(self,gate_str):
        self._gate_str=gate_str
        self._gate_attr=self._gate_str.split(' ')
        self._gate_name="".join(re.findall("[a-zA-Z]+", self._gate_attr[0]))
        self._gate=eval(self._gate_attr[0].upper()) if self._gate_name in ['X','Y','Z'] else eval(self._gate_attr[0].upper()+'()') 
        self._qubits=eval(self._gate_attr[1])
        Id=I()
        if len(self._qubits)==self._gate.num_qubits:
            if len(self._qubits)==1:
                self.matrix=numpy.kron(self._gate.matrix,Id.matrix) if self._qubits[0]==0 else numpy.kron(Id.matrix,self._gate.matrix)
                self._gate_str=self._gate_str+'|'+Id.__str__()+" [%s]"%1 if self._qubits[0]==0 else Id.__str__()+" [%s]"%0+'|'+self._gate_str
            elif len(self._qubits)==2:
                if self._gate_name=='CX':
                    if self._qubits[0]<self._qubits[1]:
                        self._gate.matrix[[1,2]]=self._gate.matrix[[2,1]]
                        self._gate.matrix[:,[1,2]]=self._gate.matrix[:,[2,1]]
                        self.matrix=self._gate.matrix
                    else:
                        self.matrix=self._gate.matrix
                elif self._gate_name=='CZ':
                    self.matrix=self._gate.matrix
        else:
            raise AttributeError("Gate %s acts on %s qubit, %s given."%(self._gate_name,self._gate.num_qubits,len(self._qubits)))
    
    def __str__(self):
        self.circ_str=self._gate_str
        return self.circ_str
    
            
            