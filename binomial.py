from calc_channel.DensityOperator import DensityOperator
import calc_channel as cc
import numpy as np


def expedient(p = 0.006):
    err_model = cc.ErrorModel(0.1, p, p)jjk

 #    [[0.4915      0      0  0.486]
 # [     0 0.008491 0.007086      0]
 # [     0 0.007086 0.008491      0]
 # [ 0.486      0      0 0.4915]]
# [[0.49150882      0      0 0.48603865]
#  [     0 0.0084911765 0.0070856237      0]
#  [     0 0.0070856237 0.0084911765      0]
#  [0.48603865      0      0 0.49150882]]


    ρ0 = bosonic_bell_pair([0, 3])
    ρ1 = cc.make_bell_with(ρ0, err_model, False, False)
    ρ1.print()
    ρ = cc.make_GHZ_with(ρ1, err_model, False, False)
    return ρ
    
def stringent():
    err_model = cc.ErrorModel(0.1, 0.0075, 0.0075)

    ρ0 = bosonic_bell_pair([0, 3])
    ρ1 = cc.make_bell_with(ρ0, err_model, True, False)
    ρ1.print()
    ρ = cc.make_GHZ_with(ρ1, err_model, True, False)
    return ρ


def bosonic_bell_pair(qubits = [0, 1]):
    mat = np.array([
        [0.44976515, 0,          0,          0.41063044],
        [0,          0.05022543, 0.0085779,  0],         
        [0,          0.085779,   0.05022543, 0],         
        [0.41063044, 0,          0,          0.44976515],
        ])
    return DensityOperator(qubits, mat)

if __name__ == "__main__":
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%6.4g" % x)
                        )
    # ρ = expedient()
    # ρ = stringent()
    GHZ_perfect = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    GHZ_perfect = np.outer(GHZ_perfect, GHZ_perfect) / 2
    GHZ_perfect = cc.DensityOperator([0, 3, 6, 9], GHZ_perfect)

    ps = np.arange(0.002, 0.004, 0.00025)
    results_c = []
    results_e = []
    for p in ps:
        print("running probs ", p)
        error_model = cc.ErrorModel(1, p, p)
        ρ1 = cc.make_bell(error_model, False, False)
        ρ1.print()
        ρ = cc.make_GHZ_with(ρ1, error_model, False, False)
        result_correct, result_error = cc.get_result(ρ.operator, error_model)
        print(cc.entanglement_fidelity(ρ, GHZ_perfect))
        ρ.print()
        results_c.append(result_correct)
        results_e.append(result_error)
        
    for i in range(len(ps)):
        print(ps[i], " : ", results_c[i][0, 0, 0, 0], " ", results_e[i][0, 0, 0, 0])

    
    with open('data/scan_result.npz', 'wb') as f:
        np.savez(f, results_c, results_e)
    # with open('data/expedient_GHZ_full.npy', 'wb') as f:
    #     np.save(f, ρ.operator, False)

    

