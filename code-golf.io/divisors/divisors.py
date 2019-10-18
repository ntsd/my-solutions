# for i in range(1,101):print(*[j for j in range(1,i+1)if i%j<1])

# i=1
# exec('print(*[j for j in range(1,i+1)if i%j<1]);i+=1;'*100)

i=2
while i<101:print(*[j for j in range(1,i+1)if i%j<1]);i+=1
