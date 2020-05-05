def cni(n,i):
    minNI=min(i,n-i)
    n=10
    result=1
    for j in range(0,minNI):
        result=result*(n-j)/(minNI-j)
        return result