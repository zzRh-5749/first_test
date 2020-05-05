maxNumber =int(input('caiji'))
lst=list(range(2,maxNumber))
m=int(maxNumber**0.5)
for index,value in enumerate(lst):
    if value>m:
        break
        lst[index+1:]=filter(lambda x:x%value!=0,lst[index+1:])
        print(lst)