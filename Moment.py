class Moment:
    '''
    This class returns the quantum operation 
    on each of the two qubits at a given time
    slice
    '''
    def __init__(self,instruction_str,op_time):
        
        self._instruction_str=instruction_str
        if '|' in self._instruction_str:
            self._gate_1,self._gate_2=instruction_str.split('|')
            self.moment=[str(op_time),self._gate_1,self._gate_2]
        else:
            self.moment=[str(op_time),self._instruction_str]
        