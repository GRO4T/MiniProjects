import sys

file = open("medium.txt", 'r')

tree = []
c = ' '
while c != '':
    row = []
    c = file.read(1)
    while c != '\n' and c != '':
        if c >= '0' and c <= '9':
            row.append(ord(c) - ord('0'))
        c = file.read(1)
    if len(row) > 0:
        tree.append(row)

number = file.read(1)
file.close()
#print(tree[len(tree)-1])

#shortestPath = [item[0] for item in tree]
#jshortestSum = sum(shortestPath)
#print(shortestSum)j
#print(shortestPath)
weightTree = [item.copy() for item in tree]
weightTree[0] = tree[0]

for i in range(1, len(tree)):
    print("i = ",i)
    for j in range(0, len(tree[i])):
        leftParent = 99999
        rightParent = 99999
        if (j>=len(tree[i-1])):
            leftParent = weightTree[i-1][j-1]
        if (j<len(tree[i-1])):
            rightParent = weightTree[i-1][j]
        print("r = ",leftParent)
        print("l =", rightParent)
        print("tree=", tree[i][j])
        if leftParent < rightParent:
            weightTree[i][j] = leftParent + tree[i][j]
        else:
            weightTree[i][j] = rightParent + tree[i][j]
print(weightTree)
print(tree)

path = []
i = len(tree)-1
lt = len(tree)
j = 0
smallestSum = weightTree[lt-1][0]
for x in range(1, len(tree[lt-1])):
    if weightTree[lt-1][x] < smallestSum:
        smallestSum=weightTree[lt-1][x]
        j = x

summ = smallestSum
i = lt-1
while i > 0:
    print(len(tree[i]))
    print("j",j)
    path.append(tree[i][j])
    if (j>=len(tree[i-1])):
        leftParent = weightTree[i-1][j-1]
    if (j<len(tree[i-1])):
        rightParent = weightTree[i-1][j]
    print("r",rightParent)
    print("l",leftParent)
    print("c", tree[i][j])
    oldj = j
    if leftParent + tree[i][j] == summ:
        j = j-1
    summ = summ - tree[i][oldj]
    i = i - 1
path.append(tree[0][0])
path = path[::-1]
print(sum(path))
path = ''.join([str(elem) for elem in path])
print("sum = ",smallestSum)
print("path\n",path)




"""
        0
    0       1
0       1      2
"""