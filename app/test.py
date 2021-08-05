x = {1:"@"}
print(x[1])
x[2] = 3
print(x)
x[2] += 1
print(x)
for i,j in x.items():
    print(i,j)