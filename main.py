from QOperator import pauli
from utils import ErrorModel
import calc_channel as cc
import numpy as np


# ρ = cc.DensityOperator(1, np.array([[1, 0], [0, 0]]))
# channel = cc.depolarizing_channel(0.01)
# ρ.channel(channel)

# cnot = cc.cnot()
# x = cc.σ_x()
# z = cc.σ_z()

# r = cc.multiply(z, cnot)
# r = cc.multiply(r, z)
# # print(ρ.operator)
# print(r.operator)


'''
A: 0, 1, 2
B: 3, 4, 5
C: 6, 7, 8
D: 9, 10, 11
'''



def test_1():
    np.set_printoptions(edgeitems=16, linewidth=200,
                        # formatter=dict(float=lambda x: "%.3g" % x)
                        )
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
    ρ1.bell_measure(2, 4, 'z')
    ρ1.print()
    return ρ1
    
def test_2():
    x = cc.pauli_x(1)
    z = cc.pauli_z(0)

    a = x.broadcast_with([1, 0])
    # x.print()
    # z.print()
    a = cc.multiply(x, z)
    a.print()
    a = a.broadcast_with([0, 1])
    a.print()

def test_3():
    ρ = cc.bell_pair(0)
    ρ.bell_measure(0, 1, 'x')
    ρ.print()
    
if __name__ == "__main__":
    # a = test_1()
    # test_3()
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%5.6g" % x)
                        )
    err_model = cc.ErrorModel(0.1, 0.01)
    ρ = cc.make_bell(err_model, True, False)
    ρ.print()
    # test_2()
