# 62
i=1;exec("print('Fizz'*(i%3<1)+'Buzz'*(i%5<1)or i);i+=1;"*100)

# 61
i=0;exec("print(i%3//2*'Fizz'+i%5//4*'Buzz'or-~i);i+=1;"*100)

# 60
i=0
while i<100:print(i%3//2*'Fizz'+i%5//4*'Buzz'or-~i);i+=1

# 59
for i in range(100):print(i%3//2*"Fizz"+i%5//4*"Buzz"or-~i)

# 59
i=1
while i<101:print('FizzBuzz'[i%-3&4:12&8-i%5]or i);i+=1
