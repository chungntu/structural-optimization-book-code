"""Code 9.2 (phần tối ưu): Den Hartog, bản đồ đẳng trị, SQP (dạng epigraph), GA và biên Pareto mu - a_max."""
import json, time
import numpy as np
from scipy.optimize import minimize
import tmd as T

BND = np.array([[0.80, 1.10], [0.005, 0.30]])         # gamma = f_t/f_1, zeta_t

def sqp(mu, x0):
    """min s  s.t.  a_c(gamma, zeta_t) <= s với mọi (đoàn tàu, vận tốc) c -- dạng epigraph trơn của min max."""
    def cons(z):
        return z[2] - T.peak_accelerations(mu, z[0], z[1])
    a0 = T.peak_accelerations(mu, *x0).max()
    res = minimize(lambda z: z[2], np.r_[x0, a0], method='SLSQP',
                   bounds=list(map(tuple, BND)) + [(0, None)],
                   constraints=[{'type': 'ineq', 'fun': cons}], options=dict(maxiter=100, ftol=1e-6))
    th = res.x[:2]
    return th, T.a_max(th, mu), res.nit, res.nfev

def ga(mu, pop=24, gens=40, seed=0, pc=0.9, pm=0.2):
    """GA số thực: chọn lọc đấu, lai ghép số học, đột biến Gauss, giữ cá thể tốt nhất (Chương 8)."""
    rng = np.random.default_rng(seed)
    lo, hi = BND[:, 0], BND[:, 1]
    X = lo + rng.random((pop, 2)) * (hi - lo)
    f = np.array([T.a_max(x, mu) for x in X])
    hist = [f.min()]
    for _ in range(gens):
        elite = X[f.argmin()].copy(); fe = f.min()
        def pick():
            i, j = rng.integers(pop, size=2)
            return X[i] if f[i] < f[j] else X[j]
        children = []
        while len(children) < pop - 1:
            p1, p2 = pick(), pick()
            if rng.random() < pc:
                w = rng.random()
                c1, c2 = w * p1 + (1 - w) * p2, (1 - w) * p1 + w * p2
            else:
                c1, c2 = p1.copy(), p2.copy()
            for c in (c1, c2):
                mask = rng.random(2) < pm
                c[mask] += rng.normal(0, 0.1, mask.sum()) * (hi - lo)[mask]
                children.append(np.clip(c, lo, hi))
        X = np.vstack([elite, children[:pop - 1]])
        f = np.r_[fe, [T.a_max(x, mu) for x in X[1:]]]
        hist.append(f.min())
    return X[f.argmin()], f.min(), hist, pop * (gens + 1)

if __name__ == '__main__':
    out = {}
    a0 = T.peak_accelerations()
    out['no_tmd'] = dict(a_max=float(a0.max()), case=T.CASES[int(a0.argmax())][0],
                         v=float(T.CASES[int(a0.argmax())][1] * 3.6))
    print('Không TMD:', out['no_tmd'])
    mu = 0.01
    dh = T.den_hartog(mu)
    a_dh = T.a_max(dh, mu)
    print(f'Den Hartog mu=1%: gamma={dh[0]:.4f}, zeta={dh[1]:.4f}, a_max={a_dh:.3f}')
    # bản đồ đẳng trị a_max(gamma, zeta_t) cho phương pháp đồ thị
    G_ = np.linspace(0.90, 1.04, 36); Z_ = np.linspace(0.01, 0.20, 32)
    t0 = time.time()
    grid = np.array([[T.a_max((g, z), mu) for g in G_] for z in Z_])
    print(f'Bản đồ {grid.size} điểm: {time.time()-t0:.0f} s; nhỏ nhất trên lưới {grid.min():.3f}')
    t0 = time.time()
    th_s, a_s, nit, nfev = sqp(mu, np.array(dh))
    print(f'SQP: gamma={th_s[0]:.4f}, zeta={th_s[1]:.4f}, a_max={a_s:.3f} ({nit} vòng lặp, {nfev} lượt, {time.time()-t0:.0f} s)')
    t0 = time.time()
    gas = [ga(mu, seed=s) for s in range(3)]
    bi = int(np.argmin([g[1] for g in gas]))
    print(f'GA (3 lần): ' + ', '.join(f'{g[1]:.3f}' for g in gas) + f'; tốt nhất gamma={gas[bi][0][0]:.4f}, zeta={gas[bi][0][1]:.4f}; {gas[bi][3]} lượt/lần; {time.time()-t0:.0f} s')
    out['mu1'] = dict(den_hartog=[float(v) for v in dh], a_dh=float(a_dh), sqp=th_s.tolist(), a_sqp=float(a_s),
                      sqp_nit=int(nit), sqp_nfev=int(nfev), ga=[g[0].tolist() for g in gas], a_ga=[float(g[1]) for g in gas],
                      ga_hist=[list(map(float, g[2])) for g in gas], ga_nfev=int(gas[0][3]),
                      grid=dict(gamma=G_.tolist(), zeta=Z_.tolist(), a=grid.tolist()))
    # biên Pareto: với mỗi mu, cực tiểu a_max theo (gamma, zeta_t)
    front = []
    x0 = np.array(T.den_hartog(0.0025))
    for mu_k in [0.0025, 0.005, 0.0075, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05]:
        start = x0 if T.a_max(x0, mu_k) < T.a_max(T.den_hartog(mu_k), mu_k) else np.array(T.den_hartog(mu_k))
        th, a, _, _ = sqp(mu_k, start)
        x0 = th
        front.append(dict(mu=mu_k, gamma=float(th[0]), zeta=float(th[1]), a_max=float(a),
                          a_dh=float(T.a_max(T.den_hartog(mu_k), mu_k))))
        print(f'   mu={mu_k*100:4.2f}%  m_t={mu_k*T.M1/1e3:5.2f} t  gamma={th[0]:.4f} zeta={th[1]:.4f}  a_max={a:.3f} (Den Hartog {front[-1]["a_dh"]:.3f})')
    out['front'] = front
    # phản ứng theo vận tốc để vẽ hình (không TMD, Den Hartog, tối ưu) với mu = 1%
    curves = {}
    for lab, args in (('none', (0.0, 1.0, 0.0)), ('dh', (mu, *dh)), ('opt', (mu, *th_s))):
        a = T.peak_accelerations(*args).reshape(len(T.HSLM), len(T.V_KMH))
        curves[lab] = a.tolist()
    out['curves'] = dict(v=T.V_KMH.tolist(), trains=list(T.HSLM), a=curves)
    json.dump(out, open('tmd_results.json', 'w'), indent=1)
