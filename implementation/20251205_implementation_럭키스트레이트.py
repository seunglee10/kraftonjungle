n = input()
lenght = len(n)
sum = 0

for i in range(lenght//2):
    sum += int(n[i])

for i in range(lenght//2, lenght):
    sum -= int(n[i])

if sum == 0:
    print("LUCKY")
else:
    print("READY")