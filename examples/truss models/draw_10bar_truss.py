import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Dữ liệu giàn 10 thanh (TrussData_10bar) ---
L = 10  # m

# Tọa độ nút (x, y)
nodes = {
    1: (2*L, 1*L),
    2: (2*L, 0*L),
    3: (1*L, 1*L),
    4: (1*L, 0*L),
    5: (0*L, 1*L),
    6: (0*L, 0*L),
}

# Kết nối các thanh
bars = [
    (5, 3), (3, 1), (6, 4), (4, 2),
    (4, 3), (2, 1), (5, 4), (6, 3),
    (3, 2), (4, 1),
]

# Tải trọng: 500 kN hướng xuống tại nút 1 và 2
load_nodes = {2: 500, 4: 500}  # kN

# --- Vẽ hình ---
fig, ax = plt.subplots(1, 1, figsize=(14, 8))

# Vẽ các thanh
for idx, (n1, n2) in enumerate(bars):
    x1, y1 = nodes[n1]
    x2, y2 = nodes[n2]
    ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2, zorder=2)
    # Số thanh tại giữa
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    nx, ny = -dy / length, dx / length
    ax.text(mx + nx * 0.6, my + ny * 0.6, str(idx + 1),
            fontsize=9, ha='center', va='center', color='blue',
            fontweight='bold', zorder=6,
            bbox=dict(boxstyle='round,pad=0.15', facecolor='lightyellow',
                      edgecolor='blue', alpha=0.9))

# Vẽ các nút
for nid, (x, y) in nodes.items():
    ax.plot(x, y, 'ko', markersize=8, zorder=4)
    label_y = y + 0.7 if y > 0 else y - 0.7
    va = 'bottom' if y > 0 else 'top'
    ax.text(x, label_y, str(nid), fontsize=11, ha='center', va=va,
            fontweight='bold', zorder=5)

# --- Vẽ gối cố định ---
def draw_fixed_support(ax, x, y, size=0.8, direction='left'):
    s = size
    triangle = plt.Polygon(
        [(x, y), (x - s*0.7, y - s/2), (x - s*0.7, y + s/2)],
        closed=True, fill=False, edgecolor='green', linewidth=2, zorder=3)
    ax.add_patch(triangle)
    ax.plot([x - s*0.7, x - s*0.7], [y - s*0.7, y + s*0.7],
            'g-', linewidth=2, zorder=3)
    for i in range(5):
        yi = y - s*0.7 + i * (2*s*0.7) / 4
        ax.plot([x - s*0.7, x - s*0.7 - s*0.2], [yi, yi - s*0.15],
                'g-', linewidth=1.5, zorder=3)

draw_fixed_support(ax, *nodes[5], size=1.0, direction='left')
draw_fixed_support(ax, *nodes[6], size=1.0, direction='left')

# --- Vẽ lực tập trung (mũi tên xuống) ---
arrow_len = 2.5
for nid, force in load_nodes.items():
    x, y = nodes[nid]
    ax.annotate('', xy=(x, y), xytext=(x, y + arrow_len),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.5,
                                mutation_scale=18), zorder=5)
    ax.text(x, y + arrow_len + 0.3, f'{force} kN',
            fontsize=11, fontweight='bold', color='red',
            ha='center', va='bottom', zorder=5)

# --- Vẽ kích thước ---
dim_color = 'black'
dim_fontsize = 12

def draw_dimension_h(ax, x1, x2, y, label, offset=-2.0):
    yo = y + offset
    ax.plot([x1, x1], [y - 0.3, yo - 0.3], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.plot([x2, x2], [y - 0.3, yo - 0.3], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.annotate('', xy=(x1, yo), xytext=(x2, yo),
                arrowprops=dict(arrowstyle='<->', color=dim_color, lw=1.5))
    ax.text((x1 + x2) / 2, yo - 0.5, label,
            fontsize=dim_fontsize, ha='center', va='top', color=dim_color,
            fontweight='bold')

def draw_dimension_v(ax, x, y1, y2, label, offset=2.5):
    xo = x + offset
    ax.plot([x + 0.3, xo + 0.3], [y1, y1], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.plot([x + 0.3, xo + 0.3], [y2, y2], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.annotate('', xy=(xo, y1), xytext=(xo, y2),
                arrowprops=dict(arrowstyle='<->', color=dim_color, lw=1.5))
    ax.text(xo + 0.5, (y1 + y2) / 2, label,
            fontsize=dim_fontsize, ha='left', va='center', color=dim_color,
            fontweight='bold', rotation=90)

# Kích thước ngang (2 nhịp, mỗi nhịp 10 m)
draw_dimension_h(ax, nodes[6][0], nodes[4][0], 0, '10 m', offset=-2.2)
draw_dimension_h(ax, nodes[4][0], nodes[2][0], 0, '10 m', offset=-2.2)

# Kích thước đứng (chiều cao 10 m)
draw_dimension_v(ax, nodes[2][0], nodes[2][1], nodes[1][1], '10 m', offset=2.0)

# Thiết lập trục
ax.set_xlim(-3.5, 2*L + 4)
ax.set_ylim(-5, L + 5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\10bar_truss.png', dpi=200, bbox_inches='tight')
print("Đã lưu hình: 10bar_truss.png")
