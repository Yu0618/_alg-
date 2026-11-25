# 數值微積分與蒙地卡羅積分實作

## 功能簡介

本專案使用 Python (`numpy`) 實作以下內容：

1. **單變數數值微分**：`diff_1d(f, x, h)`，採用中心差分法 $\frac{f(x+h)-f(x-h)}{2h}$。
2. **單變數數值積分（黎曼積分）**：`integrate_1d_riemann(f, low, high, n_steps)`，採用中點黎曼和。
3. **單變數蒙地卡羅積分**：`integrate_1d_monte_carlo(f, low, high, n_samples, seed)`，透過均勻抽樣估計積分值與標準誤。
4. **n 變數數值微分（梯度）**：`gradient_nd(f, x, h)`，逐維計算偏導數組成梯度向量 $\nabla f(x)$。
5. **n 變數數值積分（黎曼積分）**：`integral(f, low, high, n_per_dim, max_total_points)`，依據 `low` 與 `high` 的陣列長度決定維度 $n$，計算超體積積分。
6. **n 變數蒙地卡羅積分（超體積）**：`integral_monte_carlo(f, low, high, n_samples, seed)`，於 $[low_1, high_1] \times \dots \times [low_n, high_n]$ 超長方體均勻抽樣估計超體積積分。

## 範例題目與維度災難說明

測試範例針對：

$$f(x) = x_1^2 + x_2^2 + \dots + x_n^2, \quad x \in [0, 1]^n$$

在 $[0, 1]^n$ 上，各變數獨立均勻分佈於 $[0, 1]$，每一項 $\int_{[0,1]^n} x_i^2\,dx = \frac{1}{3}$，因此 $n$ 維積分的精確解析解為：

$$\int_{[0,1]^n} \sum_{i=1}^n x_i^2\,dx = \frac{n}{3}$$

- **1 維（$n=1$）**：精確值為 $\frac{1}{3} \approx 0.333333$
- **2 維（$n=2$）**：精確值為 $\frac{2}{3} \approx 0.666667$
- **5 維（$n=5$）**：精確值為 $\frac{5}{3} \approx 1.666667$
- **100 維（$n=100$）**：精確值為 $\frac{100}{3} \approx 33.333333$

### 為什麼高維度（如 100 維）不能直接用固定細網格做黎曼積分？
若每個維度切 $k$ 格，$n$ 維網格點總數為 $k^n$。當 $n=100, k=20$ 時，網格點數為 $20^{100}$，遠超記憶體與運算能力（即**維度災難 / Curse of Dimensionality**）。程式中的 `integral()` 設有 `max_total_points` 上限保護，並在輸出中展示此現象；而**蒙地卡羅積分**的統計誤差收斂速度為 $O(1/\sqrt{N})$，在 $n=100$ 時仍能穩定且快速地給出近似解。

