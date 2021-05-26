from calc_channel.DensityOperator import bell_pair
from calc_channel.purify_circuits import BBPSSW_2, bell_purify_2
from calc_channel.QOperator import multiply
import calc_channel as cc
import numpy as np

'''
A: 0, 1, 2
B: 3, 4, 5
C: 6, 7, 8
D: 9, 10, 11
'''

def test_1():
    err_model = cc.ErrorModel()
    ρ1 = cc.bell_pair(err_model.p_n, [1, 3])
    ρ2 = cc.bell_pair(err_model.p_n, [2, 4])
    # ρ1.print()
    # print(ρ1.operator.trace())
    ρ1.merge(ρ2)
    # ρ1.print()
    print("trace of ρ1", ρ1.operator.trace())
    # ρ1.print()
    c1 =cc.cphase([2, 1])
    c2 =cc.cphase([4, 3])
    ρ1.evolution(c1)
    ρ1.evolution(c2)

    print("trace of ρ1", ρ1.operator.trace())
    ρ1.bell_measure(2, 4, 'z', 'z')
    ρ1.print()
    return ρ1
    
def test_2():
    x = cc.pauli_x(1)
    z = cc.pauli_z(0)

    a = x.broadcast_with([1, 0])
    a = cc.multiply(x, z)
    a.print()
    a = a.broadcast_with([0, 1])
    a.print()

def test_3():
    ρ = cc.bell_pair(0)
    ρ.bell_measure(0, 1, 'x', 'x')
    ρ.print()
    
def test_BBPSSW_2(p_n = 0.1):
    err_model = cc.ErrorModel(p_n)
    # perfect_bell = cc.bell_pair([0, 1])
    perfect_bell = cc.bell_pair(0, [0, 1])
    noise_bell = cc.bell_pair(err_model.p_n, [0, 1])
    ρ = cc.BBPSSW_2(err_model, True)
    # f1 is just 1 - p_n
    f1 = cc.entanglement_fidelity(noise_bell, perfect_bell)
    f2 = cc.entanglement_fidelity(ρ, perfect_bell)
    p_theory = (f1 ** 2 + 2 * f1 * (1 - f1) / 3 + 5 * ((1 - f1) / 3) ** 2)
    f_theory = (f1 ** 2  + ((1 - f1) / 3) ** 2) / p_theory
    print("no purification:    ", f1)

    print("after purification: ", f2)
    print("fidelity in theory: ", f_theory)
    print("success probability in theory: ", p_theory)

def test_BBPSSW(p_n = 0.1):
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%8.4g" % x)
                        )
    err_model = cc.ErrorModel(p_n)
    perfect_bell = cc.BBPSSW_bell_pair([0, 1])
    noise_bell = cc.BBPSSW_bell_pair([0, 1], err_model.p_n)
    ρ = cc.BBPSSW(err_model, True)
    # f1 is just 1 - p_n
    f1 = cc.entanglement_fidelity(noise_bell, perfect_bell)
    f2 = cc.entanglement_fidelity(ρ, perfect_bell)
    p_theory = (f1 ** 2 + 2 * f1 * (1 - f1) / 3 + 5 * ((1 - f1) / 3) ** 2)
    f_theory = (f1 ** 2  + ((1 - f1) / 3) ** 2) / p_theory
    print("no purification:    ", f1)

    print("after purification: ", f2)
    print("fidelity in theory: ", f_theory)
    print("success probability in theory: ", p_theory)

def test_4():
    a = cc.bell_pair(0, [1, 3])
    # a.broadcast_with_self([1, 3, 2, 4])
    # a.print()
    c1 = cc.cnot([2, 1])
    c2 = cc.cnot([4, 3])
    c = multiply(c1, c2).broadcast_with([1, 3, 2, 4])
    # c.print()
    a.evolution(c)
    a.print()

    #     0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
    array = np.array(
        [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],    # 0
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 1
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 2
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],    # 3
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 4
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],    # 5
         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],    # 6
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 7
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 8
         [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],    # 9
         [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],    # 10
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 11
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],    # 12
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 13
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],    # 14
         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],    # 15
         ]
        ) / 2

    print("\n--------------\n")

    print(array)
    

if __name__ == '__main__':
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%8.4g" % x)
                        )
    err_model = cc.ErrorModel(0.1, 0.006, 0.006)
    ρ = cc.bell_pair(err_model.p_n, [0, 3])
    cc.bell_purify_1(ρ, err_model, 0, 3, 1, 2, 4, 5, 'z')
    ρ.print()
