"""Code 9.1 (phần phân tích): nhân tử Lagrange, nghiệm rời rạc và đường đánh đổi khối lượng - chiều cao."""
import json
import numpy as np
from scipy.optimize import differential_evolution, nnls
import girder as G
from girder_opt import solve_sqp, gvec

MODEL = 'B'
res = json.load(open('girder_results.json'))
xB = np.array(res[MODEL]['sqp_x'])

# ---------------- nhân tử Lagrange: grad m = -sum(lambda_i grad g_i), lambda >= 0 (KKT, Chương 3)
names = list(G.constraints(xB, MODEL).keys())
g0 = gvec(xB, MODEL)
active = [i for i, v in enumerate(g0) if v > -5e-3]
h = 1e-4 * xB
grad_m = np.array([(G.mass(xB + h[j] * np.eye(6)[j]) - G.mass(xB - h[j] * np.eye(6)[j])) / (2 * h[j]) for j in range(6)])
J = np.array([[(gvec(xB + h[j] * np.eye(6)[j], MODEL)[i] - gvec(xB - h[j] * np.eye(6)[j], MODEL)[i]) / (2 * h[j])
               for j in range(6)] for i in active])
lam, resid = nnls(J.T, -grad_m)
print('Nhân tử Lagrange (kg trên một đơn vị nới lỏng ràng buộc chuẩn hóa):')
for i, l in zip(active, lam):
    print(f'   {names[i]:24s} lambda = {l:8.1f} kg   (nới 1% -> giảm ~{0.01*l:.1f} kg)')
print(f'   phần dư điều kiện dừng ||grad m + J^T lambda|| = {resid:.3e} (so với ||grad m|| = {np.linalg.norm(grad_m):.2f})')

# ---------------- nghiệm rời rạc: bề rộng bội số 10 mm, chiều dày theo danh mục thép tấm, D bội số 10 mm
THK = np.array([8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 30, 32, 36, 40, 45, 50], float)
def decode(z):
    i = np.clip(np.round(z).astype(int), 0, None)
    return np.array([10 * i[0], THK[min(i[1], len(THK) - 1)], 10 * i[2], THK[min(i[3], len(THK) - 1)],
                     THK[min(i[4], len(THK) - 1)], 10 * i[5]], float)
def pen_discrete(z):
    x = decode(z)
    return G.mass(x) * (1 + 1e4 * np.maximum(gvec(x, MODEL), 0).sum())
bounds_d = [(5, 60), (0, len(THK) - 1), (5, 60), (0, len(THK) - 1), (0, 6), (50, 300)]
best = None
for seed in range(10):
    r = differential_evolution(pen_discrete, bounds_d, integrality=[True] * 6, seed=seed, maxiter=800,
                               popsize=10, mutation=0.7, recombination=0.6, tol=0, polish=False)
    x = decode(r.x)
    if gvec(x, MODEL).max() <= 0 and (best is None or G.mass(x) < G.mass(best)):
        best = x
print(f'Nghiệm rời rạc tốt nhất (10 lần DE): {best} -> {G.mass(best):.1f} kg')
G.report(best, MODEL, 'nghiệm rời rạc')

# ---------------- đường đánh đổi: min khối lượng với D <= D_max (phương pháp ràng buộc epsilon, Chương 7)
front = []
for Dmax in np.arange(900, 1801, 50):
    extra = [{'type': 'ineq', 'fun': lambda z, Dm=Dmax: Dm - z[5] * G.X_EMP[5]}]
    sols = []
    rng = np.random.default_rng(3)
    x0s = [np.minimum(xB, [600, 100, 600, 100, 30, Dmax])] + \
          [G.BOUNDS[:, 0] + rng.random(6) * (np.minimum(G.BOUNDS[:, 1], [600, 100, 600, 100, 30, Dmax]) - G.BOUNDS[:, 0]) for _ in range(12)]
    for x0 in x0s:
        x, m, v, _ = solve_sqp(MODEL, x0, extra)
        if v <= 1e-6 and x[5] <= Dmax + 1e-6:
            sols.append((m, x))
    m, x = min(sols, key=lambda t: t[0])
    act = [k for k, val in G.constraints(x, MODEL).items() if abs(val) < 5e-3]
    front.append(dict(Dmax=float(Dmax), mass=float(m), x=x.tolist(), active=act))
    print(f'   D <= {Dmax:5.0f} mm: m = {m:8.1f} kg, D = {x[5]:7.1f}, hoạt động: {", ".join(act)}')
res[MODEL]['lambda'] = {names[i]: float(l) for i, l in zip(active, lam)}
res[MODEL]['discrete_x'] = best.tolist()
res[MODEL]['discrete_mass'] = float(G.mass(best))
res[MODEL]['front'] = front
json.dump(res, open('girder_results.json', 'w'), indent=1)
