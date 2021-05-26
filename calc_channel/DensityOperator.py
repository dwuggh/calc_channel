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

        super().__init__(qubits, mat)

    def deepcopy(self):
        operator = self.operator.copy()
        qubits = self.qubits.copy()
        return DensityOperator(qubits, operator)

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

    def alter_qubits(self, qubits):
        self.qubits = np.array(qubits)
        
    def evolution(self, unitary: QOperator, p_g = 0, on_qubits = None):

        # ρ = U ρ U^\dagger
        if on_qubits is not None:
            unitary = unitary.alter_qubits(on_qubits)

        result = multiply(unitary, multiply(self, unitary.dagger()))

        self.operator = result.operator
        self.qubits = result.qubits

        if p_g != 0:
            self.channel(depolarizing_channel(p_g, unitary.qubits))
        return result


    # TODO rename this function
    def channel(self, channel: QChannel):
        result = reduce(add, (multiply(multiply(E, self), E.dagger()) for E in channel.kraus_operators))
        self.operator = result.operator
        self.qubits = result.qubits
        return result


    '''
    In the paper, measurement error is modeled by perfect measurement preceded by
    inversion of the state with probability $p_m$.
    '''
    def pre_measure_noise(self, q, pauli, p_m = 0):
        # construct state inversion channel:
        op1 = pauli_0(q)
        op1.operator *= np.sqrt(1 - p_m) 
        op2 = pauli_z(q) if pauli == 'x' else pauli_x(q)
        op2.operator *= np.sqrt(p_m)
        pre_channel = QChannel([op1, op2])
        self.channel(pre_channel)
        
    def bell_measure(self, q1, q2, pauli1, pauli2, p_m = 0, normal_probs = True):
        self.pre_measure_noise(q1, pauli1, p_m)
        self.pre_measure_noise(q2, pauli2, p_m)

        channel1 = measure_x(q1) if pauli1 == 'x' else measure_z(q1)
        channel2 = measure_x(q2) if pauli2 == 'x' else measure_z(q2)

        # the 4 projection operator
        P_00 = multiply(channel1.kraus_operators[0], channel2.kraus_operators[0])
        P_11 = multiply(channel1.kraus_operators[1], channel2.kraus_operators[1])
        
        # the 4 result density matrix, with weight of p_ij
        # ρ_00 = multiply(self, P_00).partial_trace([q1, q2])
        # ρ_11 = multiply(self, P_11).partial_trace([q1, q2])
        ρ_00 = multiply(P_00, multiply(self, P_00)).partial_trace([q1, q2])
        ρ_11 = multiply(P_11, multiply(self, P_11)).partial_trace([q1, q2])

        p_00 = ρ_00.operator.trace()
        p_11 = ρ_11.operator.trace()
        p_sum = p_00 + p_11

        operator = ρ_00.operator + ρ_11.operator
        operator /= p_sum

        self.operator = operator
        self.qubits = ρ_00.qubits
            
    '''
    In the paper, measurement error is modeled by perfect measurement preceded by
    inversion of the state with probability $p_m$.
    NOTE this function may cause porbability loss.
    '''
    def bell_measure_2(self, q1, q2, pauli1, pauli2, p_m = 0, normal_probs = True):
        channel1 = measure_x(q1) if pauli1 == 'x' else measure_z(q1)
        channel2 = measure_x(q2) if pauli2 == 'x' else measure_z(q2)

        # the 4 projection operator
        P_00 = multiply(channel1.kraus_operators[0], channel2.kraus_operators[0])
        P_01 = multiply(channel1.kraus_operators[0], channel2.kraus_operators[1])
        P_10 = multiply(channel1.kraus_operators[1], channel2.kraus_operators[0])
        P_11 = multiply(channel1.kraus_operators[1], channel2.kraus_operators[1])

        # the 4 result density matrix, with weight of p_ij
        # ρ_00 = multiply(self, P_00).partial_trace([q1, q2])
        # ρ_01 = multiply(self, P_01).partial_trace([q1, q2])
        # ρ_10 = multiply(self, P_10).partial_trace([q1, q2])
        # ρ_11 = multiply(self, P_11).partial_trace([q1, q2])

        ρ_00 = multiply(P_00, multiply(self, P_00)).partial_trace([q1, q2])
        ρ_01 = multiply(P_01, multiply(self, P_01)).partial_trace([q1, q2])
        ρ_10 = multiply(P_10, multiply(self, P_10)).partial_trace([q1, q2])
        ρ_11 = multiply(P_11, multiply(self, P_11)).partial_trace([q1, q2])

        p_00 = ρ_00.operator.trace()
        p_01 = ρ_01.operator.trace()
        p_10 = ρ_10.operator.trace()
        p_11 = ρ_11.operator.trace()
        p_sum = p_00 + p_11

        p00 = (1 - p_m) ** 2 * p_00 + p_m ** 2 * p_11
        p01 = p_m * (1 - p_m) * p_sum
        p10 = p_m * (1 - p_m) * p_sum
        p11 = (1 - p_m) ** 2 * p_11 + p_m ** 2 * p_00

        # substitute ρ_00s probability
        f = lambda x, y: 0 if y == 0 else x / y
        p00 = f(p00, p_00)
        p01 = f(p01, p_01)
        p10 = f(p10, p_10)
        p11 = f(p11, p_11)

        if normal_probs:
            p00 = p00 / p_sum
            p01 = p01 / p_sum
            p10 = p10 / p_sum
            p11 = p11 / p_sum


        operator = ρ_00.operator * p00 + ρ_01.operator * p01 + ρ_10.operator * p10 +ρ_11.operator * p11

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
def bell_pair(p_n, qubits = [0, 1], i = 0):
    ρ_00 = np.array([
        [1, 0, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 0, 0, 1]], dtype=np.float64) / 2
    ρ_11 = np.array([
        [1, 0, 0, -1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-1, 0, 0, 1]], dtype=np.float64) / 2
    ρ_0 =  ρ_00 if i == 0 else ρ_11
    mat = (1 - 4 / 3 * p_n) * ρ_0 + (p_n / 3) * np.identity(4)
    # mat = np.array([
    #     [0.44976515, 0,          0,          0.41063044],
    #     [0,          0.05022543, 0.0085779,  0],         
    #     [0,          0.085779,   0.05022543, 0],         
    #     [0.41063044, 0,          0,          0.44976515],
    #     ])
    return DensityOperator(qubits, mat)
