"""
Code 9.1 - Tối ưu dầm thép chữ I liên hợp nhịp giản đơn theo TCVN 11823:2017.

Bài toán dựng lại theo Hùng và cs. (2021), Tạp chí KHCN Xây dựng NUCE 15(3V):55-68,
ví dụ dầm giữa, cầu nhịp 33 m (nhịp tính toán 32 m). Đơn vị: N, mm, MPa.
Biến thiết kế x = [b_tf, t_tf, b_bf, t_bf, t_w, D] (mm).

Hai mô hình:
  'A' - gần với giả thiết của bài báo: mọi tải trọng do tiết diện liên hợp chịu
        (thi công có chống đỡ), không kể trọng lượng bản thân dầm thép, mỏi với hệ số 0,75;
  'B' - đầy đủ theo trình tự thi công không chống đỡ: dầm thép chịu tĩnh tải giai đoạn 1
        (kể cả trọng lượng bản thân), kiểm toán giai đoạn thi công, mỏi I (hệ số 1,5).
"""
import numpy as np

# ----------------------------------------------------------------------------- số liệu
E, Fy, fc = 2.0e5, 345.0, 30.0       # MPa
N_MOD = 8                            # hệ số quy đổi n (ngắn hạn); dài hạn 3n
BE, TS, HH = 2300.0, 241.6, 98.4     # bản quy đổi (mm); HH: khoảng vút hiệu chỉnh theo Bảng 3 bài báo
L = 32000.0                          # nhịp tính toán (mm)
L_GIRDER = 33000.0                   # chiều dài dầm để tính khối lượng (mm)
RHO = 7.85e-6                        # kg/mm^3
G_ACC = 9.81e-3                      # N/kg tính theo mm: rho*A*G_ACC -> N/mm
DC1_EXT = 13.35 + 1.75 + 0.2         # N/mm: bản + vút; dầm ngang + sườn; chốt + mối nối
DW = 3.62                            # N/mm: lớp phủ mặt đường
DFM, DFV = 0.598, 0.793              # hệ số phân bố mô-men / lực cắt
IM, IM_FAT = 0.33, 0.15
LANE = 9.3                           # N/mm
LB = 4000.0                          # chiều dài không giằng bản cánh trên khi thi công (dầm ngang cách 4 m, giả thiết)
DF_TH = 82.7                         # MPa, ngưỡng mỏi chi tiết loại C'
TRUCK = [(0.0, 35e3), (4300.0, 145e3), (8600.0, 145e3)]
TANDEM = [(0.0, 110e3), (1200.0, 110e3)]
FATIGUE_TRUCK = [(0.0, 35e3), (4300.0, 145e3), (13300.0, 145e3)]
SECTIONS = np.array([0.0, 1/8, 2/8, 3/8, 4/8]) * L          # MC1..MC5
BOUNDS = np.array([[50, 600], [5, 100], [50, 600], [5, 100], [5, 30], [500, 3000]], float)
NAMES = ['b_tf', 't_tf', 'b_bf', 't_bf', 't_w', 'D']
X_EMP = np.array([300, 16, 500, 22, 14, 1125], float)          # thiết kế kinh nghiệm (Hình 1b bài báo)
X_PAPER = np.array([228.64, 10.047, 240.60, 25.173, 9.1245, 1368.60])  # nghiệm công bố (Bảng 4)

MODELS = {
    'A': dict(self_weight=False, staged=False, construction=False, gamma_fat=0.75),
    'B': dict(self_weight=True, staged=True, construction=True, gamma_fat=1.5),
}

# ----------------------------------------------------------------------------- hoạt tải
def _envelope(axles, x, ordinate):
    """Giá trị lớn nhất của đại lượng có đường ảnh hưởng 'ordinate' khi đoàn trục chạy qua."""
    best = 0.0
    for sgn in (1, -1):
        for lead in np.linspace(-20000, L + 20000, 4001):
            val = sum(P * ordinate(lead + sgn * a, x) for a, P in axles if 0 <= lead + sgn * a <= L)
            best = max(best, val)
    return best

