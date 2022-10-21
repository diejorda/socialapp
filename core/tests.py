from django.test import TestCase

# Create your tests here.
def idcount(List):
    ids=[]
    counts=[]
    l=0
    while l<=5:
        one=0
        num=0
        for i in List:
            
            count = List.count(i)

            if count > one:
                one=count
                num= i
        List=[value for value in List if value != num]
        ids.append(num)
        counts.append(one)
        l=l+1
    ids=[value for value in ids if value != 0]
    counts=[value for value in counts if value != 0]

    
    return ids,counts