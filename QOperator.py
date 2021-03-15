import numpy as np
from utils import *

class QOperator(object):
    def __init__(self, qubits, operator: np.ndarray):
        self.qubits = np.array(qubits)
        self.operator = np.array(operator, dtype=np.complex64)

    def qnum(self):
        return self.qubits.size

    def qmax(self):
        return np.max(self.qubits) + 1

    def dim(self):
        # the following should be equivalent:
        # return 2 ** self.qubits.size
        return self.operator.shape[0]

    def alter_qubits(self, qubits):
        self.qubits = np.array(qubits)

    # construct gate in the big hilbert space
    # G = I ⊗ G
    def broadcast(self, qnum: int):
        dim = 2 ** qnum
        big_operator = np.zeros((dim, dim), dtype=np.complex64)
        for i in range(dim):
            for j in range(dim):
                di = np.flip(get_bin_digits(i, qnum))
                dj = np.flip(get_bin_digits(j, qnum))

                # coordinates in the small HIlbert space
                gi = from_bin_digits(np.flip(di[self.qubits]))
                gj = from_bin_digits(np.flip(dj[self.qubits]))

                # check for identity
                id = 1
                for k in range(len(di)):
                    if id == 1 and not contains(self.qubits, k) and di[k] != dj[k]:
                        id = 0

                val = np.complex64(id) * self.operator[gi, gj]
                big_operator[i, j] = val
        return big_operator

    # def rearrange(self, qubits_new):
    #     pass

    # get adjoint operator
    def dagger(self):
        t = self.operator.transpose()
        t = t.conj()
        return QOperator(self.qubits, t)

    def partial_trace(self, traced_qubits):
        dim = self.dim()
        qnum = self.qnum()

        qubits_reserved = np.fromiter((x for x in self.qubits if not contains(traced_qubits, x)), np.int32)

        dim_new = dim - 2 ** len(traced_qubits)
        # for simplicity, we treat scalar as a matrix of dim (1, 1)
        dim_new = dim_new if dim_new > 0 else 1

        # the traced matrix
        mat_new = np.zeros((dim_new, dim_new), dtype=np.complex64)

        for i in range(dim):
            for j in range(dim):
                di = np.flip(get_bin_digits(i, qnum))
                dj = np.flip(get_bin_digits(j, qnum))
                
                tr_i = from_bin_digits(np.flip(di[traced_qubits]))
                tr_j = from_bin_digits(np.flip(dj[traced_qubits]))

                i_new = from_bin_digits(np.flip(di[qubits_reserved]))
                j_new = from_bin_digits(np.flip(dj[qubits_reserved]))
                if tr_i == tr_j:
                    # print(i, j, i_new, j_new)
                    mat_new[i_new, j_new] += self.operator[i, j]
        return QOperator(qubits_reserved, mat_new)


# multiply 2 QOperators, often needs to broadcast them
def multiply(lhs: QOperator, rhs: QOperator):
    q1 = lhs.qubits
    q2 = rhs.qubits
    qmax = np.max(np.concatenate((q1, q2))) + 1
    lhs_big = lhs.broadcast(qmax)
    rhs_big = rhs.broadcast(qmax)
    result_mat = np.matmul(lhs_big, rhs_big)
    result_qubits = [i for i in range(qmax)]
    return QOperator(result_qubits, result_mat)

def add(lhs: QOperator, rhs: QOperator):
    q1 = lhs.qubits
    q2 = rhs.qubits
    qmax = np.max(np.concatenate((q1, q2))) + 1
    lhs_big = lhs.broadcast(qmax)
    rhs_big = rhs.broadcast(qmax)
    result_mat = lhs_big + rhs_big
    result_qubits = [i for i in range(qmax)]
    return QOperator(result_qubits, result_mat)

# the identity operator I
def identity(qubits=[0]):
    return QOperator(qubits, np.identity(2 ** len(qubits)))

def pauli_0(q=0):
    return QOperator([q], np.identity(2))

# pauli's σ operators
def pauli_x(q = 0):
    return QOperator([q], np.array([[0, 1], [1, 0]]))

def pauli_y(q = 0):
    return QOperator([q], np.array([[0, 0 - 1j], [0 + 1j, 0]]))

def pauli_z(q = 0):
    return QOperator([q], np.array([[1, 0], [0, -1]]))

def hadamard(q = 0):
    return QOperator([q], 2**(-0.5) * np.array([[1, 1], [1, -1]], dtype=np.complex64))

σ_x = pauli_x
σ_y = pauli_y
σ_z = pauli_z


# which pauli operator?
def pauli(i, q = 0):
    if i == 0:
        return pauli_0(q)
    elif i == 1:
        return pauli_x(q)
    elif i == 2:
        return pauli_y(q)
    elif i == 3:
        return pauli_z(q)
    else:
        # should not happen
        return pauli_0(q)
    
σ = pauli

# CNOT gate, 0 as control, 1 as target
def cnot(qubits = [0, 1]):
    return QOperator(qubits, np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        ]))

# C-Z gate
def cphase(qubits = [0, 1]):
    return QOperator(qubits, np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
        ]))

def cpauli(pauli, qubits = [0, 1]):
    if pauli == 'x':
        return cnot(qubits)
    elif pauli == 'z':
        return cphase(qubits)
    else:
        # WARN this should not happen
        return cnot(qubits)
