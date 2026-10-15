def hanoi_iterative(n, source, target, auxiliary):
    stack = [(n, source, target, auxiliary)]
    
    while stack:
        curr_n, curr_src, curr_tgt, curr_aux = stack.pop()
        
        if curr_n == 1:
            print(f"將盤子 1 從 {curr_src} 移動到 {curr_tgt}")
        else:

            stack.append((curr_n - 1, curr_aux, curr_tgt, curr_src))
            
            stack.append((1, curr_src, curr_tgt, curr_aux))
            
            stack.append((curr_n - 1, curr_src, curr_aux, curr_tgt))

