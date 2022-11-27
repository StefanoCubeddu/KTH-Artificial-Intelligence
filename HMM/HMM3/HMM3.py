
import math
import sys

with open("hmm4_03.txt", 'r') as fobj:
    lines = [[float(num) for num in line.split()] for line in fobj]

observations=lines[3][1:]
A=[]
B=[]
pi=[]

for j in range(len(lines)):
    for i in range(len(lines[j])):
          if(j==0):
                A.append(float(lines[j][i]))
          if(j==1):
                B.append(float(lines[j][i]))
          if(j==2):
                pi.append(float(lines[j][i]))

def createMatrix(rowCount, colCount, dataList):
    mat = []
    x=0
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            # you need to increment through dataList here, like this:
            rowList.append(dataList[x])
            x+=1
        mat.append(rowList)
    return mat

A=createMatrix(int(A[0]),int(A[1]),A[2:])  
pi=createMatrix(int(pi[0]),int(pi[1]),pi[2:]) 
pi=pi[0]
B=createMatrix(int(B[0]),int(B[1]),B[2:])


def get_obs_prob(B):
    mat=[]
    for j in range(len(B[0])):
        line=[]
        for i in range(len(B)):
            line.append(B[i][j])
        mat.append(line)
    return mat

def first_mult(P,init):
    res=[]
    for x in range(len(P)):
        res.append(P[x]*init[x])
    return res

obs_prob=get_obs_prob(B)

def mult(X,Y):
   result=[]
   for y in range(len(Y[0])):
      value=0
      for x in range(len(X)):
        value+=X[x]*Y[x][y]
      result.append(value)
   return result

def get_alpha(pi,A,B,observations):
    t=0
    alpha_store=[]
    temp=[]
    c0=0
    ct=[]
    cu=0
    val=0
    while(t<len(observations)):
       temp=[] 
       if(t==0):
          for i in range(len(A)):
                val=pi[i]*B[i][int(observations[t])]
                temp.append(val)
                c0+=val
          c0=1/c0
          ct.append(c0)
          for i in range(len(A)):
            temp[i]=c0*temp[i]
          alpha_store.append(temp)
       else:
            cu=0
            for i in range(len(A)):
                val=0
                for j in range(len(A)):
                    val+=alpha_store[t-1][j]*A[j][i]
                val=val*B[i][int(observations[t])]
                temp.append(val)
                cu+=val
            cu=1/cu
            ct.append(cu)
            for i in range(len(A)):
                temp[i]=cu*temp[i]
            alpha_store.append(temp)
       t+=1
    return alpha_store,ct


def get_beta(A,B,observations):
    t=len(observations)-1
    count=0
    beta=[]
    while(t>=0):
        temp=[]
        if(t==len(observations)-1):
            for i in range(len(A)):
                temp.append(c[t])
            count+=1
            t-=1
            beta.append(temp)
        else:
            for i in range(len(A)):
                val=0
                for j in range(len(A)):
                    val=val+A[i][j]*B[j][int(observations[t+1])]*beta[count-1][j]
                val=val*c[t]
                temp.append(val)
            beta.append(temp)
            count+=1
            t-=1
    return beta


def get_gamma(beta,alpha,observations,A,B):
    t=0
    gamma=[]
    gamma_sum=[]
    while(t<(len(observations)-1)):
        temp=[]
        temp_sum=[]
        for i in range(len(A)):
            temp2=[]
            for j in range(len(A)):
                val=0
                val=alpha[t][i]*A[i][j]*B[j][int(observations[t+1])]*beta[t+1][j]
                temp2.append(val)
            temp.append(temp2)
            temp_sum.append(sum(temp2))
        gamma.append(temp)
        gamma_sum.append(temp_sum)
        t+=1
    
    temp=[]
    for i in range(len(A)):
        temp.append(alpha[len(observations)-1][i])
    gamma_sum.append(temp)
    
    return gamma,gamma_sum

def reastimate(A,B,gamma,gamma_sum,observations):
    pi=[]
    t=0
    for i in range(len(A)):
        pi.append(gamma_sum[t][i])

    for i in range(len(A)):
        denom=0
        for t in range(len(observations)-1):
            denom+=gamma_sum[t][i]
        for j in range(len(A)):
            numer=0
            for t in range(len(observations)-1):
                numer+=gamma[t][i][j]
            A[i][j]=numer/denom

    for i in range(len(A)):
        denom=0
        for t in range(len(observations)-1):
            denom+=gamma_sum[t][i]
        for j in range(len(B[0])):
            numer=0
            for t in range(len(observations)-1):
                if(int(observations[t])==j):
                    numer+=gamma_sum[t][i]
            B[i][j]=numer/denom
    return A,B,pi





max_iters=100
iters=0
oldLogProb=float('-inf')

flag=True
while(flag):

    alpha,c=get_alpha(pi,A,B,observations)
    beta=get_beta(A,B,observations)
    beta.reverse()
    gamma,gamma_sum=get_gamma(beta,alpha,observations,A,B)
    A,B,pi=reastimate(A,B,gamma,gamma_sum,observations)
    logProb=0
    iters+=1
    for i in range(len(observations)):
        logProb+=math.log(c[i])
    logProb=-logProb
    iters+=1
    if(iters<max_iters and logProb>oldLogProb):
        oldLogProb=logProb
    else:
        flag=False



def print_AB(A,B):
    string=""
    string2=""
    string+=str(len(A))
    string+=" "
    string+=str(len(A[0]))
    string2+=str(len(B))
    string2+=" "
    string2+=str(len(B[0]))

    for i in range(len(A)):
        for j in range(len(A[0])):
            string+=" "+str(round(A[i][j],6))
    for i in range(len(B)):
        for j in range(len(B[0])):
            string2+=" "+str(round(B[i][j],6))
    print(string)
    print(string2)
    return string,string2
    
print_AB(A,B)
    










            