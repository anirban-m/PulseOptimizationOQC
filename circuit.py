from Moment import Moment
import re
import numpy
from basis_gates import I,X,Y,Z,CX,CZ
from Operation import Operation
from Moment import Moment
'''
circuit class for creating 
a collection of quantum gate operations
with scheduling using moments
'''
class circuit:
    def __init__(self,circ_str):
        '''
        instance of the class initializing
        the circuit instruction of a general 
        two qubit circuit
        '''
        
        self.circ_str=circ_str
        self.instruction=self.circ_str.split(';\n')[1:]
        
    def _get_gate_name(self,gate_str):
            '''
            This function gets the name of the quantum operation by 
            pulling the __str__ from the
            class i.e. one of ['X','Y','Z','CX','CZ','I'].
            '''
            gate_attr=gate_str.split(' ')
            gate_name="".join(re.findall("[a-zA-Z]+", gate_attr[0]))
            return gate_name     
        
    def merge_instructions(self,instruc_last,instruc_new):
        gate1_last,gate2_last=instruc_last.split('|')
        gate1_new,gate2_new=instruc_new.split('|')
        
        '''
            This function takes merges two single qubit quantum operations whenever possible:
            CASE-1 (identity id(0) on 0th qubit and G on 1st qubit or vice-versa)
            "id(0)|G(theta)";"R(theta)|id(1)";-->"R(theta)|G(theta)" 
            CASE-2 (identity id(0) on 0th qubit and G on 1st qubit or identity id(0) on 0th qubit and G' on 1st qubit)
            "id(0)|G(theta)";"id(0)|G'(theta)";-->"id|G(theta+theta')" 
            Case-3 Interchange 0 and 1 qubits and reconsider CASE-2
        '''
        
        if ((self._get_gate_name(gate1_last)=='I') and (self._get_gate_name(gate2_new)=='I')):
            
            new_instruction_str1=gate1_new+'|'+gate2_last
            new_instruction_str2=None
            
            
            
        elif ((self._get_gate_name(gate1_new)=='I') and (self._get_gate_name(gate2_last)=='I')):
            
            new_instruction_str1=gate1_last+'|'+gate2_new
            new_instruction_str2=None
            
            
           
            
        elif (((self._get_gate_name(gate1_new)!='I') and (self._get_gate_name(gate1_last)!='I')) and self._get_gate_name(gate1_new)==self._get_gate_name(gate1_last)):
            
            

            gate1_last_angle= eval(gate1_last.split(' ')[0].upper()).theta
            gate1_new_angle= eval(gate1_new.split(' ')[0].upper()).theta
            gate1_last_angle=gate1_last_angle+gate1_new_angle
            gate1_last_mod=self._get_gate_name(gate1_last)+'({:0.07f})'.format(gate1_last_angle)+' '+gate1_last.split(' ')[1]
            new_instruction_str1=gate1_last_mod+'|'+gate2_last
            new_instruction_str2='I [0]'+'|'+gate2_new if self._get_gate_name(gate2_new)!='I' else None
            
            
            
        elif (((self._get_gate_name(gate2_new)!='I') and (self._get_gate_name(gate2_last)!='I')) and self._get_gate_name(gate2_new)==self._get_gate_name(gate2_last)):
            
            gate2_last_angle= eval(gate2_last.split(' ')[0].upper()).theta
            gate2_new_angle= eval(gate2_new.split(' ')[0].upper()).theta
            gate2_last_angle=gate2_last_angle+gate2_new_angle
            gate2_last_mod=self._get_gate_name(gate2_last)+'({:0.07f})'.format(gate2_last_angle)+' '+gate2_last.split(' ')[1] if numpy.abs(gate2_last_angle)>1e-6 else 'I '+gate2_last.split(' ')[1]
            new_instruction_str1=gate1_last+'|'+gate2_last_mod
            new_instruction_str2=gate1_new+'|'+'I [1]' if self._get_gate_name(gate1_new)!='I' else None  
            
        
        
        else:
            new_instruction_str1=instruc_last+""
            new_instruction_str2=instruc_new+""
            
        return new_instruction_str1,new_instruction_str2 
    
    def compile_to_gateset(self,instruction_str,choice):
        
        def find_and_replace(translation_dict,instruction_elem,choice):
            
            def check_and_decompose_gate(gate_str):
                '''One case single qubit gate is Y    
                '''
                gate,qubit=gate_str.split(' ')
                gate_name,param_str=gate.split('(')[0],gate.split('(')[1][:-1]
                
                if gate_name=='Y':
                    translated_gate_str=self.translation_dict[gate_name].split(';')
                    translated_gate_str=[re_configure_str(translated_gate_str[0]+' '+qubit,eval(qubit)[0]), 
                                         re_configure_str(translated_gate_str[1]+'('+param_str+')'+ ' '+qubit,eval(qubit)[0]),
                                         re_configure_str(translated_gate_str[2]+' '+qubit,eval(qubit)[0])]

                else:

                    translated_gate_str=[re_configure_str(gate_str,eval(qubit)[0])]

                return translated_gate_str
            
            def re_configure_str(instruction_qubit,qubit):
                
                if qubit==0:
                    new_instruction=instruction_qubit+'|I [1]'
                else:    
                    new_instruction='I [0]|'+instruction_qubit
                    
                return new_instruction    
            
            if('|' not in instruction_elem):

                if ((choice=='1') and (self._get_gate_name(instruction_elem)=='CZ')):
                    
                    new_instruction_elems=self.translation_dict[instruction_elem].split(';')
                    

                elif ((choice=='2') and (self._get_gate_name(instruction_elem)=='CX')):

                    new_instruction_elems=self.translation_dict[instruction_elem].split(';')
                    

                elif ((choice=='3') and (self._get_gate_name(instruction_elem)=='CZ')):

                    new_instruction_elems=self.translation_dict2[instruction_elem].split(';')
                    
                else:   
                    new_instruction_elems=[instruction_elem]
                    
            else:     
                if choice=='3':
                    instruction_elem_qubit_ops=instruction_elem.split('|')
                    new_instruction_elems=[]
                    for i in range(2):
                        if (self._get_gate_name(instruction_elem_qubit_ops[i])!='I'):
                            translated_gate_str=check_and_decompose_gate(instruction_elem_qubit_ops[i])
                            new_instruction_elems=new_instruction_elems+translated_gate_str
                else: 
                    new_instruction_elems=[instruction_elem]
               
            return new_instruction_elems        
        
        self.basis_gates_dict={'1':['X','Y','Z','CX'],
                               '2':['X','Y','Z','CZ'],
                               '3':['X','Z','CX']}
        self.choice=choice
        self.chosen_basis_gates=self.basis_gates_dict[self.choice]
        self.translation_dict={'Y':'X(0.78539816339);Z;X(-0.78539816339)',
                              'CZ [1,0]':'I [0]|Y(0.78539816339) [1];CX [1,0];I [0]|Y(-0.78539816339) [1]',
                              'CX [1,0]':'I [0]|Y(-0.78539816339) [1];CZ [1,0];I [0]|Y(0.78539816339) [1]',
                              'CZ [0,1]':'Y(0.78539816339) [0]|I [1];CX [0,1];Y(-0.78539816339) [0]|I [1]',
                              'CX [0,1]':'Y(-0.78539816339) [0]|I [1];CZ [0,1];Y(0.78539816339) [0]|I [1]',
                              }
        self.translation_dict2={'CZ [1,0]':'I [0]|X(0.78539816339) [1];I [0]|Z(0.78539816339) [1];I [0]|X(-0.78539816339) [1];CX [1,0];I [0]|X(0.78539816339) [1];I [0]|Z(-0.78539816339) [1];I [0]|X(-0.78539816339) [1]',
                               'CZ [0,1]':'X(0.78539816339) [0]|I [1];Z(0.78539816339) [0]|I [1];X(-0.78539816339) [0]|I [1];CX [0,1];X(0.78539816339) [0]|I [1];Z(-0.78539816339) [0]|I [1];X(-0.78539816339) [0]|I [1]'
                               }
        self.instruction=instruction_str.split(';\n')[1:]
        self.instruction_arr=[]
        for i in range(len(self.instruction)): 
            self.instruction_arr=self.instruction_arr+find_and_replace(self.translation_dict,self.instruction[i],choice)
        self.translated_circ='qubits 2;\n'+';\n'.join(self.instruction_arr)+';\n'
        return self.translated_circ
        
    def circuit_to_moments(self):
        '''
        This function converts the circuit instruction list to time 
        ordered set of operations where multiple operations are simultaneously 
        performed whenever possible
        '''
        
        self.moments_arr=[Moment(self.instruction[0],0).moment]
        self.instruction_arr=[self.instruction[0]]
        for i in range(1,len(self.instruction)):
            empty_exception_str=':' if len(self.moments_arr)==0 else '-1'
            ind=0 if len(self.moments_arr)==0 else 3
            if ((len(self.moments_arr[eval(empty_exception_str)])==ind) and ('|' in self.instruction[i])):
                    Str='|'.join(self.moments_arr[-1][1:])
                    new_instruction_str1,new_instruction_str2=self.merge_instructions(Str,self.instruction[i])
                    self.instruction_arr[-1]=new_instruction_str1
                    self.moments_arr[-1]=Moment(new_instruction_str1,i-1).moment
                    
                    if new_instruction_str2!=None:
                        self.moments_arr.append(Moment(new_instruction_str2,i).moment)
                        self.instruction_arr.append(new_instruction_str2)
            elif (self.instruction[i]==self.moments_arr[-1][1]):
                    self.moments_arr.pop()
                    self.instruction_arr.pop()
            else:
                self.moments_arr.append(Moment(self.instruction[i],i).moment)
                self.instruction_arr.append(self.instruction[i])

        self.moments_str='qubits 2;\n'
        self.instruction_str='qubits 2;\n'
        for i in range(len(self.moments_arr)):
            elems=self.moments_arr[i]
            elems[0]=str(i)   
            self.moments_str=self.moments_str+'|'.join(elems)+';\n'
            self.instruction_str=self.instruction_str+self.instruction_arr[i]+';\n'
        return self.moments_str,self.instruction_str   