_M_IL = lambda p, x: (L - p) * x / L if p >= x else p * (L - x) / L
_V_IL = lambda p, x: (L - p) / L if p > x else (-p / L if p < x else 0.0)
_D_IL = lambda p, x: (p * (L - x) * (L**2 - p**2 - (L - x)**2) / (6 * L) if p <= x
                      else x * (L - p) * (L**2 - x**2 - (L - p)**2) / (6 * L))  # độ võng tại x (nhân 1/EI)

def _live_effects():
    out = []
    for x in SECTIONS:
        Mt = max(_envelope(TRUCK, x, _M_IL), _envelope(TANDEM, x, _M_IL))
        Vt = max(_envelope(TRUCK, x, _V_IL), _envelope(TANDEM, x, _V_IL))
        out.append(dict(M=(1 + IM) * Mt + LANE * x * (L - x) / 2,
                        V=(1 + IM) * Vt + LANE * (L - x)**2 / (2 * L),
                        Mfat=(1 + IM_FAT) * _envelope(FATIGUE_TRUCK, x, _M_IL)))
    dt = (1 + IM) * _envelope(TRUCK, L / 2, _D_IL)
    return out, max(dt, 0.25 * dt + LANE * 5 * L**4 / 384)

LIVE, DEFL_LL = _live_effects()

# ----------------------------------------------------------------------------- tiết diện
def steel_section(x):
    btf, ttf, bbf, tbf, tw, D = x
    parts = [(bbf * tbf, tbf / 2, bbf * tbf**3 / 12),
             (D * tw, tbf + D / 2, tw * D**3 / 12),
             (btf * ttf, tbf + D + ttf / 2, btf * ttf**3 / 12)]
    A = sum(p[0] for p in parts)
    yb = sum(p[0] * p[1] for p in parts) / A
    I = sum(p[2] + p[0] * (p[1] - yb)**2 for p in parts)
    return A, yb, I, tbf + D + ttf

def composite_section(x, nn):
    A, yb, I, d = steel_section(x)
    Ac, yc = BE * TS / nn, d + HH + TS / 2
    yt = (A * yb + Ac * yc) / (A + Ac)
    It = I + A * (yb - yt)**2 + BE * TS**3 / (12 * nn) + Ac * (yc - yt)**2
    return yt, It

def plastic(x):
    """Mô-men dẻo Mp, khoảng cách Dp từ mặt bản đến trục trung hòa dẻo, Dcp (phần bụng chịu nén)."""
    btf, ttf, bbf, tbf, tw, D = x
    Ps = 0.85 * fc * BE * TS
    Pc, Pw, Pt = Fy * btf * ttf, Fy * D * tw, Fy * bbf * tbf
    if Pt + Pw >= Pc + Ps:                          # trục trung hòa dẻo trong bản bụng
        Yb = D / 2 * ((Pt - Pc - Ps) / Pw + 1)
        Mp = (Pw / (2 * D) * (Yb**2 + (D - Yb)**2) + Ps * (Yb + ttf + HH + TS / 2)
              + Pc * (Yb + ttf / 2) + Pt * (D - Yb + tbf / 2))
        return Mp, TS + HH + ttf + Yb, Yb
    if Pt + Pw + Pc >= Ps:                          # trong bản cánh trên
        Yb = ttf / 2 * ((Pw + Pt - Ps) / Pc + 1)
        Mp = (Pc / (2 * ttf) * (Yb**2 + (ttf - Yb)**2) + Ps * (Yb + HH + TS / 2)
              + Pw * (ttf - Yb + D / 2) + Pt * (ttf - Yb + D + tbf / 2))
        return Mp, TS + HH + Yb, 0.0
    Yb = TS * (Pc + Pw + Pt) / Ps                   # trong bản bê tông
    c = TS - Yb + HH
    Mp = Yb**2 * Ps / (2 * TS) + Pc * (c + ttf / 2) + Pw * (c + ttf + D / 2) + Pt * (c + ttf + D + tbf / 2)
    return Mp, Yb, 0.0

