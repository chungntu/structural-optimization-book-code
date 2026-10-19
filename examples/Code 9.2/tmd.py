"""
Code 9.2 - Tối ưu bộ giảm chấn khối lượng (TMD) cho cầu đường sắt cao tốc nhịp giản đơn
chịu các đoàn tàu chuẩn HSLM-A1...A10 (EN 1991-2, Phụ lục E).

Mô hình: dầm Euler-Bernoulli tựa đơn, chồng chất dạng dao động (3 dạng uốn), tải trọng là lực tập trung
di động (bỏ qua tương tác tàu - cầu); TMD gắn tại giữa nhịp. Phản ứng được tính trong miền tần số
(FFT) nên mỗi lần đánh giá hàm mục tiêu xét đủ 10 đoàn tàu x toàn bộ dải vận tốc.
"""
import numpy as np

# ------------------------------------------------------------------ cầu (ví dụ minh họa do tác giả lập)
L = 20.0              # m, nhịp tựa đơn
m = 15000.0           # kg/m, khối lượng phân bố (kể cả balát, ray, tà vẹt)
f1 = 6.0              # Hz, tần số riêng thứ nhất
EI = m * (2 * L**2 * f1 / np.pi)**2   # N m^2
zeta = 0.010          # tỷ số cản tối thiểu, cầu BTCT DƯL L >= 20 m (EN 1991-2, Bảng 6.6)
N_MODES = 3           # xét đến max(30 Hz; 1,5f1; f3) theo EN 1990 A2: dạng 3 (54 Hz)
A_LIM = 3.5           # m/s^2, giới hạn gia tốc mặt cầu đường balát (EN 1990 A2.4.4.2.1)
M1 = m * L / 2        # khối lượng dạng 1 (phi_1 = 1 tại giữa nhịp)
x_t = L / 2           # vị trí TMD
V_KMH = np.arange(150.0, 360.0 + 1e-9, 2.5)   # dải vận tốc: đến 1,2 x 300 km/h

# ------------------------------------------------------------------ đoàn tàu HSLM-A (Bảng E.1)
HSLM = {  # tên: (N toa trung gian, D chiều dài toa [m], d khoảng cách trục giá chuyển hướng [m], P [kN])
    'A1': (18, 18, 2.0, 170), 'A2': (17, 19, 3.5, 200), 'A3': (16, 20, 2.0, 180), 'A4': (15, 21, 3.0, 190),
    'A5': (14, 22, 2.0, 170), 'A6': (13, 23, 2.0, 180), 'A7': (13, 24, 2.0, 190), 'A8': (12, 25, 2.5, 190),
    'A9': (11, 26, 2.0, 210), 'A10': (11, 27, 2.0, 210)}

def hslm_axles(name):
    """Vị trí trục (m, tính từ trục đầu) và lực trục (N) của đoàn tàu HSLM-A theo Hình E.1."""
    N, D, d, P = HSLM[name]
    head = np.array([0.0, 3.0, 14.0, 17.0, 20.525, 23.525])  # đầu máy 3+11+3 m; cách 3,525 m tới giá trước của toa cuối
    c0 = 22.025 + D                                        # tâm giá chuyển hướng khớp nối đầu tiên
    centres = c0 + D * np.arange(N + 1)                    # N+1 giá khớp nối (toa cuối - N toa trung gian - toa cuối)
    body = np.concatenate([centres - d / 2, centres + d / 2])
    total = 44.05 + (N + 2) * D                            # đoàn tàu đối xứng: tổng chiều dài giữa hai trục ngoài cùng
    pos = np.sort(np.concatenate([head, body, total - head]))
    return pos, np.full(pos.size, P * 1e3)

# ------------------------------------------------------------------ lực dạng dao động và FFT (tính một lần)
DT, NFFT = 0.004, 8192                                     # 250 Hz, 32,8 s (đủ cho đoàn tàu dài nhất ở 150 km/h)
FREQ = np.fft.rfftfreq(NFFT, DT)
OMEGA = 2 * np.pi * FREQ
WN = np.array([(n**2) * 2 * np.pi * f1 for n in range(1, N_MODES + 1)])
PHI_T = np.array([np.sin(n * np.pi * x_t / L) for n in range(1, N_MODES + 1)])   # dạng tại TMD và tại giữa nhịp

