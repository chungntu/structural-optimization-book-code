"""Kiểm chứng lời giải miền tần số bằng tích phân trực tiếp (solve_ivp) cho vài trường hợp."""
import numpy as np
from scipy.integrate import solve_ivp
import tmd as T

def time_domain(name, v, mu=0.0, gamma=1.0, zt=0.0):
    pos, P = T.hslm_axles(name)
    nm = T.N_MODES
    mt = mu * T.M1; wt = gamma * T.WN[0]; kt = mt * wt**2; ct = 2 * zt * mt * wt
    def rhs(t, y):
        q, qd = y[:nm], y[nm:2 * nm]
        s = v * t - pos; on = (s >= 0) & (s <= T.L)
        F = np.array([(P * np.sin((k + 1) * np.pi * s / T.L) * on).sum() for k in range(nm)])
        acc = (F - T.M1 * (2 * T.zeta * T.WN * qd + T.WN**2 * q)) / T.M1
        if mu > 0:
            z, zd = y[2 * nm], y[2 * nm + 1]
            rel = T.PHI_T @ q - z; reld = T.PHI_T @ qd - zd
            ft = kt * rel + ct * reld
            acc = acc - T.PHI_T * ft / T.M1
            return np.concatenate([qd, acc, [zd, ft / mt]])
        return np.concatenate([qd, acc])
    n = 2 * nm + (2 if mu > 0 else 0)
    tend = (pos[-1] + T.L) / v + 3.0
    t = np.arange(0, tend, 0.002)
    sol = solve_ivp(rhs, (0, tend), np.zeros(n), t_eval=t, max_step=0.002, rtol=1e-8, atol=1e-10)
    q = sol.y[:nm]
    qdd = np.gradient(np.gradient(q, t, axis=1), t, axis=1)
    return np.abs(T.PHI_T @ qdd).max()

a_freq = T.peak_accelerations()
for name, vk in (('A1', 259.2), ('A7', 345.6), ('A4', 302.4)):
    i = min(range(len(T.CASES)), key=lambda c: (T.CASES[c][0] != name) * 1e9 + abs(T.CASES[c][1] * 3.6 - vk))
    vk2 = T.CASES[i][1] * 3.6
    print(f'{name} {vk2:.1f} km/h: FFT {a_freq[i]:.3f}  ODE {time_domain(name, vk2/3.6):.3f} m/s^2')
mu, (g, z) = 0.02, T.den_hartog(0.02)
a_t = T.peak_accelerations(mu, g, z)
i = int(a_t.argmax()); nm, vv = T.CASES[i]
print(f'With TMD mu=2% worst {nm} {vv*3.6:.1f}: FFT {a_t[i]:.3f}  ODE {time_domain(nm, vv, mu, g, z):.3f}')
i0 = int(a_freq.argmax())
print(f'Without TMD worst: {T.CASES[i0][0]} {T.CASES[i0][1]*3.6:.1f} km/h a = {a_freq[i0]:.2f}')
