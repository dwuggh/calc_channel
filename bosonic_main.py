#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import calc_channel as cc
import numpy as np
import sys
from bosonic_code import get_bell_pair

def write_coeffs(name, correct, error):
    with open(name + ".txt", 'w') as f:
        for coeff in correct:
            f.write("%.8f " % coeff)
        f.write('\n')
        for coeff in error:
            f.write("%.8f " % coeff)

def ph_expedient(p_ph, kappa, p_local, name):
    bell_operator = get_bell_pair(p_ph, kappa)
    # the below 0.0 is actually neglected in computing
    bell_constructor = lambda: bell_operator
    err_model = cc.ErrorModel(bell_constructor, p_local, p_local)
    ρ = cc.make_bell_with_initial(bell_operator, err_model, False, False)
    ρ = cc.make_GHZ_with(ρ, err_model, False, False)
    result_correct, result_error = cc.get_result(ρ.operator, err_model)
    r1 = result_correct.reshape((1, -1))[0]
    r2 = result_error.reshape((1, -1))[0]
    write_coeffs(name, r1, r2)
    return ρ

def run(p_local, p_ph):
    name = "bosonic_channels/" + str(p_ph) + '_' + str(p_local)
    print("running " + name + " ...")
    ph_expedient(p_ph, 0.1, p_local, name)
    print("finished " + name)

def run(p_local, p_ph, kappa):
    name = "bosonic_channels/" + str(kappa) + str(p_ph) + '_' + str(p_local)
    print("running " + name + " ...")
    ph_expedient(p_ph, kappa, p_local, name)
    print("finished " + name)

if __name__ == '__main__':
    # for p_ph in np.arange(0.004, 0.0085, 0.0005):
    argv = sys.argv
    p_local = float(argv[1])
    p_ph = float(argv[2])
    kappa = float(argv[3])
    # p_local = 0.003
    # ph_expedient(p_ph, p_local, 'test')
    run_kappa(p_local, p_ph, kappa)
    # for p_ph in np.arange(0.005, 0.015, 0.001):
    #     pass

    # for p_ph in [0.005, 0.006]:
    #     for p_local in np.arange(0.003, 0.006, 0.0005):
    #         name = "bosonic_channels/{:.3f}_{:.4f}".format(p_ph, p_local)
    #         print("running {} ...".format(name))
    #         ph_expedient(p_ph, p_local, name)
    #         print("finished {}".format(name))

