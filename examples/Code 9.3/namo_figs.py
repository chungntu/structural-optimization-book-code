"""Code 9.3 (phần vẽ hình): Hình 9.9 - 9.12 và số liệu độ nhạy."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import namo as N
from namo_update import frequencies, MDL

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10, 'mathtext.fontset': 'dejavuserif',
                     'axes.grid': True, 'grid.alpha': 0.3, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})
comma = FuncFormatter(lambda v, p: f'{v:g}'.replace('.', ','))
r = json.load(open('namo_results.json'))
COL = {'upper': 'C0', 'lower': 'C0', 'vertical': 'C2', 'diagonal': 'C2', 'stringer': 'C1', 'transverse': 'C1',
       'strut': 'C4', 'upper_brace': 'C4', 'lower_brace': 'C3'}

def squeeze_white(path, keep=40, tol=250):
    """Thu gọn các dải hàng/cột trắng (do khung 3D của matplotlib) xuống còn `keep` điểm ảnh."""
    from PIL import Image
    im = Image.open(path).convert('RGB'); a = np.asarray(im)
    def bands(white):
        sel, run = [], 0
        for i, w in enumerate(white):
            run = run + 1 if w else 0
            if not w or run <= keep:
                sel.append(i)
        return np.array(sel)
    dark = (a < tol).any(axis=2)
    a = a[bands(~dark.any(axis=1))]
    dark = (a < tol).any(axis=2)
    a = a[:, bands(~dark.any(axis=0))]
    Image.fromarray(a).save(path, dpi=(300, 300))

def draw(ax, disp=None, scale=0.0, lw=1.0):
    X = MDL.nodes.copy()
    if disp is not None:
        X = X + scale * disp
    for ia, ib, g in MDL.elems:
        ax.plot(*zip(X[ia], X[ib]), color=COL[g] if disp is None else 'C0', lw=lw)

# ---------------- Hình 9.9: mô hình phần tử hữu hạn
fig = plt.figure(figsize=(7.6, 4.0)); ax = fig.add_subplot(projection='3d')
draw(ax)
for name in MDL.bearings:
    p = MDL.nodes[MDL.tag[name]]; ax.scatter(*p, color='k', marker='^', s=30)
ax.set_box_aspect((75, 5 * 2.2, 13 * 1.6)); ax.view_init(elev=22, azim=-62)
ax.set_xlabel('x (m)', labelpad=16); ax.set_ylabel('y (m)', labelpad=2); ax.set_zlabel('z (m)', labelpad=2)
ax.set_xticks([0, 18.75, 37.5, 56.25, 75]); ax.set_yticks([-2.5, 2.5]); ax.set_zticks([0, 6.5, 13])
for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
    pane.set_alpha(0.0)
for a in (ax.xaxis, ax.yaxis, ax.zaxis):
    a.set_major_formatter(comma)
from matplotlib.lines import Line2D
leg = [Line2D([], [], color=c, label=t) for c, t in (('C0', 'thanh biên trên, dưới'), ('C2', 'thanh đứng, thanh xiên'),
                                                     ('C1', 'dầm dọc, dầm ngang'), ('C4', 'liên kết trên, thanh chống'),
                                                     ('C3', 'liên kết dọc dưới'))]
fig.legend(handles=leg, fontsize=8, loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.02))
fig.subplots_adjust(left=0.0, right=1.0, top=1.05, bottom=0.12)
fig.savefig(os.path.join(OUT, 'ch9_namo_model.png')); plt.close(fig)
squeeze_white(os.path.join(OUT, 'ch9_namo_model.png'))

# ---------------- Hình 9.10: độ nhạy tương đối của 5 tần số theo các tham số
base = dict(E=200.0, lk=np.log10(8e7), kv=1.3, kh=1.5, mns=247.2, alb=1.0)   # mô hình tham chiếu: liên kết gần cứng
def freq_of(p):
    th_s = np.array([p['E'], p['lk'], p['mns'], p['alb']])
    f_s = frequencies(th_s, 'sens')
    if p['kv'] != base['kv'] or p['kh'] != base['kh']:
        return frequencies(np.array([p['E'], p['lk'], p['kv'], p['kh']]), 'paper')
    return f_s
f0 = freq_of(base)
labels = {'E': '$E$', 'lk': r'$k_{\theta}$', 'kv': '$k_v$', 'kh': '$k_h$', 'mns': '$m_{ns}$', 'alb': r'$\alpha_{lb}$'}
S = {}
for key in base:
    p1, p2 = dict(base), dict(base)
    if key == 'lk':
        p1[key] -= np.log10(1.1); p2[key] += np.log10(1.1); dlog = 2 * np.log(1.1)
    else:
        p1[key] *= 0.95; p2[key] *= 1.05; dlog = np.log(1.05 / 0.95)
    S[key] = (np.log(freq_of(p2)) - np.log(freq_of(p1))) / dlog
fig, ax = plt.subplots(figsize=(6.6, 3.2))
w = 0.13
for i, key in enumerate(base):
    ax.bar(np.arange(5) + (i - 2.5) * w, S[key], width=w, label=labels[key])
ax.set_xticks(range(5)); ax.set_xticklabels([f'{t}\n{f:.2f} Hz'.replace('.', ',') for t, f in zip(['ngang 1', 'xoắn 1', 'ngang 2', 'uốn đứng 1', 'xoắn 2'], N.MEASURED)])
ax.set_ylabel(r'độ nhạy $\partial \ln f / \partial \ln \theta$'); ax.yaxis.set_major_formatter(comma)
ax.legend(ncol=6, fontsize=8, loc='lower center', bbox_to_anchor=(0.5, 1.0)); ax.axhline(0, color='k', lw=0.6)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_namo_sensitivity.png')); plt.close(fig)

# ---------------- Hình 9.11: tần số trước / sau hiệu chỉnh và hội tụ GA
fig, axs = plt.subplots(1, 2, figsize=(7.4, 3.1), gridspec_kw=dict(width_ratios=[1.5, 1]))
ax = axs[0]
f_meas = np.array(r['measured'])
groups = [('ban đầu', r['paper']['f0'], '0.6'), ('hiệu chỉnh: bộ tham số 1', r['paper']['f_ls'], 'C1'),
          ('hiệu chỉnh: bộ tham số 2', r['sens']['f_ls'], 'C3')]
for i, (lab, f, c) in enumerate(groups):
    ax.bar(np.arange(5) + (i - 1) * 0.25, 100 * (np.array(f) - f_meas) / f_meas, width=0.25, color=c, label=lab)
ax.axhline(0, color='k', lw=0.6)
ax.set_xticks(range(5)); ax.set_xticklabels(['ngang 1', 'xoắn 1', 'ngang 2', 'uốn đứng 1', 'xoắn 2'], fontsize=8)
ax.set_ylabel('sai số tần số (%)'); ax.yaxis.set_major_formatter(comma)
ax.set_ylim(-40, 24); ax.legend(fontsize=7, loc='upper center', ncol=1, framealpha=0.9)   # chú giải ở vùng trống phía trên
ax.set_title('(a)', fontsize=9)
ax = axs[1]
for key, c, lab in (('paper', 'C1', 'bộ 1'), ('sens', 'C3', 'bộ 2')):
    ax.semilogy(r[key]['ga_hist'], color=c, label=f'GA, {lab}')
    ax.axhline(r[key]['J_ls'], color=c, ls='--', lw=0.8)
ax.set_xlabel('thế hệ'); ax.set_ylabel('hàm mục tiêu $J$'); ax.legend(fontsize=7)
ax.set_title('(b)', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_namo_results.png')); plt.close(fig)

# ---------------- Hình 9.12: năm dạng dao động của mô hình đã hiệu chỉnh (bộ 2)
th = np.array(r['sens']['ls'])
old_m, old_b = N.M_NS, N.SEC['lower_brace']
N.M_NS = th[2]; A, Iz, Iy = old_b; N.SEC['lower_brace'] = (th[3] * A, th[3] * Iz, th[3] * Iy)
f, V = MDL.modes(E=th[0] * 1e9, k_rot=10**th[1])
lab = MDL.classify(V, MDL.M_last)
N.M_NS, N.SEC['lower_brace'] = old_m, old_b
fig = plt.figure(figsize=(7.6, 5.0))
names = {'L1': 'ngang 1', 'T1': 'xoắn 1', 'L2': 'ngang 2', 'V1': 'uốn đứng 1', 'T2': 'xoắn 2'}
for k, t in enumerate(N.MEASURED_TYPE):
    i = lab.index(t)
    U = V[:, i].reshape(-1, 6)[:, :3]
    U = U / np.abs(U[:len(MDL.X)]).max()
    ax = fig.add_subplot(2, 3, k + 1, projection='3d')
    for ia, ib, g in MDL.elems:
        ax.plot(*zip(MDL.nodes[ia], MDL.nodes[ib]), color='0.85', lw=0.4)
    draw(ax, U, 6.0, lw=0.7)
    ax.set_box_aspect((75, 5 * 3.0, 13 * 1.6)); ax.view_init(elev=32, azim=-55); ax.set_axis_off()
    ax.set_title(f'{names[t]}: {f[i]:.2f} Hz (đo {N.MEASURED[k]:.2f} Hz)'.replace('.', ','), fontsize=9)
fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0, wspace=0, hspace=0.05); fig.savefig(os.path.join(OUT, 'ch9_namo_modes.png')); plt.close(fig)
squeeze_white(os.path.join(OUT, 'ch9_namo_modes.png'))
json.dump({k: v.tolist() for k, v in S.items()}, open('namo_sensitivity.json', 'w'), indent=1)
print('namo figures done'); print({k: np.round(v, 3) for k, v in S.items()})
