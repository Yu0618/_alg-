搜尋法（Search Algorithms）五大經典問題
1. 老鼠走迷宮：深度優先搜尋（DFS）
2. 狼、羊、甘藍菜過河：廣度優先搜尋（BFS）
3. 八皇后：DFS + 回溯法（Backtracking）
4. NPC 搜尋玩家：A* 啟發式搜尋
5. IC 設計電路繞線：多種路徑搜尋與最佳化方法
一、搜尋問題的基本概念
搜尋問題通常需要先定義：
- 狀態（State）：目前問題的情況。
- 起始狀態（Initial State）：搜尋開始的位置或配置。
- 目標狀態（Goal State）：希望到達的結果。
- 動作（Action）：狀態之間允許的轉換。
- 成本（Cost）：執行動作所需的代價，例如步數、距離或繞線成本。
搜尋演算法會從起始狀態出發，依照規則產生下一個可能狀態，直到找到目標或確認無解。
二、老鼠走迷宮問題（DFS）
2.1 問題說明
給定一個二維迷宮，老鼠從起點出發，必須避開牆壁並找到終點。以下範例使用：
- 0：牆壁，不能通過。
- 1：道路，可以通過。
- 起點：左上角 (0, 0)。
- 終點：右下角 (列數 - 1, 欄數 - 1)。
2.2 使用方法：深度優先搜尋（Depth-First Search）
DFS
會先沿著一個方向盡可能深入；遇到牆壁、邊界或已走過的位置時，就退回上一個位置，再嘗試其他方向。這個退回並改走其他選擇的過程稱為回溯（Backtracking）。
2.3 Python 程式碼
def solve_maze(maze):
    rows, cols = len(maze), len(maze[0])
    path = []
    visited = set()

    def dfs(r, c):
        # 越界、撞牆或走過的位置都不能再走
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or maze[r][c] == 0 or (r, c) in visited):
            return False

        visited.add((r, c))
        path.append((r, c))

        # 抵達右下角
        if (r, c) == (rows - 1, cols - 1):
            return True

        # 依序嘗試：下、右、上、左
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dr, dc in directions:
            if dfs(r + dr, c + dc):
                return True

        # 此路不通，撤銷目前路徑選擇
        path.pop()
        return False

    if dfs(0, 0):
        return path
    return None


maze = [
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0],
    [1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1]
]

result = solve_maze(maze)
print("找到路徑：" if result else "找不到路徑")
print(result)
2.4 執行流程
1. 從起點 (0, 0) 開始。
2. 檢查目前位置是否越界、撞牆或已拜訪。
3. 將合法位置加入 visited 和 path。
4. 如果到達終點，回傳成功。
5. 依照設定的方向遞迴搜尋。
6. 如果所有方向都失敗，從 path 移除目前位置並回到上一層。
2.5 優缺點
- 優點：程式容易實作；通常不需要保存整個搜尋層級。
- 缺點：不保證找到最短路徑；方向順序會影響找到的路徑。
- 注意：`visited` 可避免在迷宮中反覆繞圈。
若迷宮有 R 列、`C` 欄，每個格子最多拜訪一次，時間與空間複雜度約為
O(R × C)。
三、狼、羊、甘藍菜過河問題（BFS）
3.1 問題說明
農夫要把狼、羊、甘藍菜從河的左岸運到右岸。船只能由農夫操作，而且農夫每次最多只能帶一樣物品過河。

限制如下：
- 農夫不在場時，狼不能和羊單獨留在一起。
- 農夫不在場時，羊不能和甘藍菜單獨留在一起。
- 農夫可以自己過河，也可以帶狼、羊或甘藍菜其中一個過河。
目標是讓四者全部安全抵達右岸。
3.2 使用方法：廣度優先搜尋（Breadth-First Search）
BFS
使用佇列（Queue），按照距離起點的步數一層一層搜尋。每次擴展目前狀態的所有合法下一步，再依序處理下一個狀態。

因為每次過河的成本都相同，所以 BFS
找到的第一個目標狀態，就是過河次數最少的解。
3.3 狀態表示
使用四個 0 或 1 表示位置：

(農夫, 狼, 羊, 甘藍菜)
- 0：左岸。
- 1：右岸。
例如 (0, 1, 0, 0) 代表農夫、羊和甘藍菜在左岸，狼在右岸。
3.4 Python 程式碼
from collections import deque

