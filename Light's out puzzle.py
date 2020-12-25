#!/usr/bin/env python
# coding: utf-8

# # Learning Exercise II-A
# 
# Let's try to solve a "Lights Out" puzzle using **Grover's algorithm**! The information you learned last week will be helpful in solving this puzzle.
# 
# Answer by creating a quantum circuit to solve the puzzle shown in the figure below. In the quantum circuit to be submitted, measure **only the `solution` (9bit)** that solves the puzzle. 
# To submit your solution, create a function which takes `lights` as an input and then returns a  `QuantumCircuit`.  You can name the function as you like. Make sure it works even with another dataset of "lights". We will validate your circuit with different inputs.
# 
# **In addition, please implement the quantum circuit within 28 qubits.**
# 
# There are several ways to solve it without using Grover's algorithm, but we ask you to **use Grover's algorithm** for this exercise. It should help you in solving other challenges.
# 
# Please note that you can get the answer with the same endian as the one used in the description. You can also use the following function.
# ```python
# qc = qc.reverse_bits()
# ```

# In[3]:


Image('lights_out_prob.png')


# ## Hint
# You’ll need a more complex oracle than the “Week1-B oracle” to solve this problem. The added auxiliary qubits will help you design the oracle part, but they need to be handled with care.  At the end of the oracle part, all auxiliary qubits must be returned to their initial state (this operation is sometimes called Uncomputation). [Week 3 of last year’s IBM Quantum Challenge](https://github.com/quantum-challenge/2019/blob/master/problems/week3/week3_en.ipynb) will support your understanding of this concept. 
# 
# If you are not sure about the optimal number of iterations for Grover's algorithm, solve [this quiz](https://github.com/qiskit-community/IBMQuantumChallenge2020/tree/main/quizzes/quiz_1) and talk to Dr. Ryoko(@ryoko) in the [Qiskit slack](qiskit.slack.com) via direct message. You can get important formulas of the theoretical aspects of week 1-B.

# In[2]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np

# Importing Qiskit
from qiskit import IBMQ, BasicAer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute

# Import basic plot tools
from qiskit.tools.visualization import plot_histogram

backend = BasicAer.get_backend('qasm_simulator')
prob_of_ans = []

def week2a_ans_func(lights):
    ##### build your quantum circuit here

    #####  In addition, please make it a function that can solve the problem even with different inputs (lights). 
    ###We do validation with different inputs.
    # Initialization
    cond = [[0,1,3], [0,1,2,4], [1,2,5], [0,3,4,6],[1,3,4,5,7],[2,4,5,8],[3,6,7],[4,6,7,8],[5,7,8]]

    def light_oracle(qc, light_reg, sol_reg, out_reg, lights):
        qc.barrier()

        for i in range(len(lights)):
            for j in cond[i]:
                qc.cx(sol_reg[i], light_reg[j])

        qc.x(light_reg)
        qc.mct(light_reg, out_reg)
        qc.x(light_reg)

        for j in range(len(lights)):
            for k in cond[j]:
                qc.cx(sol_reg[j], light_reg[k])


        qc.barrier()


    def diffusion(qc, sol_reg):
        qc.h(sol_reg)
        qc.x(sol_reg)
        qc.h(sol_reg[0])
        qc.mct(sol_reg[1:], sol_reg[0])
        qc.h(sol_reg[0])
        qc.x(sol_reg)
        qc.h(sol_reg)
    
    light_register = QuantumRegister(9, name='light')
    sol_register = QuantumRegister(9, name='solution')
    out_register = QuantumRegister(1, name='out')
    cbits = ClassicalRegister(9, name='cbits')

    qc = QuantumCircuit(sol_register, light_register, out_register, cbits)

    qc.x(out_register)
    qc.h(out_register)
    qc.h(sol_register)

    for j in range(len(lights)):
            if lights[j] == 1:
                qc.x(light_register[j])

    iters = 1
    for trial in range(iters):
        light_oracle(qc, light_register, sol_register, out_register, lights)
        diffusion(qc, sol_register)

    qc.measure(sol_register[::-1], cbits)
    
    return qc


# In[44]:


# Submission code
from qc_grader import prepare_ex2a, grade_ex2a, submit_ex2a

# Execute your circuit with following prepare_ex2a() function.
# The prepare_ex2a () function works like the execute() function with only QuantumCircuit as an argument.
job = prepare_ex2a(week2a_ans_func)

result = job.result()
count = result.get_counts()
original_problem_set_counts = count[0]

original_problem_set_counts
# The bit string with the highest number of observations is treated as the solution.


# In[45]:


# Check your answer by executing following code.
# The quantum cost of the QuantumCircuit is obtained as the score. The quantum cost is related to rank only in the third week.
grade_ex2a(job)


# In[46]:


# Submit your results by executing following code. You can submit as many times as you like during the period. 
submit_ex2a(job)


# In[ ]:




