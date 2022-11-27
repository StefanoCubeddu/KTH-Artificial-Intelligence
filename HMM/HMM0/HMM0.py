
with open("sample_00.txt", 'r') as fobj:
    lines = [[float(num) for num in line.split()] for line in fobj]


# fobj=[]
# fobj.append(input())
# fobj.append(input())
# fobj.append(input())
# lines = [[float(num) for num in line.split()] for line in fobj]

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

def mult(X,Y):
   result=[]
   for i in range(len(X)):
        line=[]
        for j in range(len(Y[0])):
            value=0
            for k in range(len(Y)):
                value += X[i][k] * Y[k][j]
            line.append(value)          
        result.append(line)
   return result



A=createMatrix(int(A[0]),int(A[1]),A[2:])  
pi=createMatrix(int(pi[0]),int(pi[1]),pi[2:]) 
B=createMatrix(int(B[0]),int(B[1]),B[2:])

U=mult(pi,A)
O=mult(U,B)
def to_string(O):
    string=""
    for x in O:
        for j in x:
            string+=str(j)
            string+=" "
    return string

str=to_string(O)
print(len(pi),len(B[0]),str)





