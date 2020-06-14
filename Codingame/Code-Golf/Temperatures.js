readline()
print(readline().split(' ').map(x=>parseInt(x)).reduce((m,n)=>n*n-n<m*m?n:m)||0)

readline()
print(readline().split` `.reduce((m,n)=>n*n-n<m*m?n:m)||0)
