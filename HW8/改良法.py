import random

def target_function(x):
    return -(x - 3)**2 + 10

def get_neighbor(x):
    delta = random.uniform(-0.1, 0.1) 
    return x + delta


def hill_climbing(iter_count):
  
    current_x = random.uniform(-10, 10)
    current_height = target_function(current_x)
    
    for i in range(iter_count):
        
        next_x = get_neighbor(current_x)
        next_height = target_function(next_x)
        
       
        if next_height > current_height:
            current_x = next_x
            current_height = next_height
            print(f"迭代 {i}: 找到更好的解 x = {current_x:.4f}, y = {current_height:.4f}")
            
    return current_x, current_height

best_x, max_val = hill_climbing(1000)
print(f"--- 最終結果 ---")
print(f"最佳解 x: {best_x}, 最大值: {max_val}")
