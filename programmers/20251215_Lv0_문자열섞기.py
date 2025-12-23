def solution(str1, str2):
    answer = ''
    for i in range(len(str1)):
        answer += str1[i]+str2[i]
    return answer


'''
def solution(str1, str2):
    answer =''
    for s1,s2 in zip(str1,str2):
        answer +=s1+s2
    return answer
'''