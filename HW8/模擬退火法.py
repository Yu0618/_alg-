import math
import random

def total_distance(route, cities):
    """計算整條路徑的總距離"""
    dist = 0
    n = len(route)
    for i in range(n):
        c1 = cities[route[i]]
        c2 = cities[route[(i + 1) % n]] # 回到起點
        dist += math.hypot(c1[0] - c2[0], c1[1] - c2[1])
    return dist

def get_neighbor(route):
    """透過 2-opt 交換（反轉子路徑）產生鄰居解"""
    new_route = list(route)
    i, j = sorted(random.sample(range(len(route)), 2))
    new_route[i:j+1] = reversed(new_route[i:j+1])
    return new_route

def simulated_annealing_tsp(cities, initial_temp=1000.0, cooling_rate=0.995, stopping_temp=1e-8, max_iterations=20000):
    n = len(cities)
    # 1. 隨機初始化路徑
    current_route = list(range(n))
    random.shuffle(current_route)
    current_dist = total_distance(current_route, cities)
    
    best_route = list(current_route)
    best_dist = current_dist
    
    temp = initial_temp
    
    # 2. 開始退火循環
    for iteration in range(max_iterations):
        if temp < stopping_temp:
            break
            
        # 產生鄰居
        neighbor = get_neighbor(current_route)
        neighbor_dist = total_distance(neighbor, cities)
        
        # 計算距離差 (能量差)
        delta = neighbor_dist - current_dist
        
        # 3. Metropolis 接受準則
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor
            current_dist = neighbor_dist
            
            # 更新全域最佳解
            if current_dist < best_dist:
                best_route = list(current_route)
                best_dist = current_dist
                
        # 4. 降溫
        temp *= cooling_rate
        
    return best_route, best_dist

# --- 測試範例 ---
if __name__ == "__main__":
    # 定義 8 個城市的座標 (x, y)
    cities = [
        (0, 0), (1, 5), (5, 2), (6, 6),
        (8, 3), (2, 7), (4, 4), (7, 1)
    ]
    
    print(f"總共有 {len(cities)} 個城市，開始進行模擬退火尋優...\n")
    best_route, best_dist = simulated_annealing_tsp(cities)
    
    print("最佳走訪城市順序 (索引):", best_route)
    print("對應座標路徑:", [cities[i] for i in best_route])
    print(f"最短總距離: {best_dist:.4f}")