def safe(state):
    farmer, wolf, sheep, cabbage = state

    # 農夫不在同一岸時，狼不能與羊單獨相處
    if wolf == sheep and farmer != wolf:
        return False

    # 農夫不在同一岸時，羊不能與甘藍菜單獨相處
    if sheep == cabbage and farmer != sheep:
        return False

    return True


def bfs_river():
    start = (0, 0, 0, 0)
    goal = (1, 1, 1, 1)

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        farmer = state[0]

        # 農夫可以自己過河，或帶一個與他同岸的物品
        for item in range(1, 4):
            if state[item] == farmer:
                next_state = list(state)
                next_state[0] = 1 - farmer
                next_state[item] = 1 - farmer
                next_state = tuple(next_state)

                if safe(next_state) and next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [next_state]))

        # 農夫自己過河
        next_state = list(state)
        next_state[0] = 1 - farmer
        next_state = tuple(next_state)

        if safe(next_state) and next_state not in visited:
            visited.add(next_state)
            queue.append((next_state, path + [next_state]))

    return None


solution = bfs_river()

if solution:
    names = ["農夫", "狼", "羊", "甘藍菜"]
    for step, state in enumerate(solution):
        left = [names[i] for i, side in enumerate(state) if side == 0]
        right = [names[i] for i, side in enumerate(state) if side == 1]
        print(f"狀態 {step}: 左岸 {left} | 右岸 {right}")
else:
    print("無解")
3.5 執行流程
1. 將初始狀態放入 Queue。
2. 從 Queue 取出最早加入的狀態。
3. 列舉農夫可以執行的過河動作。
4. 檢查新狀態是否符合安全規則。
5. 若合法且未拜訪過，就加入 Queue。
6. 當取出的狀態等於目標狀態時，回傳路徑。
3.6 優缺點
- 優點：在每一步成本相同時，可以找到最少步數的解。
- 缺點：需要保存佇列與已拜訪狀態；狀態數量很大時會耗費記憶體。
- 時間與空間複雜度：一般圖搜尋為 O(V + E)，其中 V 是狀態數，`E`
  是狀態轉移數。
四、八皇后問題（DFS + Backtracking）
4.1 問題說明
八皇后問題是在 8 × 8
的西洋棋棋盤上放置八個皇后，使任意兩個皇后都不能互相攻擊。

皇后可以沿著橫向、縱向與對角線移動，因此必須符合：
1. 每一列只能放一個皇后。
2. 每一行只能放一個皇后。
3. 任意兩個皇后不能位於同一條對角線。
4.2 使用方法：DFS + 回溯法
每次選擇一列，嘗試在不同欄位放置皇后。如果位置合法，就繼續搜尋下一列；如果後續無法完成，就撤銷這次放置，回到上一列嘗試其他位置。

這是一種深度優先搜尋搭配回溯的解法，也是一種典型的限制滿足問題（Constraint
Satisfaction Problem, CSP）。
4.3 Python 程式碼
def solve_queens(n=8):
    board = [-1] * n
    solutions = []

    def dfs(row):
        if row == n:
            solutions.append(board.copy())
            return

        for col in range(n):
            valid = True

            for previous_row in range(row):
                previous_col = board[previous_row]

                # 同欄或同對角線就不能放置
                if (previous_col == col or
                    abs(previous_col - col) == abs(previous_row - row)):
                    valid = False
                    break

            if valid:
                board[row] = col
                dfs(row + 1)

                # 回溯：移除這一列的皇后
                board[row] = -1

    dfs(0)
    return solutions


solutions = solve_queens(8)

print("八皇后解答數量：", len(solutions))

# 顯示第一組解答
for row in range(8):
    print(" ".join("Q" if solutions[0][row] == col else "."
                   for col in range(8)))
4.4 執行流程
1. 從第一列開始放置皇后。
2. 逐一嘗試每個欄位。
3. 檢查是否與之前的皇后發生衝突。
4. 合法就進入下一列。
5. 放滿八個皇后時，找到一組解答。
6. 回溯並繼續尋找其他解答。
4.5 優缺點
- 優點：透過提前檢查衝突，可以排除大量不可能的配置。
- 缺點：皇后數量增加時，搜尋空間會快速擴大。
- 複雜度：最壞情況可用 O(N!)
  作為此逐列放置、逐欄嘗試方法的粗略上界；實際執行會因衝突檢查而剪枝。
