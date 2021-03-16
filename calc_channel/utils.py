import numpy as np
# get_bin_digits(6) -> array([0, 1, 1])
# get_bin_digits(6, 5) -> array([0, 1, 1, 0, 0])
def get_bin_digits(num, min_digits = None):
    digits = np.array([], dtype=int)
    while num >= 1:
        digits = np.append(digits, num % 2)
        num = num // 2

    # to satisfy minimum digits
    if min_digits is not None and len(digits) < min_digits:
        digits = np.concatenate((digits, np.zeros(min_digits - len(digits), dtype=int)))
    return digits

def get_n_digits(num, n, min_digits = None):
    digits = np.array([], dtype=int)
    while num >= 1:
        digits = np.append(digits, num % n)
        num = num // n

    # to satisfy minimum digits
    if min_digits is not None and len(digits) < min_digits:
        digits = np.concatenate((digits, np.zeros(min_digits - len(digits), dtype=int)))
    return digits

# [0, 1, 1] -> 6
def from_bin_digits(digits):
    result = 0
    for (i, d) in enumerate(digits):
        result = result + d * 2 ** i
    return result

def from_n_digits(digits, n):
    result = 0
    for (i, d) in enumerate(digits):
        result = result + d * n ** i
    return result

def contains(l, target):
    for item in l:
        if target == item:
            return True
    return False

class ErrorModel(object):
    def __init__(self, p_n = 0, p_g = 0, p_m = 0):
        self.p_n = p_n
        self.p_g = p_g
        self.p_m = p_m


def merge(l1, l2):
    l = []
    for i in l1:
        if not contains(l, i):
            l.append(i)

    for i in l2:
        if not contains(l, i):
            l.append(i)
    
    return np.array(l)
