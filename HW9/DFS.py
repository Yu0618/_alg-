def solve_maze(maze):
    rows, cols = len(maze), len(maze[0])
    # 建立一個記錄路徑的矩陣，初始皆為 0
    solution = [[0 for _ in range(cols)] for _ in range(rows)]
    
    def dfs(r, c):
        # 1. 檢查邊界條件、牆壁(0)或已經拜訪過的位置(1)
        if r < 0 c < 0 or r >= rows or c >= cols or maze[r][c] == 0 or solution[r][c] == 1:
            return False
        
        # 2. 檢查是否抵達終點 (右下角)
        if r == rows - 1 and c == cols - 1:
            solution[r][c] = 1
            return True
        
        # 3. 標記當前位置為路徑的一部分
        solution[r][c] = 1
        
        # 4. 定義四個移動方向：下、右、上、左
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc
            if dfs(next_r, next_c):
                return True
        
        # 5. 回溯 (Backtracking)：此路不通，取消標記
        solution[r][c] = 0
        return False

    # 從起點 (0, 0) 開始搜尋
    if dfs(0, 0):
        return solution
    else:
        return None

# 測試範例 (1 為路，0 為牆)
maze = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 1, 0, 0],
    [1, 1, 1, 1]
]

path = solve_maze(maze)
if path:
    print("找到路徑（1 代表老鼠走過的軌跡）：")
    for row in path:
        print(row)
else:
    print("此迷宮無解")