補充：標準 8 皇后問題共有 92 組解答（若將旋轉、鏡射視為相同，則有 12
組基本解）。
五、NPC 搜尋玩家問題（A*）
5.1 問題說明
在遊戲中，NPC（Non-Player
Character，非玩家角色）需要從目前位置移動到玩家所在的位置。

地圖可能有牆壁或障礙物，NPC 必須尋找一條可以通行且成本較低的路徑。
5.2 使用方法：A* 搜尋（A-Star Search）
A* 是一種啟發式搜尋演算法，會同時考慮：
- g(n)：從起點移動到目前節點的實際成本。
- h(n)：從目前節點估計到目標的剩餘成本。
- f(n) = g(n) + h(n)：預估經過目前節點到達目標的總成本。
每次優先探索 f(n) 最小的節點。

本範例使用曼哈頓距離（Manhattan Distance）作為啟發式函數：

h = abs(目前列 - 目標列) + abs(目前欄 - 目標欄)

適合只能上下左右移動、每一步成本相同的格子地圖。
5.3 Python 程式碼
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    # 優先佇列元素：(f 值, g 值, 目前位置)
    open_list = [(heuristic(start, goal), 0, start)]

    came_from = {}
    g_score = {start: 0}
    closed = set()

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while open_list:
        _, current_cost, current = heapq.heappop(open_list)

        if current in closed:
            continue

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        closed.add(current)

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor

            if not (0 <= r < rows and 0 <= c < cols):
                continue
            if grid[r][c] == 0 or neighbor in closed:
                continue

            tentative_g = current_cost + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f, tentative_g, neighbor))

    return None


