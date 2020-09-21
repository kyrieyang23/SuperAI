nameList = ['Mike', 'Winn', 'Eak', 'Non']

def countnamewithalphabet(names,alphabet):
    count = 0
    for name in names:
        if alphabet in name:
            count += 1
    return count
print(countnamewithalphabet(nameList,'i'))