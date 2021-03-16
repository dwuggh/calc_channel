from .QOperator import *
from .DensityOperator import *


def entanglement_fidelity(ρ1: DensityOperator, ρ2: DensityOperator):
    return np.matmul(ρ1.operator, ρ2.operator).trace()

def bell_fidelity(ρ: DensityOperator):
    perfect_bell = bell_pair(0, [0, 1])
    return entanglement_fidelity(perfect_bell, ρ)
