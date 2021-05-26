import numpy as np

with open('data/expedient_result_correct.npy', 'rb') as f:
    c_correct1 = np.load(f)

with open('data/expedient_result_error.npy', 'rb') as f:
    c_error1 = np.load(f)

with open('data/stringent_result_correct.npy', 'rb') as f:
    c_correct2 = np.load(f)
with open('data/stringent_result_error.npy', 'rb') as f:
    c_error2 = np.load(f)

with open('data/custom_result.npz', 'rb') as f:
    data = np.load(f)
    np.set_printoptions(suppress=True)
    c1 = data['arr_0'].reshape((1, -1))[0]
    c2 = data['arr_1'].reshape((1, -1))[0]
    print(c1)
    print(c2)
# cc1 = c_error1.reshape((1, -1))[0]
# print(cc1)
