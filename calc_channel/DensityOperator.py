import numpy as np
from functools import reduce
from .utils import *
from .QOperator import *
from .QChannel import *


class DensityOperator(QOperator):

    def __init__(self, qubits, mat = None):
        qnum = np.max(qubits)
        dim = 2 ** qnum
        # qubits = [i for i in range(qnum)]
        # ground state: | 0000...0 >
        # generate ground state density matrix
        if mat is None:
            mat = np.zeros((dim, dim))
            mat[0, 0] = 1
        # the following should be equivalent:
        # ground_state = np.zeros(dim)
        # ground_state[0] = 1
        # mat = np.outer(ground_state, ground_state)
        super().__init__(qubits, mat)

    # def print(self):
    #     print("qubits: ", self.qubits)
    #     print("shape:  ", self.operator.shape)
    #     print(self.operator)

    def merge(self, other):
        op = multiply(self, other)
        self.operator = op.operator
        self.qubits = op.qubits

    def evolution(self, unitary: QOperator, p_g = 0, on_qubits = None):

        # ρ = U ρ U^\dagger
        if on_qubits is not None:
            unitary = unitary.alter_qubits(on_qubits)

        result = multiply(unitary, multiply(self, unitary.dagger()))

        # big_unitary = unitary.broadcast(self.qnum())
        # self.operator = np.matmul(np.matmul(big_unitary, self.operator), big_unitary.transpose())

        self.operator = result.operator
        self.qubits = result.qubits

        if p_g != 0:
            self.channel(depolarizing_channel(p_g, unitary.qubits))
        return result


    # TODO rename this function
    def channel(self, channel: QChannel):
        # qmax = np.max([self.qmax(), channel.qmax])
        # result = sum(map(lambda E: np.matmul(np.matmul(E.operator, self.operator), E.dagger()), channel.kraus_operators))
        result = reduce(add, (multiply(multiply(E, self), E.dagger()) for E in channel.kraus_operators))
        self.operator = result.operator
        self.qubits = result.qubits
        return result

    # bell measurement: only result 00 and 11 will be reserved
    '''
    In the paper, measurement error is modeled by perfect measurement preceded by
    inversion of the state with probability $p_m$.
    '''
    def bell_measure(self, q1, q2, pauli, p_m = 0):
        channel1 = measure_x(q1) if pauli == 'x' else measure_z(q2)
        channel2 = measure_x(q1) if pauli == 'x' else measure_z(q2)
        # the 4 projection operator
        P_00 = multiply(channel1.kraus_operators[0], channel2.kraus_operators[0])
        P_01 = multiply(channel1.kraus_operators[0], channel2.kraus_operators[1])
        P_10 = multiply(channel1.kraus_operators[1], channel2.kraus_operators[0])
        P_11 = multiply(channel1.kraus_operators[1], channel2.kraus_operators[1])

        p1 = (1 - p_m) ** 2 + p_m ** 2
        p2 = 2 * p_m * (1 - p_m)

        p1 = np.sqrt(p1)
        p2 = np.sqrt(p2)

        # this channel will cause probability loss because of post-selection
        loss_channel = QChannel([P_00.scale_to(p1), P_01.scale_to(p2), P_10.scale_to(p2), P_11.scale_to(p1)])
        self.channel(loss_channel)
        operator = self.partial_trace([q1, q2])
        self.operator = operator.operator
        self.qubits = operator.qubits



# measurement channel
# E_0: measurement result 1, E_1: measurement result -1
def measure_x(q = 0):
    E_0 = 0.5 * np.array([[1, 1], [1, 1]], dtype=np.float64)
    E_1 = 0.5 * np.array([[1, -1], [-1, 1]], dtype=np.float64)
    return QChannel([QOperator([q], E_0), QOperator([q], E_1)])

def measure_z(q = 0):
    E_0 = np.array([[1, 0], [0, 0]], dtype=np.float64)
    E_1 = np.array([[0, 0], [0, 1]], dtype=np.float64)
    return QChannel([QOperator([q], E_0), QOperator([q], E_1)])

# generate bell pair in werner form
def bell_pair(p_n, qubits = [0, 1]):
    Φ = np.array([1, 0, 0, 1], dtype=np.float64) / 2 ** 0.5
    mat = (1 - 4 / 3 * p_n) * np.outer(Φ, Φ) + (p_n / 3) * np.identity(4)
    return DensityOperator(qubits, mat)
