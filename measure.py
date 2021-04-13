import numpy as np
import calc_channel as cc

GHZ_expedient = [
    [0.4929, 0,         0,         0,         0,         3.397e-39, 0,         0,         0,         0,         0,         0,         0,         0,         0,         0.4687],
    [0,      0.001239,  0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0.0001834, 0],     
    [0,      0,         0.001239,  0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0.0001834, 0,         0],     
    [0,      0,         0,         0.0001014, 0,         0,         0,         0,         0,         0,         0,         0,         2.678e-05, 0,         0,         0],     
    [0,      0,         0,         0,         0.001239,  0,         0,         0,         0,         0,         0,         0.0001834, 0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0.00206,   0,         0,         0,         0,         0.001256,  0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,         5.802e-06, 0,         0,         7.174e-08, 0,         0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,         0,         0.001239,  0.0001834, 0,         0,         0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,         0,         0.0001834, 0.001239,  0,         0,         0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,         7.174e-08, 0,         0,         5.802e-06, 0,         0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0.001256,  0,         0,         0,         0,         0.00206,   0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0.0001834, 0,         0,         0,         0,         0,         0,         0.001239,  0,         0,         0,         0],     
    [0,      0,         0,         2.678e-05, 0,         0,         0,         0,         0,         0,         0,         0,         0.0001014, 0,         0,         0],     
    [0,      0,         0.0001834, 0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0.001239,  0,         0],     
    [0,      0.0001834, 0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0.001239,  0],     
    [0.4687, 0,         0,         0,         0,         0,         0,         0,         0,         0,         3.397e-39, 0,         0,         0,         0,         0.4929]
    ]

GHZ_stringent = [
    [0.4907, 0,         0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0,         0.4832],
    [0,      0.0009547, 0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0.000136,  0],     
    [0,      0,         0.0009547, 0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0.000136,  0,         0],     
    [0,      0,         0,         3.485e-05, 0,         0,        0,         0,         0,         0,         0,        0,         3.679e-06, 0,         0,         0],     
    [0,      0,         0,         0,         0.0009547, 0,        0,         0,         0,         0,         0,        0.000136,  0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0.005441, 0,         0,         0,         0,         0.005026, 0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        3.58e-06,  0,         0,         3.826e-08, 0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        0,         0.0009547, 0.000136,  0,         0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        0,         0.000136,  0.0009547, 0,         0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0,        3.826e-08, 0,         0,         3.58e-06,  0,        0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0,         0.005026, 0,         0,         0,         0,         0.005441, 0,         0,         0,         0,         0],     
    [0,      0,         0,         0,         0.000136,  0,        0,         0,         0,         0,         0,        0.0009547, 0,         0,         0,         0],     
    [0,      0,         0,         3.679e-06, 0,         0,        0,         0,         0,         0,         0,        0,         3.485e-05, 0,         0,         0],     
    [0,      0,         0.000136,  0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0.0009547, 0,         0],     
    [0,      0.000136,  0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0.0009547, 0],     
    [0.4832, 0,         0,         0,         0,         0,        0,         0,         0,         0,         0,        0,         0,         0,         0,         0.4907],
    ]


GHZ_expedient = np.array(GHZ_expedient)
GHZ_stringent = np.array(GHZ_stringent)
dim = GHZ_expedient.shape[0]

p_even = 0
p_odd = 0
for i in range(dim):
    a = GHZ_expedient[i][i]
    b = GHZ_expedient[i][dim - i - 1]
    # in basis of (|00> + |11>) and (|00> - |11>)
    p_even += (a + b) / 2
    p_odd += (a - b) / 2

ps = [p_even, p_odd]
p = ps[0]
# p = 0.5
# ps = [p, 1 - p]
# print("p_even, p_odd:", p_even, p_odd)

