"""Code 9.1 (phần giải): SQP đa điểm xuất phát và tiến hóa vi phân (DE) với hàm phạt."""
import time, json
import numpy as np
from scipy.optimize import minimize, differential_evolution
import girder as G

LB_, UB_ = G.BOUNDS[:, 0], G.BOUNDS[:, 1]
X_REF = G.X_EMP.copy()                     # đưa biến về thang đo ~1 để SQP ổn định

def gvec(x, model):
    return np.array(list(G.constraints(x, model).values()))

def solve_sqp(model, x0, extra=None):
    cons = [{'type': 'ineq', 'fun': lambda z: -gvec(z * X_REF, model)}]
    if extra:
        cons += extra
    res = minimize(lambda z: G.mass(z * X_REF) / 1000.0, x0 / X_REF, method='SLSQP',
                   bounds=list(zip(LB_ / X_REF, UB_ / X_REF)), constraints=cons,
                   options=dict(maxiter=500, ftol=1e-10))
    x = res.x * X_REF
    return x, G.mass(x), gvec(x, model).max(), res.nit

def penalized(x, model, alpha=1e4):
    """Hàm phạt dạng V(1 + sum alpha*beta) như công thức (7) của bài báo."""
    viol = np.maximum(gvec(x, model), 0.0).sum()
    return G.mass(x) * (1 + alpha * viol)

def solve_de(model, seed, integrality=None):
    rng = np.random.default_rng(seed)
    init = LB_ + rng.random((25, 6)) * (UB_ - LB_)           # NP = 25 như bài báo
    res = differential_evolution(penalized, G.BOUNDS, args=(model,), strategy='rand1bin',
                                 maxiter=500, mutation=0.7, recombination=0.6, init=init,
                                 tol=0, polish=False, seed=seed, integrality=integrality)
    return res.x, G.mass(res.x), gvec(res.x, model).max(), res.nfev

if __name__ == '__main__':
    out = {}
    for model in ('A', 'B'):
        t0 = time.time()
        best = None
        rng = np.random.default_rng(1)
        starts = [G.X_EMP] + [LB_ + rng.random(6) * (UB_ - LB_) for _ in range(30)]
        sq = []
        for s in starts:
            x, m, v, it = solve_sqp(model, s)
            if v <= 1e-6:
                sq.append((m, x, it))
        sq.sort(key=lambda t: t[0])
        t_sqp = time.time() - t0
        print(f'[{model}] SQP: {len(sq)}/{len(starts)} khả thi, tốt nhất {sq[0][0]:.1f} kg, '
              f'từ thiết kế kinh nghiệm {solve_sqp(model, G.X_EMP)[1]:.1f} kg, {t_sqp:.1f} s')
        print('      x* =', np.round(sq[0][1], 3))
        t0 = time.time()
        de = [solve_de(model, s) for s in range(20)]
        ms = np.array([d[1] for d in de]); feas = np.array([d[2] <= 1e-6 for d in de])
        ib = int(np.argmin(np.where(feas, ms, np.inf)))
        print(f'[{model}] DE 20 lần: tốt nhất {ms[feas].min():.1f}, kém nhất {ms[feas].max():.1f}, '
              f'TB {ms[feas].mean():.1f}, độ lệch {ms[feas].std():.2f} kg, khả thi {feas.sum()}/20, '
              f'{de[0][3]} lượt tính/lần, {time.time()-t0:.1f} s')
        print('      x* =', np.round(de[ib][0], 3))
        G.report(sq[0][1], model, 'nghiệm SQP')
        out[model] = dict(sqp_best=sq[0][0], sqp_x=sq[0][1].tolist(), sqp_feasible=len(sq),
                          sqp_starts=len(starts), de=ms.tolist(), de_feas=feas.tolist(),
                          de_x=de[ib][0].tolist())
    json.dump(out, open('girder_results.json', 'w'), indent=1)
