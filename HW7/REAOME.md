# 編輯距離 (Edit Distance / Levenshtein Distance) 動態規劃與步驟視覺化器

這是一個用 Python 撰寫的編輯距離演算法實作。本專案透過**動態規劃（Dynamic Programming）**解決字串相似度與轉換成本計算問題，並內建了**矩陣視覺化印出功能**，讓您可以清楚看見 DP 表格是如何一步步填滿的。

---

## 問題背景與核心概念

* **問題定義**：給定兩個字串 $A$ 與 $B$，計算將字串 $A$ 轉換成字串 $B$ 所需的最少基本編輯操作次數。
* **允許的操作**：
  1. **插入 (Insertion)** 一個字元
  2. **刪除 (Deletion)** 一個字元
  3. **替換 (Substitution)** 一個字元
* **應用場景**：拼字檢查（Auto-correct）、DNA 序列相似度比對、機器翻譯評估與程式碼抄襲檢測。

---

## 演算法比較：非動態規劃 v.s. 動態規劃

| 比較維度 | 非動態規劃（純遞迴暴力搜尋） | 動態規劃（DP 填表法） |
| :--- | :--- | :--- |
| **核心思維** | 盲目窮舉所有可能的分支，重複計算相同子問題 | 記憶子問題結果、由底向上（Bottom-Up）填表 |
| **時間複雜度** | $O(3^{m+n})$（指數級，極慢） | $O(m \times n)$（多項式級，極快） |
| **空間複雜度** | $O(m+n)$（僅佔用遞迴堆疊空間） | $O(m \times n)$（需儲存二維表格） |
| **實際可行性** | 僅適用於極短字串（長度 $< 10$） | 適用於海量文字、基因序列、拼字校正 |

---

## Python 程式碼實作 (`edit_distance.py`)

```python
def print_matrix(dp, s1, s2):
    """輔助函數：印出當前的 DP 矩陣狀態"""
    m, n = len(s1), len(s2)
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
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],    # 刪除 (Deletion)
                    dp[i][j-1],    # 插入 (Insertion)
                    dp[i-1][j-1]   # 替換 (Substitution)
                )
    
    print("=== 最終完成的 DP 矩陣 ===")
    print_matrix(dp, str1, str2)
    
    print(f"字串 '{str1}' 轉換為 '{str2}' 的最少編輯距離為: {dp[m][n]}")
    return dp[m][n]

if __name__ == "__main__":
    s1 = "kitten"
    s2 = "sitting"
    print(f"計算字串 '{s1}' 到 '{s2}' 的編輯距離：\n")
    edit_distance_visualized(s1, s2)
