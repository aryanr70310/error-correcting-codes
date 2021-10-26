def hammingGeneratorMatrix(r):
    n = 2**r-1
    #construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2**(r-i-1))
    for j in range(1,r):
        for k in range(2**j+1,2**(j+1)):
            pi.append(k)

    #construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i+1))

    #construct H'
    H = []
    for i in range(r,n):
        H.append(decimalToVector(pi[i],r))

    #construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n-r):
        GG.append(decimalToVector(2**(n-r-i-1),n-r))

    #apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    #transpose    
    G = [list(i) for i in zip(*G)]

    return G
def lenvec(l):
    i=3
    while True:
        t=(2**i)-i-1
        if t-i>=l:
            break
        i+=1
    return i,t
def decimalToVector(i,l):
    a=[]
    while i!=0:
        a.append(i%2)
        i=int(i/2)
    for j in range(len(a),l):
        a.append(0)
    a.reverse()
    return a
def Vectortodecimal(v):
    j=0
    for i in range(len(v)):
        j+=v[i]*2**(len(v)-i-1)
    return j
def repetitionEncoder(m,n):
    a=[]
    for i in range(len(m)):
        for j in range(n):
            a.append(m[i])
    return a
    #return m*n
def repetitionDecoder(v):
    nz=0
    no=0
    for i in range(len(v)):
        if v[i]==0:
            nz+=1
        else:
            no+=1
    if nz==no:
        return []
    elif nz>no:
        return [0]
    else:
        return [1]
def message(a):
    i=lenvec(len(a))
    b=[]
    l=decimalToVector(len(a),i[0])
    for j in l:
        b.append(j)
    for j in a:
        b.append(j)
    while len(b)!=i[1]:
        b.append(0)
    return b
def hammingEncoder(m):
    i=lenvec(len(m))
    G=hammingGeneratorMatrix(i[0]-1)
    if len(m)!=len(G):
        return []
    b=[]
    t=0
    for j in range(len(G[0])):
        for k in range(len(G)):
            t+=G[k][j]*m[k]
        if t%2==0:
            t=0
        else:
            t=1
        b.append(t)
        t=0
    return b
def hammingDecoder(v):
    x=1
    while True:
        if 2**x>len(v):
            break
        x+=1
    H=[]
    for i in range(1,2**x):
        H.append(decimalToVector(i,x))
    if len(H)!=len(v):
        return []
    for i in range(len(v)-1,-1,-1):
        chk=[]
        e=len(v)*[0]
        if i!=-1:
            e[i]=1
        ve=[]
        carry=0
        for j in range(len(v)-1,-1,-1):
            t = carry
            t+=1 if e[j]==1 else 0
            t+=1 if v[j]==1 else 0
            ve.append(1 if t%2==1 else 0)
            carry=0 if t<2 else 1
        ve.reverse()
        t=0
        for j in range(len(H[0])):
            for k in range(len(ve)):
                t+=ve[k]*H[k][j]
            t=0 if t%2==0 else 1
            chk.append(t)
            if chk==len(H[0])*[0]:
                return ve
    return []
def messageFromCodeword(c):
    G=[]
    for i in range(2,len(c)):
        G=hammingGeneratorMatrix(i)
        if len(G[0])==len(c):
            break
        elif len(G[0])>len(c):
            return []
    for i in range(2**len(G)-1,0,-1):
        v=[]
        m=decimalToVector(i,len(G))
        t=0
        for j in range(len(G[0])):
            for k in range(len(G)):
                t+=G[k][j]*m[k]
            if t%2==0:
                t=0
            else:
                t=1
            if t!=c[j]:
                break
            else:
                v.append(t)
            t=0
        if len(v)==len(c):
            return m
    return []
def dataFromMessage(m):
    i=lenvec(len(m))
    r=i[0]-1
    G=hammingGeneratorMatrix(r)
    if len(m)!=len(G):
        return []
    l=Vectortodecimal(m[0:r])
    if l>len(m[r:]):
        return []
    n=m[r:r+l]
    return n