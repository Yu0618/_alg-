def sqrt_newton(S: float, tol: float = 1e-7, max_iter: int = 100) -> float:
    """使用牛頓迭代法計算 S 的平方根"""
    if S < 0:
        raise ValueError("負數沒有實數平方根")
    if S == 0:
        return 0.0

    # 選擇初始猜測值
    x = S / 2.0 if S >= 1.0 else 1.0

    print(f"尋求 sqrt({S}) 的迭代過程：")
    for i in range(1, max_iter + 1):
        x_next = 0.5 * (x + S / x)
        diff = abs(x_next - x)
        print(f"Iteration {i}: x = {x_next:.10f}, diff = {diff:.2e}")

        if diff < tol:
            print(f"在第 {i} 次迭代收斂！\n")
            return x_next

        x = x_next

    return x


# 測試計算 sqrt(2)
result = sqrt_newton(S=2.0)
print(f"最終計算結果: {result:.10f}")
