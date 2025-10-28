from sympy import primefactors

m = 1
for k in range(1, 200):
    while True:
        working = True
        for i in range(m + k, m, -1):  #go from the highest number to the lowest to improve the "skipping ahead"
            if primefactors(i)[-1] <= k:
                working = False
                m = i - 1   #skip ahead since this i will confound us until m reaches i 
                break
        if working:
            print(k, ': ', m)
            break
        m += 1