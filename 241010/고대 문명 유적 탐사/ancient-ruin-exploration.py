from collections import deque
import copy
k,m = map(int,input().split())
a = [list(map(int,input().split())) for _ in range(5)]
relics = list(map(int,input().split()))
dx = [1,0,-1,0]
dy = [0,-1,0,1]
relics = deque(relics)
answer = []

def BFS(matrix):
    sum_ = 0
    coordinates = []
    count = [[0]*5 for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if count[i][j]:
                continue
            visited = [[False]*5 for _ in range(5)]
            visited[i][j] = True
            cnt = 1
            q = deque([(i,j)])
            while q:
                x,y = q.popleft()
                for k in range(4):
                    ax = x + dx[k]
                    ay = y + dy[k]
                    if 0 <= ax < 5 and 0<= ay < 5 and count[ax][ay] == 0 and not visited[ax][ay] and matrix[ax][ay] == matrix[i][j]:
                         visited[ax][ay] = True
                         cnt += 1
                         q.append((ax,ay))
            if cnt >= 3:
                sum_ += cnt
                for u in range(5):
                    for v in range(5):
                         if visited[u][v] == True:
                             count[u][v] = 1
                             coordinates.append((u,v))
    
    return sum_, coordinates

def rotate(matrix,x,y):
    matrix_copy = copy.deepcopy(matrix)
    top_left = (x-1,y-1)
    submatrix = [row[top_left[1]:top_left[1]+3] for row in matrix[top_left[0]:top_left[0]+3]]
    rotated_submatrix = list(zip(*submatrix[::-1]))
    for i in range(3):
       for j in range(3):
           matrix_copy[top_left[0] + i][top_left[1] + j] = rotated_submatrix[i][j]
    return matrix_copy

def replenish(matrix):
    for j in range(5):
        for i in range(4,-1,-1):
            if matrix[i][j] ==0:
                matrix[i][j] = relics.popleft()
    return matrix

def zeroize(matrix,coordinates):
    for coordinate in coordinates:
         x,y = coordinate
         matrix[x][y] = 0
    return matrix

for p in range(k):
    res = 0
    scores = []
    for i in range(1,4):
        for j in range(1,4):
            _90 = (BFS(rotate(a,i,j)),i,j,90)
            _180 = (BFS(rotate(rotate(a,i,j),i,j)),i,j,180)
            _270 = (BFS(rotate(rotate(rotate(a,i,j),i,j),i,j)),i,j,270)
            scores.append(_90)
            scores.append(_180)
            scores.append(_270)
    scores = sorted(scores,key=lambda x : (-x[0][0],x[3],x[2],x[1]))
    candidates,x,y = scores[0][0][1], scores[0][1], scores[0][2]
    if not candidates:
        break
    if scores[0][3] == 90:
        a = rotate(a,x,y)
    elif scores[0][3] == 180:
        a = rotate(rotate(a,x,y),x,y)
    elif scores[0][3] == 270:
        a = rotate(rotate(rotate(a,x,y),x,y),x,y)
    a = zeroize(a,candidates)
    a = replenish(a)
    res += scores[0][0][0]

    while True:
        score, coordidates = BFS(a)
        if not coordidates:
            break
        res += score
        a = zeroize(a,coordidates)
        a = replenish(a)
    answer.append(res)
print(*answer)