def modal_forces(name, v):
    pos, P = hslm_axles(name)
    t = np.arange(NFFT) * DT
    s = v * t[:, None] - pos[None, :]                      # vị trí từng trục trên cầu
    on = (s >= 0) & (s <= L)
    F = np.empty((N_MODES, NFFT))
    for k in range(N_MODES):
        F[k] = (P[None, :] * np.sin((k + 1) * np.pi * s / L) * on).sum(axis=1)
    return F

CASES = [(nm, v) for nm in HSLM for v in V_KMH / 3.6]

def precompute():
    return np.stack([np.fft.rfft(modal_forces(nm, v), axis=1) for nm, v in CASES])   # (ncase, nmode, nfreq)

FHAT = precompute()

# ------------------------------------------------------------------ phản ứng
def accel_spectra(mu=0.0, gamma=1.0, zt=0.0):
    """Hàm truyền gia tốc giữa nhịp H_n(omega) với mỗi lực dạng n, có/không TMD (ma trận động lực 4x4)."""
    w = OMEGA
    nm = N_MODES
    Z = np.zeros((w.size, nm + 1, nm + 1), complex)
    for k in range(nm):
        Z[:, k, k] = M1 * (WN[k]**2 - w**2 + 2j * zeta * WN[k] * w)
    if mu > 0:
        mt = mu * M1
        wt = gamma * WN[0]
        kt, ct = mt * wt**2, 2 * zt * mt * wt
        zc = kt + 1j * w * ct
        for a in range(nm):
            for b in range(nm):
                Z[:, a, b] += zc * PHI_T[a] * PHI_T[b]
            Z[:, a, nm] = -zc * PHI_T[a]
            Z[:, nm, a] = -zc * PHI_T[a]
        Z[:, nm, nm] = -mt * w**2 + zc
    else:
        Z[:, nm, nm] = 1.0
    # gia tốc giữa nhịp do lực đơn vị ở dạng n: -w^2 * sum_j phi_j(L/2) * [Z^-1]_{j n}
    Zinv = np.linalg.inv(Z)
    return -(w**2)[:, None] * np.einsum('j,fjn->fn', PHI_T, Zinv[:, :nm, :nm])   # (nfreq, nmode)

def peak_accelerations(mu=0.0, gamma=1.0, zt=0.0):
    H = accel_spectra(mu, gamma, zt)                       # (nfreq, nmode)
    A = np.einsum('cnf,fn->cf', FHAT, H)
    a = np.fft.irfft(A, n=NFFT, axis=1)
    return np.abs(a).max(axis=1)                           # theo từng (đoàn tàu, vận tốc)

def a_max(theta, mu):
    gamma, zt = theta
    return peak_accelerations(mu, gamma, zt).max()

def den_hartog(mu):
    return 1 / (1 + mu), np.sqrt(3 * mu / (8 * (1 + mu)**3))

if __name__ == '__main__':
    import time
    print(f'EI = {EI:.4e} N m^2, M1 = {M1/1e3:.0f} t, so truc A1 = {hslm_axles("A1")[0].size}, chieu dai A1 = {hslm_axles("A1")[0][-1]:.1f} m')
    t0 = time.time(); a0 = peak_accelerations(); t1 = time.time()
    i = int(a0.argmax())
    print(f'Khong TMD: a_max = {a0.max():.2f} m/s^2 ({CASES[i][0]}, {CASES[i][1]*3.6:.1f} km/h); 1 lan danh gia {t1-t0:.2f} s')
    for mu in (0.01, 0.02, 0.03):
        g, z = den_hartog(mu)
        print(f'mu={mu:.2f}: Den Hartog gamma={g:.4f}, zeta_t={z:.4f} -> a_max={a_max((g, z), mu):.2f}')
