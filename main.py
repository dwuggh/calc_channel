import calc_channel as cc
import numpy as np
import sys
from bosonic_code import get_bell_pair

def write_coeffs(name, correct, error):
    with open(name + ".txt", 'w') as f:
        for coeff in correct:
            f.write("%.6f " % coeff)
        f.write('\n')
        for coeff in error:
            f.write("%.6f " % coeff)

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

def ph_expedient(p_ph, p_local):
    bell_operator = get_bell_pair(p_ph)
    err_model = cc.ErrorModel(0.1, p_local, p_local)
    ρ = cc.make_bell_with_initial(bell_operator, err_model, False, False)
    ρ = cc.make_GHZ_with(ρ, err_model, False, False)
    result_correct, result_error = cc.get_result(ρ.operator, err_model)
    r1 = result_correct.reshape((1, -1))[0]
    r2 = result_error.reshape((1, -1))[0]
    name = str(p_ph) + str(p_local)
    write_coeffs(name, r1, r2)
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
            name = 'expedient' + str(p)
            ρ = custom(p, False)
        elif argv[1] == 'stringent' or argv[1] == 's':
            print("stringent")
            # ρ = stringent()
            p = float(argv[2]) if len(argv) > 2 else 0.0075
            name = 'stringent' + str(p)
            ρ = custom(p, True)
        elif argv[1] == 'boson-expedient' or argv[1] == 'be':
            p_ph = float(argv[2]) if len(argv) > 2 else 0.005
            p_local = float(argv[3]) if len(argv) > 2 else 0.006
            print("boson(expedient) p_ph: " + str(p_ph) + " p_local: " + str(p_local))
            name = str(p_ph) + str(p_local)
            ρ = ph_expedient(p_ph, p_local)
    else:
        print("custom")
        name = 'custom'
        ρ = custom(0.003, False)

    ρ.print()
    # GHZ_perfect = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    # GHZ_perfect = np.outer(GHZ_perfect, GHZ_perfect) / 2
    # GHZ_perfect = cc.DensityOperator([0, 3, 6, 9], GHZ_perfect)
    
    # print("fidelity of GHZ: ", cc.entanglement_fidelity(ρ, GHZ_perfect))