grid = [
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

start = (0, 0)
player = (4, 4)

path = astar(grid, start, player)
print("NPC 移動路徑：", path)
5.4 執行流程
1. 將 NPC 起點放入優先佇列。
2. 計算每個節點的 f(n) = g(n) + h(n)。
3. 取出 f(n) 最小的節點。
4. 檢查是否已抵達玩家位置。
5. 若尚未抵達，擴展上下左右的合法鄰居。
6. 更新更好的路徑成本與前驅節點。
7. 找到目標後，從 came_from 回推完整路徑。
5.5 優缺點
- 優點：利用啟發式函數引導搜尋，通常比不考慮目標方向的搜尋更有效率。
- 缺點：需要設計合適的啟發式函數，也可能使用大量記憶體。
- 若啟發式函數不高估剩餘成本（admissible），且搜尋條件符合 A*
  的標準假設，就能找到最低成本路徑。
- 複雜度：與啟發式品質及地圖結構有關；最壞情況仍可能需要探索大量節點。
六、IC 設計中的電路繞線問題（Routing）
6.1 問題說明
在 IC（Integrated
Circuit，積體電路）設計中，電路繞線是將不同元件的連接點透過金屬導線連接起來。

繞線時必須考慮：
- 導線不能穿過禁止使用的區域。
- 不同網路（Net）的導線必須遵守設計規則，避免短路。
- 盡量減少導線長度。
- 避免線路過度集中，降低擁塞（Congestion）。
- 遵守線寬、線距、過孔（Via）及金屬層等設計規則。
這是一個複雜的最佳化問題，通常不是單純找出一條可行路徑，而是要在多種限制下尋找品質較好的整體繞線結果。
6.2 常見繞線方法
方法一：Maze Routing（迷宮繞線）
- 使用 BFS 在網格中逐層擴展搜尋。
- 從起點開始探索相鄰位置，直到找到終點。
- 若每個網格移動成本相同，可以找到最短步數路徑。
- 缺點是可能探索大量網格，速度較慢。
方法二：Lee's Algorithm（Lee 演算法）
- 是經典的網格迷宮繞線方法。
- 先從起點向外進行波前擴展（Wave Expansion）。
- 為可到達的格子標記距離。
- 到達終點後，依照距離標記回溯路徑。
- 優點是容易理解，且在等成本網格上可找到最短路徑。
- 缺點是記憶體使用量較大。
方法三：A* Routing
- 使用 f(n) = g(n) + h(n) 選擇下一個搜尋位置。
- g(n) 可以代表目前導線長度、轉彎成本或過孔成本。
- h(n) 可以使用到目標的曼哈頓距離作為估計。
- 可以減少不必要的搜尋範圍。
- 適合具有明確目標位置的路徑搜尋。
方法四：Dijkstra Algorithm（戴克斯特拉演算法）
- 從起點開始，優先擴展目前累積成本最低的節點。
- 可處理不同網格移動成本，例如不同金屬層或過孔成本。
- 當所有邊權重非負時，可以找到最低成本路徑。
- 缺點是沒有目標方向的啟發資訊，可能探索較多節點。
方法五：Negotiated Congestion（協商式擁塞繞線）
- 先嘗試為多條 Net 找出可行路徑。
- 計算各區域的擁塞程度。
- 對過度使用的資源增加成本。
- 重新進行繞線，讓不同 Net 避開競爭資源。
- 經過多次迭代，逐步改善整體繞線品質。
這類方法常用於多網路、多限制的實際 IC
繞線流程；不保證每次都能找到全域最佳解。
方法六：Rip-up and Reroute（拆線重繞）
- 先完成一部分線路。
- 如果後續線路無法繞通，或發現擁塞問題，就移除部分既有線路。
- 調整成本或繞線順序後重新繞線。
- 可以搭配 Maze Routing、A* 或協商式擁塞方法使用。
6.3 方法比較
  方法              核心概念           優點                   缺點
  Maze Routing      BFS 搜尋網格       可找到等成本最短路徑   搜尋範圍可能很大

  Lee's Algorithm   波前擴展與回溯     正確性清楚、容易實作   記憶體需求較高

  A*               實際成本 +         可引導搜尋方向         需要設計啟發式函數
啟發式估計                                

  Dijkstra          累積成本最小優先   適合非負加權成本       可能探索較多節點

  Negotiated        反覆調整資源成本   能處理多條線路的擁塞   需要多次迭代
Congestion                                                  
Rip-up and        拆除並重新繞線     能處理衝突與繞線失敗   可能增加執行時間
Reroute
6.4 簡化的 A* 電路繞線示範
以下程式將 IC 繞線簡化為二維網格問題：
- 0：可以繞線。
- 1：障礙物。
- 起點與終點代表兩個需要連接的端點。
- 實際 IC 設計還需要加入多層金屬、過孔、線寬、線距、DRC 與多 Net
  擁塞等條件。
# 可直接使用上一節的 astar() 函式
# 0 表示可通行，1 表示障礙物

chip = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

source = (0, 0)
target = (5, 5)

route = astar(chip, source, target)

if route:
    print("找到繞線路徑：", route)
    print("路徑長度：", len(route) - 1)
else:
    print("無法找到可行繞線路徑")
6.5 實際 IC 繞線的補充
實際設計流程通常會先進行全域繞線（Global
Routing），決定大致的路由資源與通道，再進行詳細繞線（Detailed
Routing），決定實際幾何形狀與金屬層。

除了路徑長度，也需要考慮：
- DRC（Design Rule Check，設計規則檢查）。
- Wirelength（導線總長度）。
- Via Count（過孔數量）。
- Congestion（繞線擁塞）。
- Timing（訊號延遲）。
- Signal Integrity（訊號完整性）。
因此，實際 IC Routing 通常會結合多種演算法與最佳化策略。
七、五種問題的演算法比較
  問題              使用演算法                            主要資料結構      搜尋特色
  老鼠走迷宮        DFS                                   Stack / Recursion 沿路深入，失敗就回溯

  狼羊甘藍菜過河    BFS                                   Queue             逐層搜尋，找最少過河次數

  八皇后            DFS + Backtracking                    Recursion         逐步放置並排除衝突

  NPC 搜尋玩家      A*                                   Priority Queue    使用成本與距離估計引導搜尋
IC 電路繞線       BFS、Lee、A*、Dijkstra、Negotiated   Queue / Priority  同時考慮路徑、成本與資源限制
Congestion 等                         Queue 等
八、總結
本次作業透過五種經典問題，了解不同搜尋演算法的用途與差異。
- DFS：適合深入探索與回溯，例如迷宮和八皇后。
- BFS：適合尋找無權圖中的最少步數解，例如狼羊甘藍菜過河。
- A*：透過啟發式函數估計到目標的成本，適合遊戲 NPC 尋路。
- 電路繞線：需要依照問題規模與限制，結合
  BFS、A*、Dijkstra、協商式擁塞及拆線重繞等方法。
由此可知，沒有一種搜尋演算法適用於所有問題。選擇演算法時，必須考慮狀態空間大小、是否需要最短路徑、成本是否相同、記憶體使用量，以及問題本身的限制條件。
