import numpy
import sys
numpy.set_printoptions(precision=5,suppress=True)

#Identity Operator 
class I:
    def __init__(self):
        self.num_qubits=1
        self._gate_name='I'
        try:
           self.matrix=numpy.array([[1,0],
                                    [0,1]])
        except:
            print ("\u001b[31mTypeError \u001b[0m: parameter value needed to obtain matrix rep. of %s gate"%(self._gate_name))
    def __str__(self):
        return ("%s"%(self._gate_name))        

#Rotn about X axis
class X:
    
    def __init__(self,theta=None):
        self.num_qubits=1
        self._gate_name='X'
        self.theta=theta
        try:
           self.matrix=numpy.array([[numpy.cos(self.theta), 1j*numpy.sin(self.theta)],
                                    [1j*numpy.sin(self.theta), numpy.cos(self.theta)]])
        except:
            print ("\u001b[31mTypeError \u001b[0m: parameter value needed to obtain matrix rep. of %s gate"%(self._gate_name))
    def __str__(self):
        return ("%s"%(self._gate_name))        

#Rotn about Y axus
class Y:

    def __init__(self,theta=None):
        self.num_qubits=1
        self._gate_name='Y'
        self.theta=theta
        try:
           self.matrix=numpy.array([[numpy.cos(theta), numpy.sin(theta)],
                                    [-numpy.sin(theta), numpy.cos(theta)]])
        except TypeError:
             print ("\u001b[31mTypeError \u001b[0m: parameter value needed to obtain matrix rep. of %s gate"%(self._gate_name))
    def __str__(self):
        return ("%s"%(self._gate_name))
#Rotn about Z axis
class Z:

    def __init__(self,theta=None):
        self.num_qubits=1
        self._gate_name='Z'
        self.theta=theta
        try:
           self.matrix=numpy.array([[numpy.exp(1j*theta), 0 ],
                                    [0, numpy.exp(-1j*theta)]])
        except TypeError:
             print ("\u001b[31mTypeError \u001b[0m: parameter value needed to obtain matrix rep. of %s gate"%(self._gate_name))

    def __str__(self):
        return ("%s"%(self._gate_name))
#CNOT Gate with 0 as control and 1 as target qubit
class CX:
    def __init__(self):
        self.num_qubits=2
        self._gate_name='CX'
        self.matrix=numpy.kron(numpy.array([[1,0],[0,0]]),numpy.array([[1,0],[0,1]]))+numpy.kron(numpy.array([[0,0],[0,1]]),numpy.array([[0,1],[1,0]]))
    def __str__(self):
        
        return ("%s"%(self._gate_name))
#CZ Gate with 0 as control and 1 as target qubit
class CZ:
    def __init__(self):
        self.num_qubits=2
        self._gate_name='CZ'
        self.matrix=numpy.kron(numpy.array([[1,0],[0,0]]),numpy.array([[1,0],[0,1]]))+numpy.kron(numpy.array([[0,0],[0,1]]),numpy.array([[1,0],[0,-1]]))
    def __str__(self):
        """
        This function returns the gate name
        """
        return ("%s"%(self._gate_name))
        
    