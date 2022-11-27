with open("hmm3_01.txt", 'r') as fobj:
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






def get_delta(alpha,ob_prob,A):
    i=0
    j=0
    alpha_state={}
    alpha_val=[]
    while(i<len(A)):
        best=0.0
        best_state=[]
        j=0
        while(j<len(A[i])):
            val=0.0
            val=float(alpha[j])*float(A[j][i])*float(ob_prob[i])
            if(val>best):
                best=val
                best_state=[]
                best_state.append(j)
            elif(val==best and best!=0):
                best_state.append(j) 
            j+=1
        if(best>0.0):
            alpha_val.append(best)
            alpha_state[i]=best_state
        else:
            alpha_val.append(best)
            alpha_state[i]="Zero"              
        i+=1

    return alpha_state,alpha_val



delta_val=[]
delta_state=[]
delta_val.append(first_mult(pi,obs_prob[int(observations[0])]))
i=1

while(i<len(observations)):
    state,val=get_delta(delta_val[i-1],obs_prob[int(observations[i])],A)
    delta_val.append(val)
    delta_state.append(state)
    i+=1





def stampa_seq(delta_val,delta_state,len):
    X=[]
    max_value = max(delta_val[len])
    index = delta_val[len].index(max_value)
    X.append(index)
    i=len
    i-=1
    while(i>=0):
        index=int(delta_state[i][index][0])
        X.append(index)
        i-=1
    return X

ris=stampa_seq(delta_val,delta_state,len(delta_val)-1)

ris=list(reversed(ris))



def to_string(O):
    string=""
    for j in O:
        string+=str(j)
        string+=" "
    return string


print(to_string(ris))


