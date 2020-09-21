ls = [1,2,3,4,5,6,7,8,9]

def slidingWindow(L,window):
    result = []
    step = 0
    stepw = 0
    for i in range(len(L)-window):
        result.append(L[0 + step:window + step])
        step += 1
        stepw += window
    return result

print("window = 2 : " + str(slidingWindow(ls,2)))
print("window = 3 : " + str(slidingWindow(ls,3)))
print("window = 4 : " + str(slidingWindow(ls,4)))
print("window = 5 : " + str(slidingWindow(ls,5)))
