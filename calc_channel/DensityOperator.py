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

    def scale(self, scalar):
        self.operator = self.operator * scalar

    def broadcast_with_self(self, qubits):
        op = self.broadcast_with(qubits)
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

            
    '''
    In the paper, measurement error is modeled by perfect measurement preceded by
    inversion of the state with probability $p_m$.
    NOTE this function may cause porbability loss.
    '''
    def bell_measure(self, q1, q2, pauli1, pauli2, p_m = 0):
        channel1 = measure_x(q1) if pauli1 == 'x' else measure_z(q1)
        channel2 = measure_x(q2) if pauli2 == 'x' else measure_z(q2)

        # the 4 projection operator
        P_00 = multiply(channel1.kraus_operators[0], channel2.kraus_operators[0])
        P_01 = multiply(channel1.kraus_operators[0], channel2.kraus_operators[1])
        P_10 = multiply(channel1.kraus_operators[1], channel2.kraus_operators[0])
        P_11 = multiply(channel1.kraus_operators[1], channel2.kraus_operators[1])
        # P_00.print()

        # the 4 resulting density matrix, with weight of p_ij
        ρ_00 = multiply(self, P_00).partial_trace([q1, q2])
        ρ_01 = multiply(self, P_01).partial_trace([q1, q2])
        ρ_10 = multiply(self, P_10).partial_trace([q1, q2])
        ρ_11 = multiply(self, P_11).partial_trace([q1, q2])


        p_00 = ρ_00.operator.trace()
        p_01 = ρ_01.operator.trace()
        p_10 = ρ_10.operator.trace()
        p_11 = ρ_11.operator.trace()
        p_sum = p_00 + p_11

        p00 = (1 - p_m) ** 2 * p_00 + p_m ** 2 * p_11
        p01 = p_m * (1 - p_m) * p_sum
        p10 = p_m * (1 - p_m) * p_sum
        p11 = (1 - p_m) ** 2 * p_11 + p_m ** 2 * p_00

        # no rescaling: this is intentional
        # p00 = p00 / p_sum
        # p01 = p01 / p_sum
        # p10 = p10 / p_sum
        # p11 = p11 / p_sum

        print(p_00, p_01, p_10, p_11)
        print(p00 , p01 , p10 , p11)

        operator = ρ_00.operator * p00 + ρ_01.operator * p10 + ρ_10.operator * p10 +ρ_11.operator * p11

        self.operator = operator
        self.qubits = ρ_00.qubits
        



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
    ρ_0 = np.array([
        [1, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 0, 0, 1]], dtype=np.float64) / 2
    mat = (1 - 4 / 3 * p_n) * ρ_0 + (p_n / 3) * np.identity(4)
    return DensityOperator(qubits, mat)
