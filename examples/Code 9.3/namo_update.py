"""Code 9.3 (phần hiệu chỉnh): bình phương tối thiểu có cận (Gauss-Newton/vùng tin cậy) và GA."""
import json, time
import numpy as np
from scipy.optimize import least_squares
import namo as N

MDL = N.NamO()
W = np.ones(5)                                            # trọng số các dạng

# Bộ tham số 1 (như bài báo): E, k_rot, k_v, k_h; Bộ 2 (chọn theo độ nhạy): E, k_rot, m_ns, alpha_lb
SETS = {
    'paper': dict(names=['E (GPa)', 'log10 k_rot', 'k_v (1e10 N/m)', 'k_h (1e7 N/m)'],
                  lo=np.array([190, 5.0, 1.0, 1.0]), hi=np.array([220, 9.0, 2.0, 2.0]),
                  x0=np.array([200, np.log10(8e5), 1.3, 1.5])),
    'sens': dict(names=['E (GPa)', 'log10 k_rot', 'm_ns (kg/m)', 'alpha_lb'],
                 lo=np.array([190, 5.0, 100, 0.5]), hi=np.array([220, 9.0, 350, 3.0]),
                 x0=np.array([200, np.log10(8e5), 247.2, 1.0])),
}

def frequencies(theta, which):
    if which == 'paper':
        E, lk, kv, kh = theta
        f, V = MDL.modes(E=E * 1e9, k_rot=10**lk, k_v=kv * 1e10, k_h=kh * 1e7)
    else:
        E, lk, mns, alb = theta
        old_m, old_b = N.M_NS, N.SEC['lower_brace']
        N.M_NS = mns
        A, Iz, Iy = old_b
        N.SEC['lower_brace'] = (alb * A, alb * Iz, alb * Iy)
        try:
            f, V = MDL.modes(E=E * 1e9, k_rot=10**lk)
        finally:
            N.M_NS, N.SEC['lower_brace'] = old_m, old_b
    return MDL.paired(f, MDL.classify(V, MDL.M_last))

def residual(theta, which):
    fp = frequencies(theta, which)
    r = W * (fp - N.MEASURED) / N.MEASURED
    return np.where(np.isnan(r), 1.0, r)                  # dạng không tìm thấy -> phạt

def objective(theta, which):
    return float(np.sum(residual(theta, which)**2))

def solve_ls(which, x0):
    s = SETS[which]
    scale = s['hi'] - s['lo']
    res = least_squares(lambda z: residual(s['lo'] + z * scale, which), (x0 - s['lo']) / scale,
                        bounds=(0, 1), diff_step=1e-3, method='trf', xtol=1e-8, ftol=1e-10)
    th = s['lo'] + res.x * scale
    return th, objective(th, which), res.nfev

def ga(which, pop=20, gens=25, seed=0):
    s = SETS[which]; rng = np.random.default_rng(seed)
    lo, hi = s['lo'], s['hi']
    X = lo + rng.random((pop, lo.size)) * (hi - lo)
    f = np.array([objective(x, which) for x in X]); hist = [f.min()]
    for _ in range(gens):
        e, fe = X[f.argmin()].copy(), f.min()
        def pick():
            i, j = rng.integers(pop, size=2); return X[i] if f[i] < f[j] else X[j]
        kids = []
        while len(kids) < pop - 1:
            p1, p2 = pick(), pick(); w = rng.random(lo.size)
            c = w * p1 + (1 - w) * p2
            mask = rng.random(lo.size) < 0.25
            c[mask] += rng.normal(0, 0.1, mask.sum()) * (hi - lo)[mask]
            kids.append(np.clip(c, lo, hi))
        X = np.vstack([e, kids]); f = np.r_[fe, [objective(x, which) for x in X[1:]]]
        hist.append(f.min())
    return X[f.argmin()], f.min(), hist, pop * (gens + 1)

if __name__ == '__main__':
    out = {}
    for which in ('paper', 'sens'):
        s = SETS[which]
        f0 = frequencies(s['x0'], which)
        t0 = time.time()
        th_ls, J_ls, nfev = solve_ls(which, s['x0'])
        t_ls = time.time() - t0
        t0 = time.time()
        th_ga, J_ga, hist, nfev_ga = ga(which)
        t_ga = time.time() - t0
        f_ls, f_ga = frequencies(th_ls, which), frequencies(th_ga, which)
        print(f'== Bộ tham số "{which}": J0 = {objective(s["x0"], which):.4f}')
        print(f'   ban đầu  f = {np.round(f0, 3)}  sai số % = {np.round(100*(f0-N.MEASURED)/N.MEASURED, 1)}')
        print(f'   BPTT     f = {np.round(f_ls, 3)}  sai số % = {np.round(100*(f_ls-N.MEASURED)/N.MEASURED, 1)}  J = {J_ls:.4f}, {nfev} lượt, {t_ls:.0f} s')
        print(f'            theta = {dict(zip(s["names"], np.round(th_ls, 3)))}')
        print(f'   GA       f = {np.round(f_ga, 3)}  sai số % = {np.round(100*(f_ga-N.MEASURED)/N.MEASURED, 1)}  J = {J_ga:.4f}, {nfev_ga} lượt, {t_ga:.0f} s')
        print(f'            theta = {dict(zip(s["names"], np.round(th_ga, 3)))}', flush=True)
        out[which] = dict(names=s['names'], x0=s['x0'].tolist(), lo=s['lo'].tolist(), hi=s['hi'].tolist(),
                          f0=f0.tolist(), ls=th_ls.tolist(), f_ls=f_ls.tolist(), J_ls=J_ls, nfev_ls=int(nfev),
                          ga=th_ga.tolist(), f_ga=f_ga.tolist(), J_ga=float(J_ga), ga_hist=list(map(float, hist)),
                          nfev_ga=int(nfev_ga), J0=objective(s['x0'], which))
    out['measured'] = N.MEASURED.tolist()
    json.dump(out, open('namo_results.json', 'w'), indent=1)