def shear_C(D, tw, k):
    r = np.sqrt(E * k / Fy)
    lam = D / tw
    if lam <= 1.12 * r:
        return 1.0
    if lam <= 1.40 * r:
        return 1.12 * r / lam
    return 1.57 / lam**2 * (E * k / Fy)

def construction_capacity(x):
    """Ứng suất danh định bản cánh nén của dầm thép khi thi công (cục bộ + xoắn ngang, Cb = 1)."""
    btf, ttf, bbf, tbf, tw, D = x
    A, yb, I, d = steel_section(x)
    Dc = d - yb - ttf                                # chiều cao bụng chịu nén (đàn hồi)
    lam_f, lam_pf = btf / (2 * ttf), 0.38 * np.sqrt(E / Fy)
    lam_rf = 0.56 * np.sqrt(E / (0.7 * Fy))
    if lam_f <= lam_pf:
        F_flb = Fy
    else:
        F_flb = (1 - 0.3 * (lam_f - lam_pf) / (lam_rf - lam_pf)) * Fy
    rt = btf / np.sqrt(12 * (1 + Dc * tw / (3 * btf * ttf)))
    Lp, Lr = rt * np.sqrt(E / Fy), np.pi * rt * np.sqrt(E / (0.7 * Fy))
    if LB <= Lp:
        F_ltb = Fy
    elif LB <= Lr:
        F_ltb = (1 - 0.3 * (LB - Lp) / (Lr - Lp)) * Fy
    else:
        F_ltb = np.pi**2 * E / (LB / rt)**2
    k_w = 9 / (Dc / D)**2                            # oằn bụng do uốn
    F_crw = min(0.9 * E * k_w / (D / tw)**2, Fy)
    return min(F_flb, F_ltb), F_crw, Dc

# ----------------------------------------------------------------------------- mục tiêu và ràng buộc
def mass(x):
    return RHO * steel_section(x)[0] * L_GIRDER       # kg

