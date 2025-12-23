# 감시피하기 

import sys

def overlook():
    for x, y in teachers:
        for i in range(4):
            nx,ny=x,y
            while True:
                nx = nx + dx[i]
                ny = ny + dy[i]

                if nx<0 or nx>=n or ny<0 or ny>=n:
                    break

                elif passway[nx][ny] == 'O':
                    break
                
                elif passway[nx][ny] == 'S':
                    return False

    return True 

def dfs(count):
        global result
        
        if result == "YES":
            return

        if count == 3:
            if overlook() == True:
                result = "YES"
            return
            
        for x in range(n):
            for y in range(n):
                # 장애물 설치하기
                if passway[x][y] == 'X':
                    passway[x][y] = 'O'
                    dfs(count+1)
                    # 장애물 없애기
                    passway[x][y] = 'X'

n = int(sys.stdin.readline())

passway = []
for _ in range(n):
        passway.append(list(sys.stdin.readline().split()))

teachers = []
for x in range(n):
    for y in range(n):
        if passway[x][y] == 'T':
            teachers.append((x,y))

dx = [-1,1,0,0]
dy = [0,0,-1,1]

result = "NO"
dfs(0)
print(result)