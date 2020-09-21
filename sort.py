ls = [5,1,3,2,4,8,6,7,9,3,4,1,7]

def merge(left,right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while(i < len(left)):
        result.append(left[i])
        i += 1
    while(j < len(right)):
        result.append(right[j])
        j += 1
    return result

def msort(inlist):
    if len(inlist) < 2:
        return inlist[:]
    else:
        middle = len(inlist)//2
        left = msort(inlist[:middle])
        right = msort(inlist[middle:])
        return merge(left, right)

print("sorted list : " + str(msort(ls)))
print("Highest number : " + str(msort(ls)[-1]))
        
    