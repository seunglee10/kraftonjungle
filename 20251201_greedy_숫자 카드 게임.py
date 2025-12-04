# 숫자 카드 게임 풀이 1
n,m=map(int,input().split())
result = 0

for i in range(n):
    data=list(map(int,input().split()))
    # 각 행의 최소값들을 리스트에 저장할 필요 없이 현재까지 발견된 최대의 최소값만 result 변수에 저장해서 갱신한다.
    min_value = min(data)
    result = max(result,min_value)  # 첫번째 (0,1) -> 1 / 두번째(1,1) -> 1 / 세번째(1,2) -> 2

print(result)