import calc_channel as cc
import numpy as np
import sys


def custom(p, stringent):
    err_model = cc.ErrorModel(0.1, p, p)
    ρ1 = cc.make_bell(err_model, stringent, False)
    # ρ1.print()
    ρ = cc.make_GHZ_with(ρ1, err_model, stringent, False)
    result_correct, result_error = cc.get_result(ρ.operator, err_model)
    with open('data/custom_result.npz', 'wb') as f:
        np.savez(f, result_correct, result_error)
    np.set_printoptions(suppress=True)
    
    r1 = result_correct.reshape((1, -1))[0]
    r2 = result_error.reshape((1, -1))[0]
    print(r1)
    print(r2)
    return ρ
    

def expedient():
    err_model = cc.ErrorModel(0.1, 0.006, 0.006)
    bell_operator = np.array(
        [[0.4978, 0,        0,        0.4962],
         [0,      0.002229, 0.001136, 0],     
         [0,      0.001136, 0.002229, 0],     
         [0.4962, 0,        0,        0.4978]]
        )

    ρ1 = cc.DensityOperator([0, 3], bell_operator)
    # ρ1 = cc.make_bell(err_model, True, False)
    # ρ1.print()
    ρ = cc.make_GHZ_with(ρ1, err_model, False, False)
    return ρ
    
def stringent():
    err_model = cc.ErrorModel(0.1, 0.0075, 0.0075)
    bell_operator = np.array(
        [[0.4972, 0,        0,        0.4953],
         [0,      0.002758, 0.001367, 0],     
         [0,      0.001367, 0.002758, 0],     
         [0.4953, 0,        0,        0.4972]])
    ρ1 = cc.DensityOperator([0, 3], bell_operator)
    ρ1 = cc.make_bell(err_model, True, False)
    ρ1.print()
    ρ = cc.make_GHZ_with(ρ1, err_model, True, False)
    return ρ

if __name__ == "__main__":
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%6.4g" % x)
                        )
    argv = sys.argv
    if len(argv) > 1:
        if argv[1] == 'expedient' or argv[1] == 'e':
            print("expedient")
            # print(argv[2])
            p = float(argv[2]) if len(argv) > 2 else 0.006
            ρ = custom(p, False)
        elif argv[1] == 'stringent' or argv[1] == 's':
            print("stringent")
            # ρ = stringent()
            p = float(argv[2]) if len(argv) > 2 else 0.0075
            ρ = custom(p, True)
    else:
        print("custom")
        ρ = custom(0.003, False)
    ρ.print()
    GHZ_perfect = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    GHZ_perfect = np.outer(GHZ_perfect, GHZ_perfect) / 2
    GHZ_perfect = cc.DensityOperator([0, 3, 6, 9], GHZ_perfect)
    
    # print("fidelity of GHZ: ", cc.entanglement_fidelity(ρ, GHZ_perfect))



