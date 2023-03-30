import itertools
import numpy as np
from scipy.optimize import minimize

n_move=10
n_out=4

# 技の候補を定義
moves = range(1, 1+n_move)
#["ムーンフォース","シャドーボール",...]等技名を並べたリストを作っても可

# 技の使用率を定義 ここをポケモンホームのデータ使って書き換える
usage_rates =[0.930,0.900,0.511,0.472,0.394,0.162,0.111,0.090,0.086,0.085]#サーフゴー
#[0.714,0.691,0.581,0.499,0.255,0.195,0.172,0.170,0.108,0.194]#カイリュー
#[0.903,0.847,0.842,0.783,0.213,0.198,0.074,0.048,0.026,0.015]#セグ
#[0.939, 0.928, 0.675, 0.409, 0.223, 0.144, 0.079, 0.078, 0.077, 0.058]#ハバカミ


# 技のセットを生成する
moves_sets = list(itertools.combinations(moves, 4))
 
#moves_cmp=[]
moves_cmp_idx=[]
for j in range(n_move):
    moves_cmp_idx.append([])
    for s in moves_sets:
        if moves[j] in s:
            moves_cmp_idx[j].append(moves_sets.index(s))

# 問題の定義
def objective(x):
    return -np.dot(x,x)

# 制約条件の定義
def constraint(x, i):
    s = np.zeros_like(x)
    for j in moves_cmp_idx[i]:
        s[j] = x[j]
    return np.sum(s) - usage_rates[i]

cons = [{'type':'eq', 'fun':constraint, 'args':(i,)} for i in range(len(moves))]
bounds = [(0, 1) for _ in range(len(moves_sets))]

# 初期値
x0 = np.zeros(len(moves_sets))
for i,s in enumerate(moves_sets):
    x0[i] = usage_rates[moves.index(s[0])]*usage_rates[moves.index(s[1])]*usage_rates[moves.index(s[2])]*usage_rates[moves.index(s[3])]

# 最適化
result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

# 出力用のデータ整形
sort_idx = np.argsort(result.x)[-1:-n_out-1:-1]
sorted_x = result.x[sort_idx]
print_name=[moves_sets[i] for i in sort_idx]

print(f"success?: {result.success}")
print("型:          使用率")
for i in range(n_out):
  print(f"{print_name[i]}: {sorted_x[i]:.0%}")
