"""
Code 9.3 - Mô hình phần tử hữu hạn không gian nhịp thứ nhất cầu giàn thép đường sắt Nam Ô (Đà Nẵng).

Số liệu theo Tran-Ngoc, Khatir, De Roeck, Bui-Tien, Nguyen-Ngoc, Abdel Wahab (2018),
Sensors 18(12):4131 (CC BY 4.0): tiết diện 9 nhóm thanh (Bảng 2), vật liệu (Bảng 3),
tần số đo (Bảng 5). Hình học dựng lại từ các hình của bài báo: nhịp 75 m chia 8 khoang,
cánh trên dạng parabol cao 13 m ở giữa nhịp, hai giàn chủ cách nhau 5 m.
Phần tử dầm không gian Euler-Bernoulli (6 bậc tự do/nút), ma trận khối lượng nhất quán.
"""
import numpy as np
from scipy.linalg import eigh

SPAN, NPANEL, H, B = 75.0, 8, 13.0, 5.0
RHO = 7850.0
M_NS = 247.2           # kg/m, khối lượng ray và bộ phận không kết cấu trên mỗi cánh dưới
Y_STR = 1.0            # m, vị trí dầm dọc (giả thiết, khổ đường 1 m)
# A (m2), Iz (m4, uốn ngoài mặt phẳng), Iy (m4, uốn trong mặt phẳng chính); J giả thiết (bài báo không cho)
SEC = {
    'upper':   (0.056, 6.70e-4, 3.10e-3), 'lower':   (0.020, 2.10e-4, 6.30e-4),
    'vertical': (0.010, 5.49e-5, 1.15e-4), 'diagonal': (0.014, 1.24e-4, 2.78e-4),
    'stringer': (0.020, 2.07e-4, 6.27e-4), 'transverse': (0.026, 2.03e-4, 3.61e-3),
    'strut':   (0.020, 6.25e-4, 2.80e-3), 'upper_brace': (0.0036, 8.00e-6, 1.09e-5),
    'lower_brace': (0.0049, 2.38e-6, 4.38e-6)}
J_FACTOR = 0.05        # J = J_FACTOR*(Iy + Iz), giả thiết
MEASURED = np.array([1.45, 3.11, 3.28, 4.62, 6.05])           # Hz, 5 dạng đầu (Bảng 5)
MEASURED_TYPE = ['L1', 'T1', 'L2', 'V1', 'T2']                 # ngang 1, xoắn 1, ngang 2, uốn đứng 1, xoắn 2
NOMINAL = dict(E=2.0e11, k_rot=8.0e5, k_v=1.3e10, k_h=1.5e7)  # giá trị ban đầu theo Bảng 7 bài báo

