'''
배열의 크기 n, 숫자가 더해지는 횟수 m, 연속해서 더해질 수 있는 횟수 제한 k
result=0에 더하기

1. 가장 큰 수를 k번 더한다
한 번 더할때마다 m-1한다
가장 큰 수를 k번 더해서 더 못 더하게 되면
2. 다음으로 큰 수를 1번 더한다
한 번 더하고 m-1한다
3. 그러고나서 다시 가장 큰 수로 돌아와서 가장 큰 수를 k번 더한다

m이 0이 될때까지 1~3번 반복한다

+) 가장 큰 수랑 다음으로 큰 수가 같으면 저 로직 그대로 해도 답은 똑같지 않으려나

=> 가장 큰 수랑 다음으로 큰 수를 찾아야하니까 입력받은 데이터에서 인덱스[-1],[-2]

'''

n, m, k = map(int, input().split())
data = list(map(int, input().split()))
data.sort()
first = data[-1]
second = data[-2]

result = 0
while True:
    for i in range(k):
        if m == 0:
            break
        result += first
        m-=1
    if m==0:
        break
    result += second
    m-=1

print(result)