def get_GHZ_probs(mat):
    probs = []
    dim = mat.shape[0]
    for i in range(dim // 2):
        a = mat[i, i]
        b = mat[i, dim - i - 1]
        p1 = a + b
        p2 = a - b
        probs.append((p1, p2))
    return np.array(probs)


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

'''
@param p1 : probs of state X^j |Ψ>
@param p2 : probs of state X^j Z |Ψ>
'''
def get_pair_result_1(err_model: cc.ErrorModel, p1, p2, qubits_number = 0):
    c_correct = np.zeros((4, 4, 4, 4))
    c_error = np.zeros((4, 4, 4, 4))
    # probs = 0
    p_g = err_model.p_g
    qubits = np.flip(cc.get_bin_digits(qubits_number, 4))

    pm_correct, pm_error = measure_GHZ(err_model.p_m)

    # data_errors denote which error happened on the 4 data qubits
    for i in range(256):
        data_errors = np.flip(cc.get_n_digits(i, 4, 4))
        pgs_correct, pgs_error = get_p(data_errors, p_g)
        for j, q in enumerate(qubits):
            if q == 1:
                if data_errors[j] == 0:
                    data_errors[j] = 1
                elif data_errors[j] == 1:
                    data_errors[j] = 0
                elif data_errors[j] == 2:
                    data_errors[j] = 3
                elif data_errors[j] == 3:
                    data_errors[j] = 2


        p_1 = pgs_correct[0] * pgs_error[3] + pgs_correct[3] * pgs_error[0]
        p_2 = pgs_correct[1] * pgs_error[2] + pgs_correct[2] * pgs_error[1]
        p_3 = pgs_correct[1] * pgs_correct[2] + pgs_error[1] * pgs_error[2]
        p_4 = pgs_correct[0] * pgs_correct[3] + pgs_error[0] * pgs_error[3]
        
        pg_correct = p_1 * p_2 + p_3 * p_4
        pg_error = p_1 * p_3 + p_2 * p_4

        p_correct = p1 * (pg_correct * pm_correct + pg_error * pm_error) + p2 * (pg_correct * pm_error + pg_error * pm_correct)
        p_error = p1 * (pg_correct * pm_error + pg_error * pm_correct) + p2 * (pg_correct * pm_correct + pg_error * pm_error)

        c_correct[data_errors[0], data_errors[1], data_errors[2], data_errors[3]] += p_correct
        c_error[data_errors[0], data_errors[1], data_errors[2], data_errors[3]] += p_error

    return c_correct, c_error



def measure_GHZ(p_m):
    pm_correct = p_m ** 4 + (1 - p_m) ** 4 + 6 * p_m ** 2 * (1 - p_m) ** 2
    pm_error = 4 * p_m * (1 - p_m) ** 3 + 4 * p_m ** 3 * (1 - p_m)
    return pm_correct, pm_error


def get_result(mat, err_model: cc.ErrorModel):
    
    probs = get_GHZ_probs(mat)
    # print(probs)
    c_correct = np.zeros((4, 4, 4, 4))
    c_error = np.zeros((4, 4, 4, 4))
    for (i, ps) in enumerate(probs):
        _c_correct, _c_error = get_pair_result_1(err_model, ps[0], ps[1], i)
        c_correct += _c_correct
        c_error += _c_error
    return c_correct, c_error

# _pair_result_1(cc.ErrorModel(0.1, 0.0075, 0.0075), p)air_result_1(cc.ErrorModel(0.1, 0.0075, 0.0075), p)
# p = 0.9535
# c_correct, c_error = get_pair_result_1(cc.ErrorModel(0.1, 0.0075, 0.0075), p)
c_correct1, c_error1 = get_result(GHZ_expedient, cc.ErrorModel(0.1, 0.006, 0.006))
print(c_correct1[0, 0, 0])
# print(c_error1[0, 0, 0])
c_correct2, c_error2 = get_result(GHZ_stringent, cc.ErrorModel(0.1, 0.0075, 0.0075))
print(c_correct2[0, 0, 0])
# print(c_error2[0, 0, 0])
# print(c_odd)

with open('data/expedient_GHZ.npy', 'wb') as f:
    np.save(f, GHZ_expedient, False)

with open('data/expedient_result_correct.npy', 'wb') as f:
    np.save(f, c_correct1, False)

with open('data/expedient_result_error.npy', 'wb') as f:
    np.save(f, c_error1, False)

with open('data/stringent_GHZ.npy', 'wb') as f:
    np.save(f, GHZ_stringent, False)

with open('data/stringent_result_correct.npy', 'wb') as f:
    np.save(f, c_correct2, False)
with open('data/stringent_result_error.npy', 'wb') as f:
    np.save(f, c_error2, False)
