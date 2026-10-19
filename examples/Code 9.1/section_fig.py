"""Hình 9.1: sơ đồ tiết diện dầm liên hợp và các biến thiết kế (không theo tỷ lệ)."""
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10, 'mathtext.fontset': 'dejavuserif',
                     'savefig.dpi': 300, 'savefig.bbox': 'tight'})
fig, ax = plt.subplots(figsize=(5.8, 4.4))
steel, conc = '#4a6fa5', '#d9d9d9'
bt, tt, bb, tb, tw, D = 1.4, 0.16, 2.0, 0.22, 0.10, 3.2       # kích thước vẽ (đơn vị tùy ý)
hv, ts, bs = 0.35, 0.65, 5.6
y0 = 0.0
ax.add_patch(Rectangle((-bb / 2, y0), bb, tb, fc=steel, ec='k'))
ax.add_patch(Rectangle((-tw / 2, y0 + tb), tw, D, fc=steel, ec='k'))
yt = y0 + tb + D
ax.add_patch(Rectangle((-bt / 2, yt), bt, tt, fc=steel, ec='k'))
ax.add_patch(Polygon([(-bt / 2, yt + tt), (bt / 2, yt + tt), (bt / 2 + hv, yt + tt + hv), (-bt / 2 - hv, yt + tt + hv)],
                     fc=conc, ec='k', lw=0.8))
ys = yt + tt + hv
ax.add_patch(Rectangle((-bs / 2, ys), bs, ts, fc=conc, ec='k'))
for xb in (-bs / 2, bs / 2):                                      # nét cắt hai đầu bản
    ax.plot([xb - 0.08, xb + 0.08], [ys - 0.05, ys + ts + 0.05], color='w', lw=4)
    ax.plot([xb - 0.08, xb + 0.08], [ys - 0.05, ys + ts + 0.05], color='k', lw=0.8)
def dim(p1, p2, txt, toff, **kw):
    ax.annotate('', xy=p1, xytext=p2, arrowprops=dict(arrowstyle='<->', lw=0.8, shrinkA=0, shrinkB=0))
    ax.text((p1[0] + p2[0]) / 2 + toff[0], (p1[1] + p2[1]) / 2 + toff[1], txt, ha='center', va='center', fontsize=11, **kw)
def ext(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='k', lw=0.5)
# kích thước bản cánh trên, bụng, bản cánh dưới
dim((-bt / 2, yt - 0.35), (bt / 2, yt - 0.35), r'$b_{tf}$', (-bt / 2 - 0.25, 0))
ext(-bt / 2, yt, -bt / 2, yt - 0.45); ext(bt / 2, yt, bt / 2, yt - 0.45)
dim((bt / 2 + 0.55, yt), (bt / 2 + 0.55, yt + tt), r'$t_{tf}$', (0.32, 0))
ext(bt / 2, yt, bt / 2 + 0.65, yt); ext(bt / 2, yt + tt, bt / 2 + 0.65, yt + tt)
dim((-1.35, y0 + tb), (-1.35, yt), r'$D$', (-0.25, 0))
ext(-tw / 2, y0 + tb, -1.45, y0 + tb); ext(-tw / 2, yt, -1.45, yt)
ax.annotate(r'$t_w$', xy=(tw / 2, y0 + tb + D * 0.5), xytext=(0.9, y0 + tb + D * 0.5),
            arrowprops=dict(arrowstyle='->', lw=0.8), va='center', fontsize=11)
dim((-bb / 2, y0 - 0.35), (bb / 2, y0 - 0.35), r'$b_{bf}$', (0, -0.22))
ext(-bb / 2, y0, -bb / 2, y0 - 0.45); ext(bb / 2, y0, bb / 2, y0 - 0.45)
dim((bb / 2 + 0.4, y0), (bb / 2 + 0.4, y0 + tb), r'$t_{bf}$', (0.32, 0))
ext(bb / 2, y0, bb / 2 + 0.5, y0); ext(bb / 2, y0 + tb, bb / 2 + 0.5, y0 + tb)
# bản và vút
dim((bs / 2 - 0.35, ys), (bs / 2 - 0.35, ys + ts), r'$t_s$', (-0.3, 0))
dim((-bs / 2 + 0.25, ys - hv), (-bs / 2 + 0.25, ys), r'$h_v$', (0.3, 0))
ext(-bt / 2 - hv, ys - hv, -bs / 2 + 0.15, ys - hv)
dim((-bs / 2, ys + ts + 0.3), (bs / 2, ys + ts + 0.3), r'$b_e$', (0, 0.2))
ax.text(0, ys + ts / 2, 'bản BTCT quy đổi', ha='center', va='center', fontsize=10)
ax.text(1.2, y0 + tb + D * 0.78, 'dầm thép\nchữ I tổ hợp', ha='left', va='center', fontsize=10)
ax.set_xlim(-bs / 2 - 0.3, bs / 2 + 0.3); ax.set_ylim(y0 - 0.8, ys + ts + 0.75)
ax.set_aspect('equal'); ax.axis('off')
fig.savefig(os.path.join(OUT, 'ch9_girder_section.png')); plt.close(fig)
print('section figure done')
