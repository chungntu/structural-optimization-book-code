"""Code 9.1 (phần vẽ hình): Hình 9.2 - 9.3 (Hình 9.1 vẽ bằng section_fig.py)."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import girder as G
from girder_opt import solve_de

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10, 'mathtext.fontset': 'dejavuserif',
                     'axes.grid': True, 'grid.alpha': 0.3, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})
comma = FuncFormatter(lambda v, p: f'{v:g}'.replace('.', ','))
def commas(ax):
    ax.xaxis.set_major_formatter(comma); ax.yaxis.set_major_formatter(comma)

res = json.load(open('girder_results.json'))

# ---------------- Hình 9.2: hội tụ DE (20 lần) và vị trí nghiệm SQP, mô hình A và B
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=False)
from scipy.optimize import differential_evolution
for ax, model, ref in zip(axs, ('A', 'B'), (5399.0, None)):
    for seed in range(20):
        hist = []
        rng = np.random.default_rng(seed)
        init = G.BOUNDS[:, 0] + rng.random((25, 6)) * (G.BOUNDS[:, 1] - G.BOUNDS[:, 0])
        from girder_opt import penalized
        def cb(xk, convergence=None):
            hist.append(penalized(xk, model))
        differential_evolution(penalized, G.BOUNDS, args=(model,), strategy='rand1bin', maxiter=500,
                               mutation=0.7, recombination=0.6, init=init, tol=0, polish=False, seed=seed, callback=cb)
        ax.plot(np.arange(1, len(hist) + 1), hist, color='0.55', lw=0.6)
    ax.axhline(res[model]['sqp_best'], color='C3', lw=1.2, ls='--', label=f'SQP: {res[model]["sqp_best"]:.0f} kg'.replace('.', ','))
    if ref:
        ax.axhline(ref, color='C0', lw=1.0, ls=':', label='nghiệm công bố: 5399 kg')
    ax.set_yscale('log'); ax.set_xlabel('thế hệ'); ax.set_ylabel('khối lượng có phạt (kg)')
    ax.set_title(f'Mô hình {model}', fontsize=10); ax.legend(fontsize=8)
    ax.set_ylim(res[model]['sqp_best'] * 0.97, res[model]['sqp_best'] * 3)
    ax.xaxis.set_major_formatter(comma)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_girder_convergence.png')); plt.close(fig)

# ---------------- Hình 9.3: đường đánh đổi khối lượng - chiều cao bụng dầm (mô hình B)
fr = res['B']['front']
Dm = np.array([f['x'][5] for f in fr]); mm = np.array([f['mass'] for f in fr])
fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.plot(Dm, mm, 'o-', color='C0', ms=4)
ax.plot(G.X_EMP[5], G.mass(G.X_EMP), 's', color='C1', label='thiết kế kinh nghiệm (8173 kg)')
ax.plot(res['B']['sqp_x'][5], res['B']['sqp_best'], '*', color='C3', ms=12, label='nghiệm không khống chế D')
ax.set_xlabel('chiều cao bản bụng $D$ (mm)'); ax.set_ylabel('khối lượng dầm thép (kg)')
ax.legend(fontsize=8); commas(ax)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'ch9_girder_front.png')); plt.close(fig)
print('girder figures done')
