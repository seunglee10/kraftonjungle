n = int(input())
plans = input().split() # RRRUDD
x,y = 1,1

dx = [-1,1,0,0]
dy = [0,0,-1,1]
move = ['U','D','L','R']

for plan in plans:  # RRRUDD
    for i in range(len(move)):
        if plan == move[i]:
            nx = x + dx[i]
            ny = y + dy[i]
    if nx<1 or nx>n or ny<1 or ny>n:
        continue
    x,y = nx, ny

print(x,y)