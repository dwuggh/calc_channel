import numpy as np


with open('data/expedient_GHZ.npy', 'rb') as f:
    GHZ_expedient = np.load(f)

with open('data/expedient_result_correct.npy', 'rb') as f:
    c_correct1 = np.load(f)

with open('data/expedient_result_error.npy', 'rb') as f:
    c_error1 = np.load(f)

with open('data/stringent_GHZ.npy', 'rb') as f:
    GHZ_stringent = np.load(f)

with open('data/stringent_result_correct.npy', 'rb') as f:
    c_correct2 = np.load(f)
with open('data/stringent_result_error.npy', 'rb') as f:
    c_error2 = np.load(f)

# print(c_correct1[0, 0, 0])
# print(c_error1[0, 0, 0])


def get_probs(arr):
    p_I = arr[0, 0, 0, 0]
    p_X = arr[0, 0, 0, 1] + arr[0, 0, 1, 0] + arr[0, 1, 0, 0] + arr[1, 0, 0, 0]
    p_Y = arr[0, 0, 0, 2] + arr[0, 0, 2, 0] + arr[0, 2, 0, 0] + arr[2, 0, 0, 0]
    p_Z = arr[0, 0, 0, 3] + arr[0, 0, 3, 0] + arr[0, 3, 0, 0] + arr[3, 0, 0, 0]
    p_XX = arr[1, 1, 0, 0] + arr[1, 0, 1, 0] + arr[1, 0, 0, 1] + arr[0, 1, 0, 1] + arr[0, 1, 1, 0] + arr[0, 0, 1, 1]
    p_YY = arr[2, 2, 0, 0] + arr[2, 0, 2, 0] + arr[2, 0, 0, 2] + arr[0, 2, 0, 2] + arr[0, 2, 2, 0] + arr[0, 0, 2, 2]
    p_ZZ = arr[3, 3, 0, 0] + arr[3, 0, 3, 0] + arr[3, 0, 0, 3] + arr[0, 3, 0, 3] + arr[0, 3, 3, 0] + arr[0, 0, 3, 3]
    p_XZ = arr[1, 3, 0, 0] + arr[1, 0, 3, 0] + arr[1, 0, 0, 3] + arr[0, 1, 0, 3] + arr[0, 1, 3, 0] + arr[0, 0, 1, 3] + arr[3, 1, 0, 0] + arr[3, 0, 1, 0] + arr[3, 0, 0, 1] + arr[0, 3, 0, 1] + arr[0, 3, 1, 0] + arr[0, 0, 3, 1]
    p_XY = arr[1, 2, 0, 0] + arr[1, 0, 2, 0] + arr[1, 0, 0, 2] + arr[0, 1, 0, 2] + arr[0, 1, 2, 0] + arr[0, 0, 1, 2] + arr[2, 1, 0, 0] + arr[2, 0, 1, 0] + arr[2, 0, 0, 1] + arr[0, 2, 0, 1] + arr[0, 2, 1, 0] + arr[0, 0, 2, 1]
    p_YZ = arr[2, 3, 0, 0] + arr[2, 0, 3, 0] + arr[2, 0, 0, 3] + arr[0, 2, 0, 3] + arr[0, 2, 3, 0] + arr[0, 0, 2, 3] + arr[3, 2, 0, 0] + arr[3, 0, 2, 0] + arr[3, 0, 0, 2] + arr[0, 3, 0, 2] + arr[0, 3, 2, 0] + arr[0, 0, 3, 2]
    return np.array([p_I, p_X, p_Y, p_Z, p_XX, p_YY, p_ZZ, p_XZ, p_XY, p_YZ])

np.set_printoptions(edgeitems=16, linewidth=200,
                    formatter=dict(float=lambda x: "%6.4g" % x)
                    )


c_correct1_probs = get_probs(c_correct1)
c_error1_probs = get_probs(c_error1)
c_correct2_probs = get_probs(c_correct2)
c_error2_probs = get_probs(c_error2)

print("I  %0.8f %0.8f" % ( c_correct1_probs[0], c_correct2_probs[0] ))
print("X  %0.8f %0.8f" % ( c_correct1_probs[1], c_correct2_probs[1] ))
print("Y  %0.8f %0.8f" % ( c_correct1_probs[2], c_correct2_probs[2] ))
print("Z  %0.8f %0.8f" % ( c_correct1_probs[3], c_correct2_probs[3] ))
print("XX %0.8f %0.8f" % ( c_correct1_probs[4], c_correct2_probs[4] ))
print("YY %0.8f %0.8f" % ( c_correct1_probs[5], c_correct2_probs[5] ))
print("ZZ %0.8f %0.8f" % ( c_correct1_probs[6], c_correct2_probs[6] ))
print("XZ %0.8f %0.8f" % ( c_correct1_probs[7], c_correct2_probs[7] ))
print("XY %0.8f %0.8f" % ( c_correct1_probs[8], c_correct2_probs[8] ))
print("YZ %0.8f %0.8f" % ( c_correct1_probs[9], c_correct2_probs[9] ))

print('\n\n')
print("I  %0.8f %0.8f" % ( c_error1_probs[0], c_error2_probs[0] ))
print("X  %0.8f %0.8f" % ( c_error1_probs[1], c_error2_probs[1] ))
print("Y  %0.8f %0.8f" % ( c_error1_probs[2], c_error2_probs[2] ))
print("Z  %0.8f %0.8f" % ( c_error1_probs[3], c_error2_probs[3] ))
print("XX %0.8f %0.8f" % ( c_error1_probs[4], c_error2_probs[4] ))
print("YY %0.8f %0.8f" % ( c_error1_probs[5], c_error2_probs[5] ))
print("ZZ %0.8f %0.8f" % ( c_error1_probs[6], c_error2_probs[6] ))
print("XZ %0.8f %0.8f" % ( c_error1_probs[7], c_error2_probs[7] ))
print("XY %0.8f %0.8f" % ( c_error1_probs[8], c_error2_probs[8] ))
print("YZ %0.8f %0.8f" % ( c_error1_probs[9], c_error2_probs[9] ))
