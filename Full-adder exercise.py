#!/usr/bin/env python
# coding: utf-8

# # Learning Exercise I-A
# The full adder takes two binary numbers plus an overflow bit, which we will call X, as its input.
# Create a full adder with input data:
# 
# $A=1$, $B=0$, $X=1$
# . 
# 
# The truth table for the full adder is given below.
# 
# |A(input)|B(input)|X(carry input)|S(sum)|C(carry out)|
# |--|--|--|--|--|
# |0|0|0|0|0|
# |0|0|1|1|0|
# |0|1|0|1|0|
# |0|1|1|0|1|
# |1|0|0|1|0|
# |1|0|1|0|1|
# |1|1|0|0|1|
# |1|1|1|1|1|
# 
# Call your quantum register 'q' and classical register 'c'. Assign inputs A, B and X to q[0], q[1] and q[2] respectively, the sum output S to c[0] and carry output C to c[1].

# In[7]:


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import IBMQ, Aer, execute

#define the registers and quantum circuit 
q = QuantumRegister(4)
c = ClassicalRegister(2)
qc = QuantumCircuit(q,c)

A = q[0]
B = q[1]
X = q[2]
S = c[0]
C = c[1]

qc.x(q[0])
qc.x(q[2])
qc.ccx(q[0],q[1],q[3])
qc.cx(q[0],q[1])
qc.ccx(q[1],q[2],q[3])
qc.cx(q[1],q[2])
qc.cx(q[0],q[1])

#sum
qc.measure(q[2], c[0])
#carryout
qc.measure(q[3], c[1])

# execute the circuit by qasm_simulator
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend, shots=1000)
result = job.result()
count =result.get_counts()
print(count)
qc.draw(output='mpl')


# In[8]:


# Check your answer using following code
from qc_grader import grade_ex1a
grade_ex1a(qc)


# In[ ]:


# Submit your answer. You can re-submit at any time.
from qc_grader import submit_ex1a
submit_ex1a(qc)


# In[ ]:




