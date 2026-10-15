def hanoi_recursive(n, source, target, auxiliary):
    if n == 1:
        print(f"將盤子 1 從 {source} 移動到 {target}")
        return
    
    hanoi_recursive(n - 1, source, auxiliary, target)
    
    print(f"將盤子 {n} 從 {source} 移動到 {target}")
    
    hanoi_recursive(n - 1, auxiliary, target, source)

