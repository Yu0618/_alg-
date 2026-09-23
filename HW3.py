def solve_sat(formula, variables):
    n = len(variables)
    solutions = []

    # 總共有 2^n 種真值組合
    total = 2 ** n

    print("真值表")
    print("-" * 50)

    # 顯示變數名稱
    print(" | ".join(variables) + " | Result")
    print("-" * 50)

    # 系統性列舉 0 ~ 2^n - 1
    for number in range(total):

        assignment = {}

        # 將數字轉換成 True / False
        for i, variable in enumerate(variables):
            bit = (number >> (n - i - 1)) & 1
            assignment[variable] = bool(bit)

        # 計算 Boolean Formula
        result = eval(
            formula,
            {"__builtins__": None},
            assignment
        )

        # 印出真值表
        values = [
            int(assignment[variable])
            for variable in variables
        ]

        print(" | ".join(map(str, values)), "|", int(result))

        # 如果公式成立，記錄這組解
        if result:
            solutions.append(assignment)

    print("-" * 50)

    # 判斷 SAT / UNSAT
    if len(solutions) > 0:
        print("SAT")
        print("找到以下滿足條件的解：")

        for solution in solutions:
            print(solution)
    else:
        print("UNSAT")
        print("沒有任何滿足條件的解。")


# ==================================
# 測試範例
# ==================================

variables = ["A", "B", "C"]

formula = "(A or B) and (not A or C)"

solve_sat(formula, variables)
