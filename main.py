import calc_channel as cc
import numpy as np


ρ = cc.DensityOperator(1, np.array([[1, 0], [0, 0]]))
channel = cc.depolarizing_channel(0.01)
ρ.channel(channel)

cnot = cc.cnot()
x = cc.σ_x()
z = cc.σ_z()

r = cc.multiply(z, cnot)
r = cc.multiply(r, z)
# print(ρ.operator)
print(r.operator)


'''
A: 0, 1, 2
B: 3, 4, 5
C: 6, 7, 8
D: 9, 10, 11
'''


