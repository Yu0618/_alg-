from collections import deque

def lee_routing(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    sr, sc = start
    tr, tc = target
    
    # 如果起點或終點本身是障礙物，則無解
    if grid[sr][sc] == 0 or grid[tr][tc] == 0:
        return None
        
    # 建立距離/訪問記錄矩陣，-1 代表未訪問
    dist = [[-1 for _ in range(cols)] for _ in range(rows)]
    dist[sr][sc] = 0
    
    queue = deque([(sr, sc)])
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] # 下、上、右、左
    
    found = False
    # 1. 傳播階段 (Propagation)：從起點向四周擴散尋找終點
    while queue:
        r, c = queue.popleft()
        
        if (r, c) == (tr, tc):
            found = True
            break
            
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # 檢查邊界、是否為通道(1)、是否未被訪問過(-1)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
                
    if not found:
        return None # 找不到繞線路徑
        
    # 2. 回溯階段 (Backtrace)：從終點往回尋找距離遞減的最短路徑
    path = []
    curr = (tr, tc)
    path.append(curr)
    
    while curr != (sr, sc):
        r, c = curr
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == dist[r][c] - 1:
                curr = (nr, nc)
                path.append(curr)
                break
                
    path.reverse() # 調整順序由起點排到終點
    return path

# 測試範例：1 代表可通行通道，0 代表障礙物（如現有導線或巨集單元）
grid = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1]
]

start_pin = (0, 0)
target_pin = (4, 4)

route = lee_routing(grid, start_pin, target_pin)
if route:
    print("成功找到晶片繞線路徑座標：")
    for step in route:
        print(step)
else:
    print("繞線失敗：封鎖區過多，找不到可行路徑")
