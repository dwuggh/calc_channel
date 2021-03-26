import calc_channel as cc
import numpy as np

if __name__ == "__main__":
    # a = test_1()
    # test_3()
    np.set_printoptions(edgeitems=16, linewidth=200,
                        formatter=dict(float=lambda x: "%6.4g" % x)
                        )
    err_model = cc.ErrorModel(0.1, 0.006, 0.006)
    stringent = False
    bell = cc.make_bell(err_model, stringent, False, True)
    bell_2 = bell.deepcopy()
    bell_2.alter_qubits([6, 9])
    bell.merge(bell_2)
    cc.bell_purify_2(bell, err_model, 0, 6, 1, 2, 7, 8, 'z', stringent)
    cc.bell_purify_2(bell, err_model, 3, 9, 1, 2, 7, 8, 'z', stringent)
    bell.print()
