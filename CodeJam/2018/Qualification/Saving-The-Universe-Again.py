from math import ceil
def savingTheUniverse(hp, p):
    dmg=1
    sum_dmg=0
    charge=[]
    num_s=0
    for i in p:
        if i=="S":
            sum_dmg+=dmg
            num_s+=1
        else:
            charge.append(num_s)
            dmg*=2
            num_s=0
    charge.append(num_s)
    charge.pop(0)
    lengh_charge=len(charge)
    reduce_dmg = int(2**(lengh_charge-1))
    number_of_hack=0
    if sum_dmg <= hp:
        return 0  
    can_reduce = 0
    for i in charge[::-1]:
        can_reduce += i
        diff = sum_dmg-hp
        #print('can_reduce', can_reduce, 'reduce_dmg',reduce_dmg, 'diff', diff, 'number_of_hack', number_of_hack)
        if diff <= reduce_dmg * can_reduce:
            n=ceil(diff/reduce_dmg)
            return number_of_hack+n
        sum_dmg -= reduce_dmg * can_reduce
        reduce_dmg //= 2
        number_of_hack += i
    return "IMPOSSIBLE"

if __name__ == '__main__':
    for i in range(int(input())):
        d, p = input().split()
        d=int(d)
        ans=savingTheUniverse(d, p)
        print("Case #{}: {}".format(i+1, ans))
