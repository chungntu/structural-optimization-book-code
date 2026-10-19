"""Code 9.2 (phần vẽ hình): Hình 9.4 - 9.8."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import Rectangle, Polygon
import tmd as T

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10, 'mathtext.fontset': 'dejavuserif',
                     'axes.grid': True, 'grid.alpha': 0.3, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})
comma = FuncFormatter(lambda v, p: f'{v:g}'.replace('.', ','))
def commas(ax):
    ax.xaxis.set_major_formatter(comma); ax.yaxis.set_major_formatter(comma)
r = json.load(open('tmd_results.json'))
v = np.array(r['curves']['v']); trains = r['curves']['trains']
A = {k: np.array(a) for k, a in r['curves']['a'].items()}

# ---------------- Hình 9.4: sơ đồ đoàn tàu HSLM-A và mô hình cầu - TMD
fig, axs = plt.subplots(2, 1, figsize=(7.2, 4.0), gridspec_kw=dict(height_ratios=[1, 1.15]))
ax = axs[0]; ax.axis('off')
pos, P = T.hslm_axles('A1')
show = pos[pos <= 100]
for x in show:
    ax.annotate('', xy=(x, 0), xytext=(x, 1.0), arrowprops=dict(arrowstyle='->', lw=0.9))
ax.plot([-2, 102], [0, 0], color='k', lw=0.6)
cars = [(-1.5, 18.5, 'đầu máy'), (19.0, 22.025 + 18, 'toa cuối'), (22.025 + 18, 22.025 + 36, 'toa trung gian'),
        (22.025 + 36, 22.025 + 54, 'toa trung gian'), (22.025 + 54, 22.025 + 72, '...')]
for a, b, name in cars:
    ax.add_patch(Rectangle((a + 0.3, 1.15), b - a - 0.6, 0.9, fc='#e8eef7', ec='k', lw=0.7))
    ax.text((a + b) / 2, 1.6, name, ha='center', va='center', fontsize=8)
for a, b, t, y in ((0, 3, '3', -0.35), (3, 14, '11', -0.35), (14, 17, '3', -0.35), (17, 20.525, '3,525', -1.15),
                   (22.025 + 18 - 1, 22.025 + 18 + 1, 'd', -0.35), (22.025 + 18, 22.025 + 36, 'D', -1.15)):
    ax.annotate('', xy=(a, y), xytext=(b, y), arrowprops=dict(arrowstyle='<->', lw=0.6, shrinkA=0, shrinkB=0))
    ax.text((a + b) / 2, y - 0.12, t, ha='center', va='top', fontsize=8)
for xv in (17, 20.525, 22.025 + 18, 22.025 + 36):
    ax.plot([xv, xv], [0, -1.2], color='k', lw=0.4)
ax.text(101, 0.5, 'P mỗi trục', fontsize=8, va='center')
ax.set_xlim(-3, 112); ax.set_ylim(-1.9, 2.2)
ax.set_title('(a) Đoàn tàu HSLM-A (phần đầu đoàn, đối xứng ở cuối đoàn)', fontsize=9)
ax = axs[1]; ax.axis('off')
ax.add_patch(Rectangle((0, 0), 20, 0.6, fc='#d9d9d9', ec='k'))
ax.add_patch(Polygon([(0, 0), (-0.6, -0.8), (0.6, -0.8)], fc='w', ec='k'))
ax.add_patch(Polygon([(20, 0), (19.4, -0.8), (20.6, -0.8)], fc='w', ec='k'))
for xc in (19.0, 19.6):
    ax.add_patch(plt.Circle((xc, -0.95), 0.12, fc='w', ec='k'))
ax.plot([10, 10], [0, -0.9], color='k', lw=0.8)
zz = np.linspace(-0.9, -1.8, 9); xs = 9.5 + 0.25 * np.array([0, 1, -1, 1, -1, 1, -1, 1, 0])
ax.plot(xs, zz, color='k', lw=0.8); ax.text(9.0, -1.35, r'$k_t$', ha='right', fontsize=10)
ax.plot([10.5, 10.5], [-0.9, -1.25], color='k', lw=0.8); ax.add_patch(Rectangle((10.3, -1.55), 0.4, 0.35, fc='w', ec='k'))
ax.plot([10.5, 10.5], [-1.4, -1.8], color='k', lw=0.8); ax.text(10.9, -1.4, r'$c_t$', fontsize=10)
ax.plot([9.5, 10.5], [-0.9, -0.9], color='k', lw=0.8); ax.plot([9.5, 10.5], [-1.8, -1.8], color='k', lw=0.8)
ax.add_patch(Rectangle((9.2, -2.5), 1.6, 0.7, fc='#4a6fa5', ec='k')); ax.text(10, -2.15, r'$m_t$', color='w', ha='center', va='center', fontsize=10)
for xa in (3.0, 6.0, 14.0, 17.0):
    ax.annotate('', xy=(xa, 0.6), xytext=(xa, 1.4), arrowprops=dict(arrowstyle='->', lw=0.9))
ax.annotate('', xy=(18.5, 1.6), xytext=(14.5, 1.6), arrowprops=dict(arrowstyle='->', lw=0.9)); ax.text(16.5, 1.75, r'$v$', ha='center', fontsize=10)
ax.text(5, 0.3, r'$EI,\ m,\ \zeta$', ha='center', va='center', fontsize=10)
ax.annotate('', xy=(0, -2.9), xytext=(20, -2.9), arrowprops=dict(arrowstyle='<->', lw=0.6)); ax.text(10, -3.05, r'$L$ = 20 m', ha='center', va='top', fontsize=9)
ax.set_xlim(-6, 26); ax.set_ylim(-3.6, 2.1); ax.set_aspect('equal')
ax.set_title('(b) Dầm giản đơn có TMD tại giữa nhịp', fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_tmd_model.png')); plt.close(fig)

# ---------------- Hình 9.5: gia tốc lớn nhất theo vận tốc, không TMD
fig, ax = plt.subplots(figsize=(6.4, 3.4))
for k, name in enumerate(trains):
    ax.plot(v, A['none'][k], lw=0.9, label=f'HSLM-{name}')
ax.axhline(T.A_LIM, color='k', ls='--', lw=1.0); ax.text(152, T.A_LIM + 0.15, 'giới hạn 3,5 m/s²', fontsize=8)
ax.set_xlabel('vận tốc (km/h)'); ax.set_ylabel('gia tốc lớn nhất giữa nhịp (m/s²)')
ax.legend(fontsize=7, ncol=5, loc='upper left'); ax.set_xlim(150, 360); ax.set_ylim(0, 9); commas(ax)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_tmd_notmd.png')); plt.close(fig)

# ---------------- Hình 9.6: bản đồ đẳng trị a_max(gamma, zeta_t), mu = 1%
g = r['mu1']['grid']
Gg, Zg = np.meshgrid(g['gamma'], g['zeta']); Ag = np.array(g['a'])
fig, ax = plt.subplots(figsize=(5.8, 4.0))
cs = ax.contour(Gg, Zg, Ag, levels=[4.4, 4.6, 4.8, 5.0, 5.5, 6.0, 6.5, 7.0], colors='0.3', linewidths=0.8)
ax.clabel(cs, fmt=lambda val: f'{val:.1f}'.replace('.', ','), fontsize=7)
dh, sq = r['mu1']['den_hartog'], r['mu1']['sqp']
ax.plot(*dh, 's', color='C1', ms=7, label=f'Den Hartog: {r["mu1"]["a_dh"]:.2f} m/s²'.replace('.', ','))
ax.plot(*sq, '*', color='C3', ms=13, label=f'SQP: {r["mu1"]["a_sqp"]:.2f} m/s²'.replace('.', ','))
for i, (x, a) in enumerate(zip(r['mu1']['ga'], r['mu1']['a_ga'])):
    ax.plot(*x, 'o', mfc='none', mec='C2', ms=9, label='GA (3 lần chạy)' if i == 0 else None)
ax.set_xlabel(r'tỷ số tần số $\gamma = f_t / f_1$'); ax.set_ylabel(r'tỷ số cản của TMD $\zeta_t$')
ax.legend(fontsize=8, loc='upper right'); commas(ax)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_tmd_contour.png')); plt.close(fig)

# ---------------- Hình 9.7: đường bao gia tốc theo vận tốc: không TMD, Den Hartog, tối ưu
fig, ax = plt.subplots(figsize=(6.4, 3.3))
for key, lab, st in (('none', 'không TMD', '-'), ('dh', 'TMD theo Den Hartog (μ = 1%)', '--'), ('opt', 'TMD tối ưu (μ = 1%)', '-')):
    ax.plot(v, A[key].max(axis=0), st, lw=1.3 if key == 'opt' else 1.0, label=lab)
ax.axhline(T.A_LIM, color='k', ls=':', lw=1.0)
ax.set_xlabel('vận tốc (km/h)'); ax.set_ylabel('bao gia tốc (m/s²)'); ax.set_xlim(150, 360); ax.set_ylim(0, 8.5)
ax.legend(fontsize=8); commas(ax)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_tmd_envelope.png')); plt.close(fig)

# ---------------- Hình 9.8: biên Pareto khối lượng TMD - gia tốc lớn nhất
fr = r['front']
mt = np.array([f['mu'] for f in fr]) * T.M1 / 1e3
ao = np.array([f['a_max'] for f in fr]); ad = np.array([f['a_dh'] for f in fr])
fig, ax = plt.subplots(figsize=(5.8, 3.4))
ax.plot(mt, ao, 'o-', color='C3', label='tham số tối ưu (biên Pareto)')
ax.plot(mt, ad, 's--', color='C1', label='tham số Den Hartog')
ax.axhline(T.A_LIM, color='k', ls=':', lw=1.0); ax.text(0.3, T.A_LIM - 0.25, 'giới hạn 3,5 m/s²', fontsize=8)
ax.set_xlabel('khối lượng TMD $m_t$ (t)'); ax.set_ylabel('gia tốc lớn nhất (m/s²)')
ax.legend(fontsize=8); commas(ax)
ax2 = ax.secondary_xaxis('top', functions=(lambda m: m * 1e3 / T.M1 * 100, lambda p: p / 100 * T.M1 / 1e3))
ax2.set_xlabel('tỷ số khối lượng μ (%)'); ax2.xaxis.set_major_formatter(comma)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_tmd_pareto.png')); plt.close(fig)
print('tmd figures done')
