import sys

def dfs(n, data, calc, current_total, index):
    global max_result, min_result

    if index == n:
        max_result = max(max_result, current_total)
        min_result = min(min_result, current_total)
        return
    
    for i in range(4):
        if calc[i] > 0:
            calc[i] -= 1

            # 더하기
            if i == 0: 
                next_total = current_total + data[index]

            # 빼기
            elif i == 1:
                next_total = current_total - data[index]

            # 곱하기
            elif i == 2:
                next_total = current_total * data[index]

            # 나누기
            elif i == 3:
                next_total = int(current_total / data[index])

            dfs(n, data, calc, next_total, index+1)
            calc[i] += 1
   
max_result = -int(1e9)
min_result = int(1e9)

n = int(sys.stdin.readline())
data = list(map(int,sys.stdin.readline().split()))
calc = list(map(int,sys.stdin.readline().split()))

dfs(n,data,calc, data[0], 1)    
print(max_result)
print(min_result)
