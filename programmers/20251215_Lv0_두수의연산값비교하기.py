def solution(a, b):
    num_a1=int(str(a)+str(b))
    num_b1=int(2*a*b)
    
    if num_a1>=num_b1:
        return num_a1
    elif num_a1<num_b1:
        return num_b1
    
    
    
'''
def solution(a, b):
    num_a1 = int(str(a) + str(b))
    num_b1 = 2*a*b
    return max(num_a1,num_b1)

'''