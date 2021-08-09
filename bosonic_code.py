from qutip import *
import numpy as np
import math
def photon_loss_error2(op,kappa):
    tlists=[0.0,1.0]
    H=tensor(qeye(5),qeye(5))
    result=mesolve(H,op,tlists,[np.sqrt(kappa)*tensor(destroy(5),qeye(5))],[])
    op1=result.states[-1]
    return op1
def photon_loss_error1(op,kappa):
    tlists=[0.0,1.0]
    H=qeye(5)
    result=mesolve(H,op,tlists,[np.sqrt(kappa)*destroy(5)],[])
    op1=result.states[-1]
    return op1
def kraus(kappa,l):
    factor=math.pow(1-math.exp(-kappa),l)/math.factorial(l)
    op=math.sqrt(factor)*(-kappa/2*num(5)).expm()*destroy(5)**l
    return op

def get_bell_pair(p, kappa=0.1):
    # p=0.005
    roi1=tensor((basis(5,0)+basis(5,4)).unit(),(basis(5,0)+basis(5,4)).unit())+tensor(basis(5,2),basis(5,2))
    roi1=roi1.unit()
    logical0=(basis(5,0)+basis(5,4)).unit()
    logical1=basis(5,2)
    project=(basis(5,0)+basis(5,4)).unit()*((basis(5,0)+basis(5,4)).unit()).dag()+basis(5,2)*basis(5,2).dag()
    projectA=project
    project=tensor(project,qeye(5))
    epsi=photon_loss_error1(projectA,kappa)
    poi=photon_loss_error2(roi1,kappa)
    E0=(-kappa/2*num(5)).expm()
    E0=tensor(E0,qeye(5))
    optm = Qobj(dims=epsi.dims)
    for i in range(len(epsi.eigenenergies())):
        if np.real(epsi.eigenenergies()[i]) > 1e-6 and np.isnan(epsi.eigenenergies()[i]) == False:
            optm += 1 / np.sqrt(epsi.eigenenergies()[i]) * ket2dm(epsi.eigenstates()[1][i])
    optm = tensor(optm, qeye(5))
    poi1=project*E0.dag()*optm*poi*optm*E0*project
    l=1
    while l<4:
        El=kraus(kappa,l)
        El=tensor(El,qeye(5))
        poi1=poi1+project*El.dag()*optm*poi*optm*El*project
        l=l+1
    X1=tensor(sigmax(),qeye(2))
    Y1=tensor(sigmay(),qeye(2))
    Z1=tensor(sigmaz(),qeye(2))
    X2=tensor(qeye(2),sigmax())
    Y2=tensor(qeye(2),sigmay())
    Z2=tensor(qeye(2),sigmaz())
    A=tensor(basis(2,0)*((basis(5,0)+basis(5,4)).unit()).dag()+basis(2,1)*basis(5,2).dag(),basis(2,0)*((basis(5,0)+basis(5,4)).unit()).dag()+basis(2,1)*basis(5,2).dag())
    poi2=A*poi1*A.dag()
    poi3=(1-3*p)*(1-3*p)*poi2+p*(1-3*p)*(X1*poi2*X1+Y1*poi2*Y1+Z1*poi2*Z1)+p*(1-3*p)*(X2*poi2*X2+Y2*poi2*Y2+Z2*poi2*Z2)+p*p*(X1*X2*poi2*X1*X2+Y1*X2*poi2*Y1*X2+Z1*X2*poi2*Z1*X2+X1*Y2*poi2*X1*Y2+Y1*Y2*poi2*Y1*Y2+Z1*Y2*poi2*Z1*Y2+X1*Z2*poi2*X1*Z2+Y1*Z2*poi2*Y1*Z2+Z1*Z2*poi2*Z1*Z2)
    phi=tensor(basis(2,0),basis(2,0))+tensor(basis(2,1),basis(2,1))
    phi=phi.unit()
    # print(poi3/poi3.tr(),phi.dag()*(poi3/poi3.tr())*phi,poi1.tr())
    ρ = poi3 / poi3.tr()
    print(ρ)
    return np.array(ρ)


if __name__ == '__main__':
    ρ1 = get_bell_pair(0.01)
    print(ρ1)
    
