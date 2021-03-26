import numpy as np
from functools import reduce
from .utils import *
from .QOperator import *


class QChannel(object):

    def __init__(self, kraus_operators):
        # array of QOperators
        self.kraus_operators = kraus_operators
        # collection of all qubits
        self.qubits = []
        for op in self.kraus_operators:
            for q in op.qubits:
                if not contains(self.qubits, q):
                    self.qubits.append(q)
        self.qubits = np.array(self.qubits, dtype=np.int32)

        self.qmax = np.max(self.qubits) + 1
        # broadcast every operator
        # for op in self.kraus_operators:
        #     op = op.broadcast(qnum)
        

'''
depolarizing channel for $n$ qubits

$$
ε(ρ) = (1 - p)ρ + \\frac{ρ}{4^n - 1} \\sum (⊗ A_i) ρ (⊗ A_i^\\dagger)
$$
'''
def depolarizing_channel(p, qubits = [0]) -> QChannel:
    operators = []
    qnum = len(qubits)
    dim = 2 ** qnum
    # (1 - p) I ρ I: E_0 = \sqrt{1 - p} I
    E_0 = np.sqrt(1 - p) * np.identity(dim)
    operators.append(QOperator(qubits, E_0))
    # 4 ** qnum - 1 other operators
    for i in range(4 ** qnum):
        # the i = 0 case is just I, which has already been considered above
        if i == 0:
            continue
        indices = np.flip(get_n_digits(i, 4, qnum))
        # qi: a tuple, (q, i)
        ps = map(lambda qi: pauli(qi[1], qi[0]), list(enumerate(indices)))
        op = reduce(multiply, ps)
        op.operator *= np.sqrt(p / (4 ** qnum - 1))
        operators.append(op)
        
    return QChannel(operators)
