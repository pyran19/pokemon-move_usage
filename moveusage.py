import itertools
import numpy as np
from scipy.optimize import minimize

n_move=10
n_out=4

# 技の候補を定義
moves = range(1, 1+n_move)
#["ムーンフォース","シャドーボール",...]等技名を並べたリストを作っても可

# 技の使用率を定義 ここをポケモンホームのデータ使って書き換える
usage_rates = [0.795, 0.511, 0.480, 0.404, 0.312, 0.211, 0.199, 0.162, 0.148, 0.128]

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

# 最適化
result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

# 出力用のデータ整形
sort_idx = np.argsort(result.x)[-1:-n_out-1:-1]
sorted_x = result.x[sort_idx]
print_name=[moves_sets[i] for i in sort_idx]

print("型:          使用率")
for i in range(n_out):
  print(f"{print_name[i]}: {sorted_x[i]:.0%}")
