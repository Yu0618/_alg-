def print_matrix(dp, s1, s2):
    """輔助函數：印出當前的 DP 矩陣狀態"""
    m, n = len(s1), len(s2)
    # 印出表頭（字串 s2）
    header = "      " + " ".join([f"{c:>3}" for c in ["#"] + list(s2)])
    print(header)
    print("    " + "-" * len(header))
    
    for i in range(m + 1):
        row_label = "#" if i == 0 else s1[i-1]
        row_str = f" {row_label} |"
        for j in range(n + 1):
            row_str += f" {dp[i][j]:3}"
        print(row_str)
    print("-" * 40)

def edit_distance_visualized(str1, str2):
    m, n = len(str1), len(str2)
    
    # 初始化 (m+1) x (n+1) 的 DP 表格
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # 填入邊界條件（空字串的轉換成本）
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    print("=== 初始狀態 (邊界條件填表) ===")
    print_matrix(dp, str1, str2)
    
    # 開始動態規劃填表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                # 字元相同，成本不變
                dp[i][j] = dp[i-1][j-1]
            else:
                # 字元不同，取「刪除」、「插入」、「替換」的最小值 + 1
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # 刪除 (Deletion)
                    dp[i][j-1],    # 插入 (Insertion)
                    dp[i-1][j-1]   # 替換 (Substitution)
                )
    
    print("=== 最終完成的 DP 矩陣 ===")
    print_matrix(dp, str1, str2)
    
    print(f"字串 '{str1}' 轉換為 '{str2}' 的最少編輯距離為: {dp[m][n]}")
    return dp[m][n]

# 執行測試範例
if __name__ == "__main__":
    s1 = "kitten"
    s2 = "sitting"
    print(f"計算字串 '{s1}' 到 '{s2}' 的編輯距離：\n")
    edit_distance_visualized(s1, s2)
