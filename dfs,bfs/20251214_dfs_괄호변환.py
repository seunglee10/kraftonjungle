# 괄호 변환

def solution(p):
    return dfs(p)

def dfs(p):
    if p == '':
        return p
    
    u, v = di_uv(p)

    if correct(u) == True:
        return u + dfs(v)

    else:
        emp = '(' + dfs(v) + ')'

        for i in u[1:-1]:
            if i == '(':
                emp += ')'
            else:
                emp += '('
        return emp
            
def di_uv(p):
    left = 0
    right = 0
    for i in range(len(p)):
        if p[i] == '(':
            left +=1
        elif p[i] == ')':
            right +=1

        if left == right:
            u = p[:i+1]
            v = p[i+1:]
            return u, v
        
def correct(p):
    left = 0
    right = 0

    for i in p:
        if i == '(':
            left += 1
        elif i == ')':
            right += 1

        if left < right:
            return False
    return True
solution(p)