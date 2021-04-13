import calc_channel as cc
import numpy as np


def expedient():
    err_model = cc.ErrorModel(0.1, 0.006, 0.006)
    bell_operator = np.array(
        [[0.4947, 0,        0,        0.4899],
         [0,      0.005315, 0.003703, 0],     
         [0,      0.003703,0.005315,  0],     
         [0.4899, 0,        0,        0.4947]])

    ρ1 = cc.DensityOperator([0, 3], bell_operator)
    ρ = cc.make_GHZ_with(ρ1, err_model, False, False)
    return ρ
    
def stringent():
    err_model = cc.ErrorModel(0.1, 0.0075, 0.0075)
    bell_operator = np.array(
        [[0.4972, 0,        0,        0.4953],
         [0,      0.002758, 0.001367, 0],     
         [0,      0.001367, 0.002758, 0],     
         [0.4953, 0,        0,        0.4972]])
    # ρ1 = cc.make_bell(err_model, True, False)
    ρ1 = cc.DensityOperator([0, 3], bell_operator)
    # ρ1.print()
    ρ = cc.make_GHZ_with(ρ1, err_model, True, False)
    return ρ

if __name__ == "__main__":
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%6.4g" % x)
                        )
    ρ = stringent()
    ρ.print()
    GHZ_perfect = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    GHZ_perfect = np.outer(GHZ_perfect, GHZ_perfect) / 2
    GHZ_perfect = cc.DensityOperator([0, 3, 6, 9], GHZ_perfect)
    
    print(cc.entanglement_fidelity(ρ, GHZ_perfect)) # 0.9616 0.973911
    

