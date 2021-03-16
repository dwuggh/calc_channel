import numpy as np
from .utils import *

class QOperator(object):
    def __init__(self, qubits, operator: np.ndarray):
        self.qubits = np.array(qubits)
        self.operator = np.array(operator, dtype=np.float64)

    def qnum(self):
        return self.qubits.size

    def qmax(self):
        return np.max(self.qubits) + 1

    def dim(self):
        # the following should be equivalent:
        # return 2 ** self.qubits.size
        return self.operator.shape[0]
    
    def print(self):
        print("qubits: ", self.qubits)
        print("shape:  ", self.operator.shape)
        print(self.operator)

    def alter_qubits(self, qubits):
        qubits = np.array(qubits)
        return QOperator(qubits, self.operator)

    # scale this operator by a scalar.
    def scale_to(self, scalar):
        operator = self.operator * scalar
        return QOperator(self.qubits, operator)

    # construct gate in the big hilbert space
    # G = I ⊗ G
    def broadcast(self, qnum: int):
        dim = 2 ** qnum
        big_operator = np.zeros((dim, dim), dtype=np.float64)
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

                val = np.float64(id) * self.operator[gi, gj]
                big_operator[i, j] = val
        return big_operator

    def broadcast_with(self, qubits):
        # qubits_new = np.fromiter((x for x in qubits if not contains(self.qubits, x)), dtype=np.int32)
        qnum = len(qubits)
        dim = 2 ** qnum
        big_operator = np.zeros((dim, dim), dtype=np.float64)

        # occupied qubits of the original operator
        # we need to respect the order of self.qubits in `qubits`

        # occupy1: original qubits in parameter's order
        # occupy1 = []
        # for i, q in enumerate(qubits):
        #     if contains(self.qubits, q):
        #         occupy1.append(q)

        # occupy: original qubits index in `self.qubits` of occupy1
        occupy = []
        for q1 in self.qubits:
            for i, q2 in enumerate(qubits):
                if q1 == q2:
                    occupy.append(i)
                    break

        # self.qubits = np.array(qubits)
        for i in range(dim):
            for j in range(dim):
                di = np.flip(get_bin_digits(i, qnum))
                dj = np.flip(get_bin_digits(j, qnum))

                # coordinates in the small Hilbert space
                gi = from_bin_digits(np.flip(di[occupy]))
                gj = from_bin_digits(np.flip(dj[occupy]))

                # check for identity
                id = 1
                for k in range(len(di)):
                    if id == 1 and not contains(occupy, k) and di[k] != dj[k]:
                        id = 0

                val = np.float64(id) * self.operator[gi, gj]
                big_operator[i, j] = val
        return QOperator(qubits, big_operator)
    # def rearrange(self, qubits_new):
    #     pass

    # get adjoint operator
    def dagger(self):
        t = self.operator.transpose()
        # NOTE only need to transpose since σ_y is also real in our definition.
        # t = t.conj()
        return QOperator(self.qubits, t)

    def partial_trace(self, traced_qubits):
        dim = self.dim()
        qnum = self.qnum()

        qubits_reserved = np.fromiter((x for x in self.qubits if not contains(traced_qubits, x)), np.int32)

        dim_new = 2 ** len(qubits_reserved)

        # the traced matrix
        mat_new = np.zeros((dim_new, dim_new), dtype=np.float64)

        # occupied qubits of the original operator
        occupy_traced = []
        occupy_reserved = []
        for i, q in enumerate(self.qubits):
            if contains(qubits_reserved, q):
                occupy_reserved.append(i)
            if contains(traced_qubits, q):
                occupy_traced.append(i)

        for i in range(dim):
            for j in range(dim):
                di = np.flip(get_bin_digits(i, qnum))
                dj = np.flip(get_bin_digits(j, qnum))
                
                tr_i = from_bin_digits(np.flip(di[occupy_traced]))
                tr_j = from_bin_digits(np.flip(dj[occupy_traced]))

                i_new = from_bin_digits(np.flip(di[occupy_reserved]))
                j_new = from_bin_digits(np.flip(dj[occupy_reserved]))
                if tr_i == tr_j:
                    # print(i, j, i_new, j_new)
                    mat_new[i_new, j_new] += self.operator[i, j]
        return QOperator(qubits_reserved, mat_new)


# multiply 2 QOperators, often needs to broadcast them
def multiply(lhs: QOperator, rhs: QOperator):
    q1 = lhs.qubits
    q2 = rhs.qubits
    qubits = merge(q1, q2)
    # print(q1, q2, qubits)
    lhs_big = lhs.broadcast_with(qubits)
    # print("lhs", lhs.operator.trace())
    rhs_big = rhs.broadcast_with(qubits)
    # print("rhs", rhs.operator.trace())
    result_mat = np.matmul(lhs_big.operator, rhs_big.operator)
    # print("result", result_mat.trace())
    return QOperator(qubits, result_mat)

def add(lhs: QOperator, rhs: QOperator):
    q1 = lhs.qubits
    q2 = rhs.qubits
    qubits = merge(q1, q2)
    lhs_big = lhs.broadcast_with(qubits)
    rhs_big = rhs.broadcast_with(qubits)
    result_mat = lhs_big.operator + rhs_big.operator
    return QOperator(qubits, result_mat)

# the identity operator I
def identity(qubits=[0]):
    return QOperator(qubits, np.identity(2 ** len(qubits)))

def pauli_0(q=0):
    return QOperator([q], np.identity(2))

# pauli's σ operators
def pauli_x(q = 0):
    return QOperator([q], np.array([[0, 1], [1, 0]]))

# NOTE Since channels has the form of Kraus operator, global phase can be safely ignored.
def pauli_y(q = 0):
    return QOperator([q], np.array([[0, -1], [1, 0]]))

# this is the self=-adjoint version of σ_y, which we will not use.
def pauli_y_exact(q = 0):
    return QOperator([q], np.array([[0, 0 - 1j], [0 + 1j, 0]]))

def pauli_z(q = 0):
    return QOperator([q], np.array([[1, 0], [0, -1]]))

def hadamard(q = 0):
    return QOperator([q], 2**(-0.5) * np.array([[1, 1], [1, -1]], dtype=np.float64))

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