def constraints(x, model='B'):
    """Dict {tên: g}; g <= 0 nghĩa là thỏa mãn (các ràng buộc đã chuẩn hóa không thứ nguyên)."""
    opt = MODELS[model]
    btf, ttf, bbf, tbf, tw, D = x
    A, yb, I, d = steel_section(x)
    y8, I8 = composite_section(x, N_MOD)
    y24, I24 = composite_section(x, 3 * N_MOD)
    Mp, Dp, Dcp = plastic(x)
    Dt = TS + HH + d
    wdc = DC1_EXT + (RHO * A * G_ACC if opt['self_weight'] else 0.0)
    # mô-đun chống uốn (thớ trên, thớ dưới) cho tải giai đoạn 1 và giai đoạn 2
    S1t, S1b = ((I / (d - yb), I / yb) if opt['staged'] else (I24 / (d - y24), I24 / y24))
    S2t, S2b = I24 / (d - y24), I24 / y24
    S3t, S3b = I8 / (d - y8), I8 / y8
    g = {}
    # (a) cấu tạo
    g['D/t_w <= 150'] = D / tw / 150 - 1
    g['b_tf/2t_tf <= 12'] = btf / (2 * ttf) / 12 - 1
    g['b_bf/2t_bf <= 12'] = bbf / (2 * tbf) / 12 - 1
    g['b_tf >= D/6'] = D / (6 * btf) - 1
    g['b_bf >= D/6'] = D / (6 * bbf) - 1
    g['t_tf >= 1,1t_w'] = 1.1 * tw / ttf - 1
    g['t_bf >= 1,1t_w'] = 1.1 * tw / tbf - 1
    r = (ttf * btf**3) / (tbf * bbf**3)
    g['I_yc/I_yt >= 0,1'] = 0.1 / r - 1
    g['I_yc/I_yt <= 10'] = r / 10 - 1
    # (b) cường độ CĐ1: uốn tại MC2..MC5, cắt tại MC1..MC5
    compact = 2 * Dcp / tw <= 3.76 * np.sqrt(E / Fy)
    Mn = Mp if Dp <= 0.1 * Dt else Mp * (1.07 - 0.7 * Dp / Dt)
    g['D_p <= 0,42D_t'] = Dp / (0.42 * Dt) - 1
    flex, shear = [], []
    Vp = 0.58 * Fy * D * tw
    for i, (xs, lv) in enumerate(zip(SECTIONS, LIVE)):
        Mdc, Mdw = wdc * xs * (L - xs) / 2, DW * xs * (L - xs) / 2
        Mll = DFM * lv['M']
        if i > 0:
            if compact:
                flex.append((1.25 * Mdc + 1.5 * Mdw + 1.75 * Mll) / Mn - 1)
            else:
                ft = 1.25 * Mdc / S1t + 1.5 * Mdw / S2t + 1.75 * Mll / S3t
                fb = 1.25 * Mdc / S1b + 1.5 * Mdw / S2b + 1.75 * Mll / S3b
                flex.append(max(ft, fb) / Fy - 1)
        Vu = 1.25 * wdc * (L / 2 - xs) + 1.5 * DW * (L / 2 - xs) + 1.75 * DFV * lv['V']
        if i == 0:      # khoang đầu dầm, d0 = 0,5D, không kể trường kéo
            Vn = shear_C(D, tw, 5 + 5 / 0.5**2) * Vp
        else:           # khoang trong, d0 = D, có trường kéo
            C = shear_C(D, tw, 10.0)
            Vn = Vp * (C + 0.87 * (1 - C) / np.sqrt(2.0))
        shear.append(Vu / Vn - 1)
    g['uốn CĐ1'] = max(flex)
    g['cắt CĐ1'] = max(shear)
    # (c) sử dụng SD2 tại giữa nhịp và độ võng hoạt tải
    Mdc, Mdw, Mll = wdc * L**2 / 8, DW * L**2 / 8, 1.3 * DFM * LIVE[-1]['M']
    g['SD2 bản cánh trên'] = (Mdc / S1t + Mdw / S2t + Mll / S3t) / (0.95 * Fy) - 1
    g['SD2 bản cánh dưới'] = (Mdc / S1b + Mdw / S2b + Mll / S3b) / (0.95 * Fy) - 1
    g['độ võng L/800'] = DFM * DEFL_LL / (E * I8) / (L / 800) - 1
    # (d) mỏi tại bản cánh dưới giữa nhịp (một làn: DF/1,2)
    dF = opt['gamma_fat'] * (DFM / 1.2) * LIVE[-1]['Mfat'] / S3b
    g['mỏi bản cánh dưới'] = dF / DF_TH - 1
    # (e) giai đoạn thi công: dầm thép chịu 1,25 x tĩnh tải giai đoạn 1 (kể cả bê tông ướt)
    if opt['construction']:
        Mc = 1.25 * wdc * L**2 / 8
        F_nc, F_crw, Dc = construction_capacity(x)
        g['thi công: bản cánh nén'] = Mc * (d - yb) / I / F_nc - 1
        g['thi công: bản cánh kéo'] = Mc * yb / I / Fy - 1
        g['thi công: oằn bụng'] = Mc * Dc / I / F_crw - 1
    return g

def report(x, model, title):
    gg = constraints(x, model)
    print(f'--- [{model}] {title}: khối lượng = {mass(x):.1f} kg, vi phạm lớn nhất = {max(gg.values()):+.4f}')
    for k, v in gg.items():
        tag = 'HOẠT ĐỘNG' if abs(v) < 5e-3 else ('VI PHẠM' if v > 0 else '')
        print(f'    {k:24s} {v:+.4f} {tag}')

if __name__ == '__main__':
    for m in ('A', 'B'):
        report(X_EMP, m, 'thiết kế kinh nghiệm')
        report(X_PAPER, m, 'nghiệm công bố')
