"""
數值微積分與蒙地卡羅積分實作（支援 1 維與 n 維）
AI 使用聲明：本程式由 AI 輔助撰寫與測試，建議執行前先人工檢視數值精度與維度限制。
"""

from __future__ import annotations

import math
import time
from typing import Callable, Iterable, Sequence

import numpy as np

AI_USAGE_NOTICE = "本程式由 AI 輔助生成（含演算法實作、測試範例與說明文件）。"


# =====================================================================
# 一、單變數數值微分與積分
# =====================================================================

def diff_1d(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    """單變數數值微分（中心差分法：O(h^2)）。"""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def integrate_1d_riemann(
    f: Callable[[float], float], low: float, high: float, n_steps: int = 100_000
) -> float:
    """單變數黎曼積分（中點黎曼和）。"""
    if n_steps <= 0:
        raise ValueError("n_steps 必須大於 0")
    dx = (high - low) / n_steps
    midpoints = low + (np.arange(n_steps) + 0.5) * dx
    values = np.array([float(f(float(xi))) for xi in midpoints], dtype=float)
    return float(np.sum(values) * dx)


def integrate_1d_monte_carlo(
    f: Callable[[float], float],
    low: float,
    high: float,
    n_samples: int = 200_000,
    seed: int | None = 42,
) -> tuple[float, float]:
    """
    單變數蒙地卡羅積分。
    回傳：(估計值, 標準誤 std_err)
    """
    if n_samples <= 0:
        raise ValueError("n_samples 必須大於 0")
    rng = np.random.default_rng(seed)
    samples = rng.uniform(low, high, size=n_samples)
    vals = np.array([float(f(float(xi))) for xi in samples], dtype=float)
    volume = high - low
    estimate = volume * float(np.mean(vals))
    std_err = volume * float(np.std(vals, ddof=1)) / math.sqrt(n_samples)
    return estimate, std_err


# =====================================================================
# 二、n 變數數值微分（梯度）與數值積分（黎曼積分法）
# =====================================================================

def gradient_nd(
    f: Callable[[np.ndarray], float], x: Sequence[float], h: float = 1e-6
) -> np.ndarray:
    """
    n 變數數值梯度（對每個維度使用中心差分）。
    f 接受一維 numpy 陣列 x (shape=(n,)) 並回傳純量。
    """
    x_arr = np.asarray(x, dtype=float)
    grad = np.zeros_like(x_arr, dtype=float)
    for i in range(x_arr.size):
        step = np.zeros_like(x_arr, dtype=float)
        step[i] = h
        grad[i] = (float(f(x_arr + step)) - float(f(x_arr - step))) / (2.0 * h)
    return grad


def _as_bounds_arrays(
    low: float | Sequence[float], high: float | Sequence[float], dim: int | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """將 low 與 high 轉換為等長的一維 float 陣列。"""
    if np.ndim(low) == 0 and np.ndim(high) == 0:
        if dim is None:
            raise ValueError("當 low 與 high 為純量時，必須指定 dim")
        low_arr = np.full(dim, float(low), dtype=float)
        high_arr = np.full(dim, float(high), dtype=float)
    else:
        low_arr = np.asarray(low, dtype=float).ravel()
        high_arr = np.asarray(high, dtype=float).ravel()
        if low_arr.shape != high_arr.shape:
            raise ValueError("low 與 high 長度必須相同")
        if low_arr.size == 0:
            raise ValueError("維度 n 至少為 1")

    if np.any(high_arr < low_arr):
        raise ValueError("high 的每個分量都必須大於或等於對應的 low")
    return low_arr, high_arr


def integral(
    f: Callable[[np.ndarray], float | np.ndarray],
    low: float | Sequence[float],
    high: float | Sequence[float],
    n_per_dim: int = 20,
    max_total_points: int = 2_000_000,
) -> float:
    """
    使用黎曼積分法計算 n 變數積分（超體積積分），n 為 low, high 的陣列長度。

    參數：
    - f: 接受形狀為 (..., n) 或 (n,) 的陣列，回傳對應函數值。
    - low, high: 長度為 n 的下界與上界陣列（若傳入純量，會自動視為 1 維）。
    - n_per_dim: 每個維度的切分格數。
    - max_total_points: 為避免維度災難（n_per_dim ** n 爆炸）導致記憶體溢位，
      設定單次網格點數上限；若超過上限，會自動調整每維切分格數（或於極高維度退化為 1 格中點近似）。
    """
    low_arr, high_arr = _as_bounds_arrays(low, high)
    n = low_arr.size
    hypervolume = float(np.prod(high_arr - low_arr))
    if hypervolume == 0.0:
        return 0.0

    # 計算實際每維切分格數 k，使得 k^n <= max_total_points
    if n_per_dim <= 0:
        raise ValueError("n_per_dim 必須大於 0")

    allowed_k = int(max_total_points ** (1.0 / n))
    k = max(1, min(n_per_dim, allowed_k))

    # 建構各維中點座標
    axes_midpoints = [
        low_arr[d] + (np.arange(k, dtype=float) + 0.5) * ((high_arr[d] - low_arr[d]) / k)
        for d in range(n)
    ]

    # 產生笛卡兒積網格點，形狀為 (k^n, n)
    mesh = np.meshgrid(*axes_midpoints, indexing="ij")
    grid_points = np.column_stack([axis.ravel() for axis in mesh])

    # 支援批次評估或逐點評估
    try:
        vals = np.asarray(f(grid_points), dtype=float).ravel()
        if vals.shape[0] != grid_points.shape[0]:
            vals = np.array([float(f(pt)) for pt in grid_points], dtype=float)
    except Exception:
        vals = np.array([float(f(pt)) for pt in grid_points], dtype=float)

    cell_volume = hypervolume / (k**n)
    return float(np.sum(vals) * cell_volume)


# =====================================================================
# 三、n 變數蒙地卡羅積分（超體積）
# =====================================================================

def integral_monte_carlo(
    f: Callable[[np.ndarray], float | np.ndarray],
    low: float | Sequence[float],
    high: float | Sequence[float],
    n_samples: int = 200_000,
    seed: int | None = 42,
) -> tuple[float, float]:
    """
    使用蒙地卡羅法計算 n 變數積分（超體積積分）。
    回傳：(估計值, 標準誤 std_err)
    """
    if n_samples <= 0:
        raise ValueError("n_samples 必須大於 0")

    low_arr, high_arr = _as_bounds_arrays(low, high)
    n = low_arr.size
    hypervolume = float(np.prod(high_arr - low_arr))
    if hypervolume == 0.0:
        return 0.0, 0.0

    rng = np.random.default_rng(seed)
    # 均勻抽樣形狀：(n_samples, n)
    samples = rng.uniform(low=low_arr, high=high_arr, size=(n_samples, n))

    try:
        vals = np.asarray(f(samples), dtype=float).ravel()
        if vals.shape[0] != n_samples:
            vals = np.array([float(f(pt)) for pt in samples], dtype=float)
    except Exception:
        vals = np.array([float(f(pt)) for pt in samples], dtype=float)

    estimate = hypervolume * float(np.mean(vals))
    std_err = hypervolume * float(np.std(vals, ddof=1)) / math.sqrt(n_samples)
    return estimate, std_err


# =====================================================================
# 四、範例函數與測試
# =====================================================================

def sum_of_squares_nd(x: np.ndarray) -> float | np.ndarray:
    """範例函數：f(x) = x_1^2 + ... + x_n^2。"""
    arr = np.asarray(x, dtype=float)
    if arr.ndim == 1:
        return float(np.sum(arr**2))
    return np.sum(arr**2, axis=-1)


def exact_sum_of_squares_integral_01(n: int) -> float:
    """
    在 [0, 1]^n 上，f(x) = sum_{i=1}^n x_i^2 的精確解析積分值：
    每個 x_i^2 在 [0, 1] 的積分為 1/3，共有 n 項，故精確值為 n / 3。
    """
    return n / 3.0


def run_1d_and_gradient_tests() -> None:
    print("=== 1. 單變數數值微分與積分 / 蒙地卡羅積分測試 ===")
    f_1d = lambda x: x**2 + 2.0 * x + 1.0  # f'(x) = 2x + 2, \int_0^2 f(x)dx = 8/3 + 4 + 2 = 26/3
    x_test = 3.0
    num_deriv = diff_1d(f_1d, x_test)
    exact_deriv = 2.0 * x_test + 2.0
    print(f"f(x) = x^2 + 2x + 1 在 x={x_test}: 數值微分={num_deriv:.8f}, 精確值={exact_deriv:.8f}")

    riemann_1d = integrate_1d_riemann(f_1d, 0.0, 2.0, n_steps=100_000)
    mc_1d, mc_1d_err = integrate_1d_monte_carlo(f_1d, 0.0, 2.0, n_samples=200_000, seed=42)
    exact_1d = 26.0 / 3.0
    print(
        f"[0, 2] 積分: 黎曼積分={riemann_1d:.8f}, "
        f"蒙地卡羅={mc_1d:.8f} (±{mc_1d_err:.6f}), 精確值={exact_1d:.8f}\n"
    )

    print("=== 2. n 變數數值梯度測試 ===")
    x_vec = np.array([1.0, 2.0, 3.0])
    num_grad = gradient_nd(sum_of_squares_nd, x_vec)
    exact_grad = 2.0 * x_vec
    print(f"f(x) = sum(x_i^2) 在 x={x_vec}:")
    print(f"  數值梯度 = {num_grad}")
    print(f"  精確梯度 = {exact_grad}\n")


def run_nd_dimension_experiments(dims: Iterable[int] = (1, 2, 5, 100)) -> None:
    print("=== 3. 黎曼積分 integral(f, low, high) vs 蒙地卡羅積分（1D, 2D, 5D, 100D）===")
    print("目標函數：f(x) = x_1^2 + ... + x_n^2，積分區間：low = 0, high = 1（精確值 = n / 3）\n")

    for n in dims:
        low = np.zeros(n, dtype=float)
        high = np.ones(n, dtype=float)
        exact = exact_sum_of_squares_integral_01(n)

        t0 = time.perf_counter()
        riem_val = integral(sum_of_squares_nd, low, high, n_per_dim=20, max_total_points=2_000_000)
        t_riem = time.perf_counter() - t0

        t1 = time.perf_counter()
        mc_val, mc_err = integral_monte_carlo(
            sum_of_squares_nd, low, high, n_samples=200_000, seed=42
        )
        t_mc = time.perf_counter() - t1

        allowed_k = max(1, int((2_000_000) ** (1.0 / n)))
        eff_k = min(20, allowed_k)

        print(f"--- 維度 n = {n}（精確值 = {exact:.6f}）---")
        print(
            f"  黎曼積分 integral() [有效每維格數 k={eff_k}]: "
            f"估計={riem_val:.6f}, 誤差={abs(riem_val - exact):.6f}, 耗時={t_riem*1000:.2f} ms"
        )
        print(
            f"  蒙地卡羅積分 [N=200,000]:          "
            f"估計={mc_val:.6f} (±{mc_err:.6f}), 誤差={abs(mc_val - exact):.6f}, 耗時={t_mc*1000:.2f} ms"
        )
        if n >= 5:
            print(
                f"  註：若 {n} 維每維切 20 格，完整網格需 20^{n} 個點；"
                f"高維下蒙地卡羅收斂速率 O(1/sqrt(N)) 與維度 n 無直接指數相依。"
            )
        print()


def run_unit_assertions() -> None:
    """單元測試斷言（Assertions）。"""
    # 1D 微分與積分測試
    assert abs(diff_1d(lambda x: x**3, 2.0) - 12.0) < 1e-6
    assert abs(integrate_1d_riemann(lambda x: x**2, 0.0, 1.0, n_steps=50_000) - (1.0 / 3.0)) < 1e-6
    mc_1d_val, _ = integrate_1d_monte_carlo(lambda x: x**2, 0.0, 1.0, n_samples=200_000, seed=123)
    assert abs(mc_1d_val - (1.0 / 3.0)) < 0.01

    # n 維梯度測試
    g = gradient_nd(sum_of_squares_nd, [1.5, -2.0, 0.5])
    assert np.allclose(g, [3.0, -4.0, 1.0], atol=1e-6)

    # 1D 與 2D 黎曼積分精準度測試
    assert abs(integral(sum_of_squares_nd, [0.0], [1.0], n_per_dim=100) - (1.0 / 3.0)) < 1e-4
    assert abs(integral(sum_of_squares_nd, [0.0, 0.0], [1.0, 1.0], n_per_dim=50) - (2.0 / 3.0)) < 1e-3

    # 100D 蒙地卡羅積分合理性測試（精確值 100/3 ≈ 33.3333）
    mc_100d, _ = integral_monte_carlo(
        sum_of_squares_nd, np.zeros(100), np.ones(100), n_samples=200_000, seed=42
    )
    assert abs(mc_100d - (100.0 / 3.0)) < 0.5


if __name__ == "__main__":
    print(AI_USAGE_NOTICE)
    print("-" * 60)
    run_1d_and_gradient_tests()
    run_nd_dimension_experiments((1, 2, 5, 100))
    run_unit_assertions()
    print("所有測試斷言皆已通過！")
