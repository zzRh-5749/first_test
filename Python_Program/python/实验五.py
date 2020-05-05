maxNumber=int(input("hello"))
numbers=set(range(2,maxNumber))
m=int(maxNumber**0.5)+1
primesLessThanM=[p for p in range(2,m)
if 0 not in [p%d for d in range(2,int(p**0.5)+1)]]
for p in primesLessThanM:
    for i in range(2,maxNumber//p+1):
        numbers.discard(i*p)

        print(numbers)