def geometry():
    dx = SPAN / NPANEL
    nodes, tag = [], {}
    def add(name, xyz):
        tag[name] = len(nodes); nodes.append(xyz)
    for side, y in (('A', -B / 2), ('B', B / 2)):
        for k in range(NPANEL + 1):
            add(f'L{side}{k}', (k * dx, y, 0.0))
        for k in range(1, NPANEL):
            x = k * dx
            add(f'U{side}{k}', (x, y, H * (1 - ((x - SPAN / 2) / (SPAN / 2))**2)))
    for s, y in (('S1', -Y_STR), ('S2', Y_STR)):
        for k in range(NPANEL + 1):
            add(f'{s}{k}', (k * dx, y, 0.0))
    E = []  # (n1, n2, nhóm, có lò xo xoay ở đầu nút)
    for side in 'AB':
        for k in range(NPANEL):
            E.append((f'L{side}{k}', f'L{side}{k+1}', 'lower', False))
        up = [f'L{side}0'] + [f'U{side}{k}' for k in range(1, NPANEL)] + [f'L{side}{NPANEL}']
        for a, b in zip(up[:-1], up[1:]):
            E.append((a, b, 'upper', False))                     # kể cả thanh xiên đầu dàn
        for k in range(1, NPANEL):
            E.append((f'U{side}{k}', f'L{side}{k}', 'vertical', True))
        for k in range(1, NPANEL // 2):                           # thanh xiên dốc về giữa nhịp
            E.append((f'U{side}{k}', f'L{side}{k+1}', 'diagonal', True))
            E.append((f'U{side}{NPANEL-k}', f'L{side}{NPANEL-k-1}', 'diagonal', True))
    for k in range(NPANEL + 1):                                   # dầm ngang
        E += [(f'LA{k}', f'S1{k}', 'transverse', False), (f'S1{k}', f'S2{k}', 'transverse', False),
              (f'S2{k}', f'LB{k}', 'transverse', False)]
    for s in ('S1', 'S2'):                                        # dầm dọc
        for k in range(NPANEL):
            E.append((f'{s}{k}', f'{s}{k+1}', 'stringer', False))
    for k in range(NPANEL):                                       # liên kết gió dưới (chữ X)
        E += [(f'LA{k}', f'LB{k+1}', 'lower_brace', False), (f'LB{k}', f'LA{k+1}', 'lower_brace', False)]
    for k in range(1, NPANEL):                                    # thanh chống ngang trên tại mọi nút cánh trên
        E.append((f'UA{k}', f'UB{k}', 'strut', False))
    for k in range(1, NPANEL - 1):                                # liên kết gió trên (chữ X) giữa các nút cánh trên
        E += [(f'UA{k}', f'UB{k+1}', 'upper_brace', False), (f'UB{k}', f'UA{k+1}', 'upper_brace', False)]
    return np.array(nodes), tag, E

def frame_element(xi, xj, A, Iz, Iy, J, E, G, rho, extra_m=0.0):
    """Ma trận độ cứng và khối lượng nhất quán 12x12 trong hệ tổng thể."""
    d = xj - xi; L = np.linalg.norm(d); ex = d / L
    ref = np.array([0.0, 0.0, 1.0]) if abs(ex[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    if abs(ex[1]) > 0.9:                                         # thanh ngang cầu: trục y cục bộ theo X tổng thể
        ref = np.array([0.0, 0.0, 1.0])
    ey = np.cross(ref, ex); ey /= np.linalg.norm(ey)
    if abs(ex[1]) > 0.9:
        ey = np.array([1.0, 0.0, 0.0]) - ex * ex[0]; ey /= np.linalg.norm(ey)
    ez = np.cross(ex, ey)
    R = np.vstack([ex, ey, ez])
    # uốn trong mặt phẳng x-z cục bộ dùng I quanh trục y cục bộ (Iy, trục mạnh), x-y dùng Iz
    k = np.zeros((12, 12))
    EA, GJ = E * A / L, G * J / L
    k[0, 0] = k[6, 6] = EA; k[0, 6] = k[6, 0] = -EA
    k[3, 3] = k[9, 9] = GJ; k[3, 9] = k[9, 3] = -GJ
    def bend(I, i1, i2, sgn):
        c = E * I / L**3
        idx = [i1, i2, i1 + 6, i2 + 6]
        kb = c * np.array([[12, sgn * 6 * L, -12, sgn * 6 * L],
                           [sgn * 6 * L, 4 * L**2, -sgn * 6 * L, 2 * L**2],
                           [-12, -sgn * 6 * L, 12, -sgn * 6 * L],
                           [sgn * 6 * L, 2 * L**2, -sgn * 6 * L, 4 * L**2]])
        for a in range(4):
            for b in range(4):
                k[idx[a], idx[b]] += kb[a, b]
    bend(Iz, 1, 5, +1)       # v, theta_z
    bend(Iy, 2, 4, -1)       # w, theta_y
    mbar = rho * A + extra_m
    mm = np.zeros((12, 12))
    mm[0, 0] = mm[6, 6] = mbar * L / 3; mm[0, 6] = mm[6, 0] = mbar * L / 6
    Jp = rho * (Iy + Iz)
    mm[3, 3] = mm[9, 9] = Jp * L / 3; mm[3, 9] = mm[9, 3] = Jp * L / 6
    def bmass(i1, i2, sgn):
        c = mbar * L / 420
        idx = [i1, i2, i1 + 6, i2 + 6]
        mb = c * np.array([[156, sgn * 22 * L, 54, -sgn * 13 * L],
                           [sgn * 22 * L, 4 * L**2, sgn * 13 * L, -3 * L**2],
                           [54, sgn * 13 * L, 156, -sgn * 22 * L],
                           [-sgn * 13 * L, -3 * L**2, -sgn * 22 * L, 4 * L**2]])
        for a in range(4):
            for b in range(4):
                mm[idx[a], idx[b]] += mb[a, b]
    bmass(1, 5, +1); bmass(2, 4, -1)
    T = np.kron(np.eye(4), R)
    return T.T @ k @ T, T.T @ mm @ T

class NamO:
    def __init__(self):
        self.X, self.tag, self.E = geometry()
        # nút phụ cho lò xo xoay ở hai đầu thanh đứng và thanh xiên
        self.nodes = [tuple(p) for p in self.X]
        self.elems, self.springs = [], []
        for a, b, grp, semi in self.E:
            ia, ib = self.tag[a], self.tag[b]
            if semi:
                ja = len(self.nodes); self.nodes.append(self.nodes[ia])
                jb = len(self.nodes); self.nodes.append(self.nodes[ib])
                self.springs += [(ia, ja), (ib, jb)]
                ia, ib = ja, jb
            self.elems.append((ia, ib, grp))
        self.nodes = np.array(self.nodes)
        self.ndof = 6 * len(self.nodes)
        self.bearings = {'LA0': 'rocker', 'LB0': 'rocker', f'LA{NPANEL}': 'pin', f'LB{NPANEL}': 'pin'}

    def matrices(self, E, k_rot, k_v, k_h):
        n = self.ndof
        K, M = np.zeros((n, n)), np.zeros((n, n))
        G = E / (2 * 1.3)
        for ia, ib, grp in self.elems:
            A, Iz, Iy = SEC[grp]
            em = M_NS if grp == 'lower' else 0.0
            ke, me = frame_element(self.nodes[ia], self.nodes[ib], A, Iz, Iy, J_FACTOR * (Iy + Iz), E, G, RHO, em)
            dofs = np.r_[6 * ia:6 * ia + 6, 6 * ib:6 * ib + 6]
            K[np.ix_(dofs, dofs)] += ke; M[np.ix_(dofs, dofs)] += me
        big = 1e13
        for i, j in self.springs:                     # tịnh tiến liên kết cứng, xoay qua lò xo k_rot
            for c in range(6):
                kk = big if c < 3 else k_rot
                a, b = 6 * i + c, 6 * j + c
                K[a, a] += kk; K[b, b] += kk; K[a, b] -= kk; K[b, a] -= kk
        for name, kind in self.bearings.items():     # gối: lò xo đứng k_v, ngang cầu cứng, dọc: cứng (gối cố định) / k_h (gối di động)
            i = self.tag[name]
            K[6 * i + 2, 6 * i + 2] += k_v
            K[6 * i + 1, 6 * i + 1] += big
            K[6 * i + 0, 6 * i + 0] += big if kind == 'pin' else k_h
        return K, M

    def modes(self, E=None, k_rot=None, k_v=None, k_h=None, nmodes=30):
        p = dict(NOMINAL); p.update({k: v for k, v in dict(E=E, k_rot=k_rot, k_v=k_v, k_h=k_h).items() if v is not None})
        K, M = self.matrices(**p)
        # khử bậc tự do xoay quanh trục thanh vô định ở nút phụ: thêm độ cứng rất nhỏ để ma trận xác định
        K += np.eye(self.ndof) * 1e-3
        w2, V = eigh(K, M, subset_by_index=[0, nmodes - 1])
        self.M_last = M
        return np.sqrt(np.abs(w2)) / (2 * np.pi), V

    def classify(self, V, M=None, cutoff=0.5):
        """Phân loại dạng tổng thể: L (ngang), V (uốn đứng), T (xoắn); dạng cục bộ (X) khi các nút
        cánh giàn chiếm < cutoff phần động năng của dạng."""
        out, count = [], {'L': 0, 'V': 0, 'T': 0, 'X': 0}
        chord = np.array([self.tag[n] for n in self.tag if n[0] in 'LU'])
        cd = np.r_[6 * chord, 6 * chord + 1, 6 * chord + 2]
        lo = {s: [self.tag[f'L{s}{k}'] for k in range(1, NPANEL)] for s in 'AB'}
        up = {s: [self.tag[f'U{s}{k}'] for k in range(1, NPANEL)] for s in 'AB'}
        for i in range(V.shape[1]):
            v = V[:, i]
            uy = lambda ids: v[6 * np.array(ids) + 1]
            uz = lambda ids: v[6 * np.array(ids) + 2]
            zA, zB = uz(lo['A']), uz(lo['B'])
            yL = (uy(lo['A']) + uy(lo['B'])) / 2; yU = (uy(up['A']) + uy(up['B'])) / 2
            vert_sym = np.linalg.norm(zA + zB) / 2
            vert_anti = np.linalg.norm(zA - zB) / 2
            lat_same = np.linalg.norm(yL + yU) / 2
            lat_opp = np.linalg.norm(yL - yU) / 2
            scores = {'V': vert_sym, 'L': lat_same, 'T': vert_anti + lat_opp}
            kind = max(scores, key=scores.get)
            if M is not None:
                tr = np.zeros(self.ndof, bool); tr[np.r_[0:self.ndof:6, 1:self.ndof:6, 2:self.ndof:6]] = True
                e_all = v[tr] @ (M[np.ix_(tr, tr)] @ v[tr])
                sel = np.zeros(self.ndof, bool); sel[cd] = True
                e_ch = v[sel] @ (M[np.ix_(sel, sel)] @ v[sel])
                if e_ch / e_all < cutoff:
                    kind = 'X'

            count[kind] += 1
            out.append(f'{kind}{count[kind]}')
        return out

    def paired(self, f, labels):
        """Ghép tần số tính toán với 5 dạng đo theo loại và bậc."""
        lookup = dict(zip(labels, f))
        return np.array([lookup.get(t, np.nan) for t in MEASURED_TYPE])

if __name__ == '__main__':
    import time
    mdl = NamO()
    print(f'{len(mdl.nodes)} nút ({len(mdl.X)} nút hình học), {len(mdl.elems)} phần tử, {len(mdl.springs)} lò xo xoay, {mdl.ndof} bậc tự do')
    t0 = time.time(); f, V = mdl.modes(); t1 = time.time()
    lab = mdl.classify(V, mdl.M_last)
    for i, (fi, li) in enumerate(zip(f, lab)):
        print(f'  dạng {i+1:2d}: {fi:6.3f} Hz  {li}')
    fp = mdl.paired(f, lab)
    print('ghép với đo:', np.round(fp, 3), ' sai số %:', np.round(100 * (fp - MEASURED) / MEASURED, 1), f'({t1-t0:.2f} s)')
    tot_mass = sum(RHO * SEC[g][0] * np.linalg.norm(mdl.nodes[a] - mdl.nodes[b]) + (M_NS * np.linalg.norm(mdl.nodes[a] - mdl.nodes[b]) if g == 'lower' else 0) for a, b, g in mdl.elems)
    print(f'khối lượng nhịp: {tot_mass/1e3:.1f} t')
