from collections import deque

def solve_river_crossing():
    # 狀態: (農夫, 狼, 羊, 甘藍菜)，0表示左岸，1表示右岸
    start_state = (0, 0, 0, 0)
    goal_state = (1, 1, 1, 1)
    
    # 檢查狀態是否合法（不會發生吃掉的情況）
    def is_valid(state):
        f, w, g, c = state
        # 狼和羊在一起，但農夫不在
        if w == g and f != w:
            return False
        # 羊和菜在一起，但農夫不在
        if g == c and f != g:
            return False
        return True

    # 佇列存放：(目前狀態, 路徑紀錄)
    queue = deque([(start_state, [start_state])])
    visited = {start_state}

    while queue:
        current_state, path = queue.popleft()

        if current_state == goal_state:
            return path

        f, w, g, c = current_state
        
        # 農夫可以選擇：自己一人過河(None)，或是帶 狼('w')、羊('g')、甘藍菜('c') 之一
        choices = [None, 'w', 'g', 'c']
        
        for item in choices:
            new_f = 1 - f
            new_w, new_g, new_c = w, g, c
            
            if item == 'w':
                if w != f: continue # 狼不在農夫同側，無法攜帶
                new_w = 1 - w
            elif item == 'g':
                if g != f: continue
                new_g = 1 - g
            elif item == 'c':
                if c != f: continue
                new_c = 1 - c
            elif item is None:
                pass # 農夫單獨划船
                
            next_state = (new_f, new_w, new_g, new_c)
            
            # 若新狀態合法且未訪問過，則加入佇列
            if is_valid(next_state) and next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))
                
    return None

# 印出渡河步驟
def print_solution(path):
    names = {'f': '農夫', 'w': '狼', 'g': '羊', 'c': '甘藍菜'}
    for i, state in enumerate(path):
        f, w, g, c = state
        left = [names[k] for k, val in zip(['f', 'w', 'g', 'c'], [f, w, g, c]) if val == 0]
        right = [names[k] for k, val in zip(['f', 'w', 'g', 'c'], [f, w, g, c]) if val == 1]
        print(f"步驟 {i}: 左岸 = {left} | 右岸 = {right}")

path = solve_river_crossing()
if path:
    print_solution(path)
