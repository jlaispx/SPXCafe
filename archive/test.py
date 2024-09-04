sequence = [(6,[2,2,2]),(6,[3,2,1]),(5,[1,2,2])]

sDict = {}
for set in sequence:
    if set[0] not in sDict:
        sDict[set[0]] = [set[1]]
    else:
        sDict[set[0]].append(set[1])
    print(set[0],set[1])
print(sDict)
sortedDict = sorted(sDict.items())

#sequence.sort(key=lambda a: a[0])
for set in sortedDict:
    print(set[0],set[1])