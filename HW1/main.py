import time
import method1_builtin
import method2a_pure_recursion
import method2b_linear_recursion
import method3_memoization

def measure_time(method_name, func, n):
    print(f"[{method_name}] 正在計算 2^{n}...")
    start_time = time.time()
    try:
        func(n)
        end_time = time.time()
        print(f" ✅ 完成! 耗時: {end_time - start_time:.8f} 秒\n")
    except Exception as e:
        print(f" ❌ 失敗或發生錯誤: {e}\n")

if __name__ == "__main__":
    n_target = 100
    
    print(f"========== 演算法效能分析開始 (n = {n_target}) ==========\n")
    
    measure_time("方法 1: 內建運算子", method1_builtin.power2n, n_target)
    measure_time("方法 2b: 線性遞迴", method2b_linear_recursion.power2n, n_target)
    measure_time("方法 3: 查表法 (Memoization)", method3_memoization.power2n, n_target)
    
    print("========== 警告測試 ==========")
    print("方法 2a 為指數時間複雜度，為避免程式卡死，改以 n=30 進行對照測試：")
    measure_time("方法 2a: 純遞迴 (n=30)", method2a_pure_recursion.power2n, 30)
