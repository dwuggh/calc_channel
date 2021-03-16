import calc_channel as cc
import numpy as np

if __name__ == "__main__":
    # a = test_1()
    # test_3()
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%6.4g" % x)
                        )
    perfect_bell = cc.bell_pair(0, [0, 1])
    err_model = cc.ErrorModel(0.1, 0.005, 0.005)
    noise_bell = cc.bell_pair(err_model.p_n, [0, 1])
    print("no purification:   ", cc.entanglement_fidelity(perfect_bell, noise_bell))

    ρ = cc.make_bell(err_model, False, False)
    print("with purification: ", cc.entanglement_fidelity(perfect_bell, ρ))
