import numpy as np
import calc_channel as cc

GHZ = [
    [0.4812, 0,         0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0,         0.4596],
    [0,      0.006503,  0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0.0004135, 0],     
    [0,      0,         0.0008917, 0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0.0004135, 0,         0],     
    [0,      0,         0,         0.0001813, 0,         0,        0,         0,         0,         0,         0,        0,         3.433e-05, 0,         0,         0],     
    [0,      0,         0,         0,         0.001899,  0,        0,         0,         0,         0,         0,        0.0005545, 0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0.00805,  0,         0,         0,         0,         0.006679, 0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        5.584e-05, 0,         0,         4.989e-07, 0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        0,         0.001171,  0.0005545, 0,         0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        0,         0.0005545, 0.001171,  0,         0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        4.989e-07, 0,         0,         5.584e-05, 0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0.006679, 0,         0,         0,         0,         0.00805,  0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0.0005545, 0,        0,         0,         0,         0,         0,        0.001899,  0,         0,         0,         0],     
    [0,      0,         0,         3.433e-05, 0,         0,        0,         0,         0,         0,         0,        0,         0.0001813, 0,         0,         0],     
    [0,      0,         0.0004135, 0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0.0008917, 0,         0],     
    [0,      0.0004135, 0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0.006503,  0],     
    [0.4596, 0,         0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0,         0.4812],
]
# 0.940876

GHZ = [
    [0.4864,   0,         0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0,         0.4406],
    [0,        0.004329,  0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0.0003899, 0],     
    [0,        0,         0.0008959, 0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0.0003899, 0,         0],     
    [0,        0,         0,         0.00034,   0,         0,        0,         0,         0,         0,         0,        0,         0.0001047, 0,         0,         0],     
    [0,        0,         0,         0,         0.001844,  0,        0,         0,         0,         0,         0,        0.0007361, 0,         0,         0,         0],     
    [0,        0,         0,         0,         0,         0.004601, 0,         0,         0,         0,         0.00274,  0,         0,         0,         0,         0],     
    [0,        0,         0,         0,         0,         0,        5.125e-05, 0,         0,         6.513e-07, 0,        0,         0,         0,         0,         0],     
    [0,        0,         0,         0,         0,         0,        0,         0.001503,  0.0007361, 0,         0,        0,         0,         0,         0,         0],     
    [0,        0,         0,         0,         0,         0,        0,         0.0007361, 0.001503,  0,         0,        0,         0,         0,         0,         0],     
    [0,        0,         0,         0,         0,         0,        6.513e-07, 0,         0,         5.125e-05, 0,        0,         0,         0,         0,         0],     
    [0,        0,         0,         0,         0,         0.00274,  0,         0,         0,         0,         0.004601, 0,         0,         0,         0,         0],     
    [0,        0,         0,         0,         0.0007361, 0,        0,         0,         0,         0,         0,        0.001844,  0,         0,         0,         0],     
    [0,        0,         0,         0.0001047, 0,         0,        0,         0,         0,         0,         0,        0,         0.00034,   0,         0,         0],     
    [0,        0,         0.0003899, 0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0.0008959, 0,         0],     
    [0,        0.0003899, 0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0.004329,  0],     
    [  0.4406, 0,         0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0,         0.4864],
    ]

GHZ = np.array(GHZ)
dim = GHZ.shape[0]

p_even = 0
p_odd = 0
for i in range(dim):
    a = GHZ[i][i]
    b = GHZ[i][dim - i - 1]
    # in basis of (|00> + |11>) and (|00> - |11>)
    p_even += (a + b) / 2
    p_odd += (a - b) / 2

ps = [p_even, p_odd]
p = ps[0]
# p = 0.5
# ps = [p, 1 - p]
print(p_even, p_odd)


def get_p(indices, p_g):
    result_correct = []
    result_error = []
    for i in indices:
        probs = np.ones(4) * (p_g / 15)
        
        if i == 0:
            probs[0] = 1 - p_g

        result_correct.append(probs[0] + probs[1])
        result_error.append(probs[2] + probs[3])

    return result_correct, result_error

def get_final_result(err_model: cc.ErrorModel, p):
    c_correct = np.zeros((4, 4, 4, 4))
    c_error = np.zeros((4, 4, 4, 4))
    probs = 0
    p_g = err_model.p_g

    pm_correct, pm_error = measure_GHZ(err_model.p_m)

    # channel for data qubit
    for i in range(256):
        dsi = cc.get_n_digits(i, 4, 4)
        pgs_correct, pgs_error = get_p(dsi, p_g)


        _p1 = pgs_correct[2] * pgs_correct[3] + pgs_error[2] * pgs_error[3]
        _p2 = pgs_correct[2] * pgs_error[3] + pgs_error[2] * pgs_correct[3]
        pg_correct = pgs_correct[0] * (pgs_correct[1] * _p1 + pgs_error[1] * _p2) + pgs_error[0] * (pgs_correct[1] * _p2 + pgs_error[1] * _p1)
        pg_error = pgs_correct[0] * (pgs_error[1] * _p1 + pgs_correct[1] * _p2) + pgs_error[0] * (pgs_error[1] * _p2 + pgs_correct[1] * _p1)
        

        p_correct = p * (pg_correct * pm_correct + pg_error * pm_error) + (1 - p) * (pg_correct * pm_error + pg_error * pm_correct)
        p_error = p * (pg_correct * pm_error + pg_error * pm_correct) + (1 - p) * (pg_correct * pm_correct + pg_error * pm_error)
        c_correct[dsi[0], dsi[1], dsi[2], dsi[3]] = p_correct
        # c_correct[dsi] += p_correct
        c_error[dsi[0], dsi[1], dsi[2], dsi[3]] = p_error
        # c_error[dsi] += p_error
        # channel for GHZ qubit
        # X error does not matter, Z error can flip measurement outcome
        if i == 0:
            print(pg_correct, pg_error)
            print(p_correct, p_error)
            print(dsi)
            # print(c_correct[dsi])



    return c_correct, c_error



def measure_GHZ(p_m):
    pm_correct = p_m ** 4 + (1 - p_m) ** 4 + 6 * p_m ** 2 * (1 - p_m) ** 2
    pm_error = 4 * p_m * (1 - p_m) ** 3 + 4 * p_m ** 3 * (1 - p_m)
    return pm_correct, pm_error

c_correct, c_error = get_final_result(cc.ErrorModel(0.1, 0.006, 0.006), p)
print(c_correct[0, 0, 0])
print(np.sum(c_correct), np.sum(c_error))
# print(c_error[0, 0, 0])
# print(c_odd)
