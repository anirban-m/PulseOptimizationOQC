# PulseOptimizationOQC


The notebook 'circuit_compilation_OQC_test.ipynb' allows the user to test compilation to gate-set {X,Z,XZ} for various random gate sequences.


A set of codes for optimizing one qubit or two qubit pulse sequence.

basis_gates = A collection of classes for 1 and 2 qubit basis gates, gate-set objects = (I,X,Y,Z,CX,CZ)<br>

<br> Operation = Takes a circuit instruction in the form of string and returns its numpy matrix rep. This additional feature has been added for verifying the matrix representation of the complete pulse train, before and after compilation/optimization.<br>

random_two_qubit_circuit_instructions = A class that generates a string of one and two qubit gates from the gate-set.<br>
<br>
random_one_qubit_circuit_instructions = A class that generates a string of one qubit gate from the gate-set.<br>
<br>
circuit = A class that compiles a pulse train of one or two qubit gates to the basis gates (I,X,Z,CX).


