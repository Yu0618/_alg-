def solve_n_queens(n=8):
    solutions = []
    
    # 記錄被佔用的直行與對角線
    cols = set()
    diag1 = set() # row - col
    diag2 = set() # row + col
    
    board = [["." for _ in range(n)] for _ in range(n)]
    
    def dfs(row):
        # 1. 遞迴終止條件：成功排完前 n 行
        if row == n:
            solutions.append(["".join(r) for r in board])
            return
        
        # 2. 嘗試當前行的每一列
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue # 發生衝突，跳過此位置
            
            # 做選擇（放置皇后）
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = "Q"
            
            # 進入下一行
            dfs(row + 1)
            
            # 撤銷選擇（回溯 Backtracking）
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row][col] = "."

    dfs(0)
    return solutions

# 執行並查看結果
sols = solve_n_queens(8)
print(f"八皇后問題總共有 {len(sols)} 種不同的解法。")
print("\n其中第一種解法範例（Q 代表皇后，. 代表空格）：")
for row in sols[0]:
    print(row)
