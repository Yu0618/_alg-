# 方法 3
memo = {0: 1}

def power2n_3(n):
    if n in memo:
        return memo[n]

    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)

    return memo[n]
