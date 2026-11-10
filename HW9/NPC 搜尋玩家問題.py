import heapq

def a_star_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    
    # 啟發式函數：計算曼哈頓距離 (Manhattan Distance)
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    # 優先佇列：儲存 (f_score, g_score, current_pos, path)
    pq = []
    initial_h = heuristic(start, goal)
    heapq.heappush(pq, (initial_h, 0, start, [start]))
    
    # 記錄到達每個點的最佳 g_score
    g_scores = {start: 0}
    
    # 四個移動方向：下、上、右、左
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while pq:
        f, g, current, path = heapq.heappop(pq)
        
        # 1. 如果 NPC 抵達玩家位置 (goal)
        if current == goal:
            return path
        
        # 2. 探索鄰近格子
        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor
            
            # 檢查邊界與是否為障礙物 (1 代表通道，0 代表障礙物/牆壁)
            if 0 <= r < rows and 0 <= c < cols and maze[r][c] == 1:
                new_g = g + 1 # 假設每步移動成本為 1
                
                # 如果找到更短的路徑，或該點尚未被訪問過
                if neighbor not in g_scores or new_g < g_scores[neighbor]:
                    g_scores[neighbor] = new_g
                    f_score = new_g + heuristic(neighbor, goal)
                    heapq.heappush(pq, (f_score, new_g, neighbor, path + [neighbor]))
                    
    return None # 無法到達玩家位置

# 測試範例 (1 為路，0 為牆壁)
maze = [
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

npc_start = (0, 0) # NPC 起始位置
player_goal = (4, 4) # 玩家位置

path = a_star_search(maze, npc_start, player_goal)
if path:
    print("NPC 成功找到玩家，移動路徑座標如下：")
    for step in path:
        print(step)
else:
    print("前方有障礙，無法觸及玩家！")
