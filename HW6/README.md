# 算子微積分（Lambda Calculus）Python 解譯器與步驟解析器

這是一個用 Python 撰寫的 Lambda Calculus（λ 演算）解譯器。它不只能夠解析與計算具名及無名稱的 Lambda 表達式，還能**完整追蹤並顯示每一步的歸約過程（Reduction Steps）**、處理 **$\alpha$-轉換（$\alpha$-conversion）以防止變數捕捉**，並支援 **De Bruijn 指標轉換**。

---

## 核心功能特色

1. **多樣化語法支援**：
   - 支援標準抽象符號 `\x.` 或數學符號 `λx.`。
   - 支援函數套用（Application，如 `f x y`）與括號群組。
   - 支援巨集環境定義（如邱奇數、布林邏輯、組合子）。
2. **$\alpha$-conversion（換名機制）**：
   - 在進行 $\beta$-歸約時，自動檢測並重新命名自由變數，徹底避免**變數捕捉 (Variable Capture)** 錯誤。
3. **$\beta$-reduction 完整過程追蹤**：
   - 提供正規順序（Normal Order / 最外層優先）歸約策略，能正確處理如 Y 組合子等遞迴結構。
   - 每一輪歸約均會列印出當前的 Redex（可歸約項）、代入的變數以及化簡後的結果。
4. **De Bruijn Index（無名稱表示法）**：
   - 內建轉換函式，能將具名 Lambda 表達式一鍵轉換為基於變數繫結深度的 De Bruijn 無名稱索引格式。

---

## 專案檔案結構

* `lambda_interpreter.py`：包含 AST 定義、Parser 語法分析器、變數代換、$\alpha$-conversion、$\beta$-reduction 與 De Bruijn 轉換的主程式。
* `README.md`：專案說明與使用指南。

---

## 程式架構解析

### 1. 抽象語法樹 (AST)
定義了三種基本的 Lambda 表達式節點：
- `Var(name)`：變數（例如 `x`）
- `Abs(param, body)`：抽象（例如 `\x. x`）
- `App(fn, arg)`：套用（例如 `(f x)`）

### 2. 詞法與語法分析 (Tokenizer & Parser)
使用正規表達式將字串切割成 Token，並以遞迴下降法（Recursive Descent Parsing）建構 AST，同時支援由 `env` 提供的巨集展開。

### 3. $\alpha$-Conversion 與防捕捉代換
當執行代換 `substitute(node, var_name, replacement)` 時，若抽象參數與替換項中的自由變數衝突，會自動改名（如 `y` 變成 `y'`），確保運算語義正確。

---

## 快速開始與範例

您可以直接執行 `lambda_interpreter.py`，內建已配置好常見的 Church Encodings（邱奇編碼）與組合子範例：

```bash
# 執行範例
python lambda_interpreter.py
