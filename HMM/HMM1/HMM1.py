with open("hmm2_01.txt", 'r') as fobj:
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


i=0
alpha=[]
alpha_store=[]
while(i<len(observations)):
    if(i==0):
        alpha=first_mult(pi,obs_prob[int(observations[i])])
        alpha_store.append(alpha)
    else:  
        alpha=(first_mult(mult(alpha,A),obs_prob[int(observations[i])]))
        alpha_store.append(alpha)
    i+=1



def output(O):
    string=""
    value=0.0
    for x in O:
            if(x!=0.0):
                x=round(x,6)
                value+=x       
                 
    return print(value)

print(alpha_store)
   







