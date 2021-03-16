import numpy as np
from functools import reduce
from utils import *
from QOperator import *
from QChannel import *
from DensityOperator import *
from fidelity import *


    
'''
q1, q2, q3, q4 are the 4 ancilla qubits
q2    ---------∎--⊤--M(x)
q1    ---∎--⊤--|--Z--M(x)
data1 ---|--σ--|---------
         |     |
q4    ---|-----∎--⊤--M(x)
q3    ---∎--⊤-----Z--M(x)
data2 ------σ------------
'''
def nickerson_1(ρ: DensityOperator, err_model: ErrorModel, data1, data2, q1, q2, q3 ,q4, pauli):
    ρ1 = bell_pair(err_model.p_n, [q1, q3])
    ρ.merge(ρ1)
    ρ.print()

    # 2 control-pauli gate
    c1 = cpauli(pauli, [q1, data1])
    c2 = cpauli(pauli, [q3, data2])

    ρ.evolution(c1, err_model.p_g)
    ρ.evolution(c2, err_model.p_g)
    ρ.print()

    ρ2 = bell_pair(err_model.p_n, [q2, q4])
    ρ.merge(ρ2)

    c3 = cphase([q2, q1])
    c4 = cphase([q4, q3])

    ρ.evolution(c3, err_model.p_g)
    ρ.evolution(c4, err_model.p_g)

    # measurement
    ρ.bell_measure(q1, q3, 'x', err_model.p_m)
    ρ.bell_measure(q2, q4, 'x', err_model.p_m)
    return ρ


'''
q1, q2, q3, q4 are the 4 ancilla qubits
`stringent_plus` indicates whether the blank-separated region is performed
q2    ------∎--⊤--M(x)--∎--⊤--M(x)----  --∎--⊤--M(x)--  ------
q1    ---∎--|--X--------|--Z-------⊤--  --|--Z--------  --M(x)
data1 ---|--|-----------|----------σ--  --|-----------  ------
         |  |           |                 |
q4    ---|--∎--⊤--M(x)--∎--⊤--M(x)----  --∎--⊤--M(x)--  ------
q3    ---∎-----X-----------Z-------⊤--  -----Z--------  --M(x)
data2 -----------------------------σ--  --------------  ------
'''
def nickerson_2(ρ: DensityOperator, err_model: ErrorModel, data1, data2, q1, q2, q3 ,q4, pauli, stringent_plus = True):

    # for efficiency improvement
    ρ1 = bell_pair(err_model.p_n, [q1, q3])
    ρ2 = bell_pair(err_model.p_n, [q2, q4])

    ρ1.merge(ρ2)

    c1 = cnot([q2, q1])
    c2 = cnot([q4, q3])
    ρ1.evolution(c1, err_model.p_g)
    ρ1.evolution(c2, err_model.p_g)

    ρ1.bell_measure(q2, q4, 'x', err_model.p_m)

    ρ3 = bell_pair(err_model.p_n, [q2, q4])
    ρ1.merge(ρ3)

    c3 = cphase([q2, q1])
    c4 = cphase([q4, q3])
    ρ1.evolution(c3, err_model.p_g)
    ρ1.evolution(c4, err_model.p_g)

    ρ1.bell_measure(q2, q4, 'x', err_model.p_m)

    # now, take ρ into consideration
    ρ.merge(ρ1)

    c5 = cpauli(pauli, [q1, data1])
    c6 = cpauli(pauli, [q3, data2])
    ρ.evolution(c5, err_model.p_g)
    ρ.evolution(c6, err_model.p_g)

    if stringent_plus:
        ρ4 = bell_pair(err_model.p_n, [q2, q4])
        ρ.merge(ρ4)

        c7 = cphase([q2, q1])
        c8 = cphase([q4, q3])
        ρ.evolution(c7, err_model.p_g)
        ρ.evolution(c8, err_model.p_g)

        ρ.bell_measure(q2, q4, 'x', err_model.p_m)
        
        pass

    ρ.bell_measure(q1, q3, 'x', err_model.p_m)

'''
2  5
1  4
0  3
'''
def make_bell(err_model: ErrorModel, stringent = True, stringent_plus = True):
    ρ = bell_pair(err_model.p_n, [0, 3])
    nickerson_1(ρ, err_model, 0, 3, 1, 2, 4, 5, 'z')
    nickerson_1(ρ, err_model, 0, 3, 1, 2, 4, 5, 'x')
    if stringent:
        nickerson_2(ρ, err_model, 0, 3, 1, 2, 4, 5, 'z', stringent_plus)
        nickerson_2(ρ, err_model, 0, 3, 1, 2, 4, 5, 'x', stringent_plus)

    return ρ

def make_GHZ(ρ1: DensityOperator, ρ2: DensityOperator, err_model: ErrorModel, stringent = True, stringent_plus = True):
    pass

def stablizer_measurement(err_model: ErrorModel, stringent = True, stringent_plus = True):
    ρ1 = make_bell(err_model, stringent, stringent_plus)
    ρ2 = make_bell(err_model, stringent, stringent_plus)
    ρ2 = ρ2.alter_qubits([6, 9])
