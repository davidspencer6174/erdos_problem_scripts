from sympy import primefactors
from math import log
import matplotlib.pyplot as plt

m = 1
k_seq = []
m_seq = []
logm_k_seq = []
for k in range(1, 400):
    while True:
        working = True
        for i in range(m + k, m, -1):  #go from the highest number to the lowest to improve the "skipping ahead"
            if primefactors(i)[-1] <= k:
                working = False
                m = i - 1   #skip ahead since this i will confound us until m reaches i 
                break
        if working:
            k_seq.append(k)
            m_seq.append(m)
            print(k, ': ', m)
            if k > 1:
                logm_k_seq.append(log(m*1.0)/log(k*1.0))
            break
        m += 1

plt.plot(k_seq[1:], logm_k_seq)
plt.title('Erdos 962 empirical growth rate')
plt.xlabel('k')
plt.ylabel('log_k(m)')
plt.savefig('erdos_962_m_vs_k.png')

print(','.join([str(m) for m in m_seq]))