import numpy as np
from functools import reduce
from .utils import *
from .QOperator import *
from .QChannel import *
from .DensityOperator import *
from .fidelity import *


    
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
def bell_purify_1(ρ: DensityOperator, err_model: ErrorModel, data1, data2, q1, q2, q3 ,q4, pauli):
    ρ1 = bell_pair(err_model.p_n, [q1, q3])
    ρ.merge(ρ1)
    # ρ.print()

    # 2 control-pauli gate
    c1 = cpauli(pauli, [q1, data1])
    c2 = cpauli(pauli, [q3, data2])

    ρ.evolution(c1, err_model.p_g)
    ρ.evolution(c2, err_model.p_g)
    # ρ.print()

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
`stringent` indicates whether the blank-separated region is performed
q2    ------∎--⊤--M(x)--∎--⊤--M(x)----  --∎--⊤--M(x)--  ------
q1    ---∎--|--X--------|--Z-------⊤--  --|--Z--------  --M(x)
data1 ---|--|-----------|----------σ--  --|-----------  ------
         |  |           |                 |
q4    ---|--∎--⊤--M(x)--∎--⊤--M(x)----  --∎--⊤--M(x)--  ------
q3    ---∎-----X-----------Z-------⊤--  -----Z--------  --M(x)
data2 -----------------------------σ--  --------------  ------
'''
def bell_purify_2(ρ: DensityOperator, err_model: ErrorModel, data1, data2, q1, q2, q3 ,q4, pauli, stringent = True):

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

    if stringent:
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
qubit indexing:
2  5
1  4
0  3
'''
def make_bell(err_model: ErrorModel, stringent = True, stringent_plus = True):
    ρ = bell_pair(err_model.p_n, [0, 3])
    bell_purify_1(ρ, err_model, 0, 3, 1, 2, 4, 5, 'z')
    print(bell_fidelity(ρ))
    bell_purify_1(ρ, err_model, 0, 3, 1, 2, 4, 5, 'x')
    print(bell_fidelity(ρ))
    if stringent:
        bell_purify_2(ρ, err_model, 0, 3, 1, 2, 4, 5, 'z', stringent)
        print(bell_fidelity(ρ))
        bell_purify_2(ρ, err_model, 0, 3, 1, 2, 4, 5, 'x', stringent)
        print(bell_fidelity(ρ))

    return ρ

def make_GHZ(ρ1: DensityOperator, ρ2: DensityOperator, err_model: ErrorModel, stringent = True, stringent_plus = True):
    pass

def stablizer_measurement(err_model: ErrorModel, stringent = True, stringent_plus = True):
    ρ1 = make_bell(err_model, stringent, stringent_plus)
    ρ2 = make_bell(err_model, stringent, stringent_plus)
    ρ2 = ρ2.alter_qubits([6, 9])



'''
|0>x|0>z + |1>x|1>z
'''
def BBPSSW_bell_pair(qubits, p_n = 0):
    ρ_0 = np.array([
        [1, 1, 1, -1],
        [1, 1, 1, -1],
        [1, 1, 1, -1],
        [-1, -1, -1, 1]], dtype=np.float64) / 4
    mat = (1 - 4 / 3 * p_n) * ρ_0 + (p_n / 3) * np.identity(4)
    return DensityOperator(qubits, mat)


    
'''
BBPSSW protocol in 1996, Bennett et al.
q2    ------∎--X--M(z)
q1    ---∎--|--⊥------
         |  |          
q4    ---|--∎--⊤--M(x)
q3    ---∎-----X------
'''
def BBPSSW(err_model: ErrorModel, detail = False):
    # ρ1 = bell_pair(err_model.p_n, [1, 3])
    # ρ2 = bell_pair(err_model.p_n, [2, 4])
    ρ1 = BBPSSW_bell_pair([1, 3], err_model.p_n)
    ρ2 = BBPSSW_bell_pair([2, 4], err_model.p_n)
    if detail:
        ρ1.print()

    ρ1.merge(ρ2)
    ρ1.broadcast_with_self([1, 3, 2, 4])
    if detail:
        ρ1.print()

    c1 = cnot([1, 2])
    # c1 = cnot([2, 1])
    c2 = cnot([4, 3])

    c2 = multiply(c1, c2)
    # c2.broadcast_with([1, 3, 2, 4]).print()

    # ρ1.evolution(c1, err_model.p_g)
    ρ1.evolution(c2, err_model.p_g)
    ρ1.broadcast_with_self([1, 3, 2, 4])


    if detail:
        ρ1.print()

    # ρ1.bell_measure(2, 4, 'z')
    probs = ρ1.operator.trace()
    if detail:
        print("probs", probs)
    ρ1.bell_measure(2, 4, 'z', 'x')
    # ρ1 = ρ1.partial_trace([2, 4])
    probs = ρ1.operator.trace()
    ρ1.scale(1 / probs)

    if detail:
        print("probs", probs)
        ρ1.print()

    return ρ1

'''
this circuit does nothing.
q2    ------∎--⊤--M(z)
q1    ---∎--|--X------
         |  |          
q4    ---|--∎--⊤--M(z)
q3    ---∎-----X------
'''
def BBPSSW_2(err_model: ErrorModel, detail = False):
    ρ1 = bell_pair(err_model.p_n, [1, 3])
    ρ2 = bell_pair(err_model.p_n, [2, 4])
    if detail:
        ρ1.print()

    ρ1.merge(ρ2)
    ρ1.broadcast_with_self([1, 3, 2, 4])
    if detail:
        ρ1.print()

    # c1 = cnot([1, 2])
    c1 = cnot([2, 1])
    c2 = cnot([4, 3])

    c2 = multiply(c1, c2)
    c2.broadcast_with([1, 3, 2, 4]).print()

    # ρ1.evolution(c1, err_model.p_g)
    ρ1.evolution(c2, err_model.p_g)
    ρ1.broadcast_with_self([1, 3, 2, 4])


    if detail:
        ρ1.print()

    # ρ1.bell_measure(2, 4, 'z')
    ρ1.bell_measure(2, 4, 'z', 'z')
    # ρ1 = ρ1.partial_trace([2, 4])
    probs = ρ1.operator.trace()
    ρ1.scale(1 / probs)

    if detail:
        print("probs", probs)
        ρ1.print()

    return ρ1
