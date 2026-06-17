import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Dữ liệu giàn 17 thanh (TrussData_17bar - SI) ---
S = 2.5  # m

# Tọa độ nút (x, y) - 9 nút
nodes = {
    1: (0*S, 0*S),
    2: (0*S, 1*S),
    3: (1*S, 0*S),
    4: (1*S, 1*S),
    5: (2*S, 0*S),
    6: (2*S, 1*S),
    7: (3*S, 0*S),
    8: (3*S, 1*S),
    9: (4*S, 0*S),
}

# Kết nối các thanh (17 thanh)
bars = [
    (2, 4), (2, 3), (1, 3), (3, 4),
    (4, 6), (4, 5), (3, 5), (5, 6),
    (6, 8), (6, 7), (5, 7), (7, 8),
    (8, 9), (7, 9), (1, 4), (3, 6), (5, 8),
]

# Tải trọng: 500 kN hướng xuống tại nút 9
loads = {9: (0, -500)}

# --- Vẽ hình ---
fig, ax = plt.subplots(1, 1, figsize=(16, 8))

# Vẽ các thanh
for idx, (n1, n2) in enumerate(bars):
    x1, y1 = nodes[n1]
    x2, y2 = nodes[n2]
    ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2, zorder=2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    length = np.sqrt(dx**2 + dy**2)
    nx, ny = -dy / length, dx / length
    ax.text(mx + nx * 0.15, my + ny * 0.15, str(idx + 1),
            fontsize=9, ha='center', va='center', color='blue',
            fontweight='bold', zorder=6,
            bbox=dict(boxstyle='round,pad=0.15', facecolor='lightyellow',
                      edgecolor='blue', alpha=0.9))

# Vẽ các nút
for nid, (x, y) in nodes.items():
    ax.plot(x, y, 'ko', markersize=8, zorder=4)
    if nid in [1, 3, 5, 7, 9]:  # nút dưới
        ax.text(x, y - 0.2, str(nid), fontsize=11, ha='center', va='top',
                fontweight='bold', zorder=5)
    else:  # nút trên
        ax.text(x, y + 0.15, str(nid), fontsize=11, ha='center', va='bottom',
                fontweight='bold', zorder=5)

# --- Vẽ gối cố định ---
def draw_fixed_support(ax, x, y, size=0.2, direction='left'):
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

draw_fixed_support(ax, *nodes[1], size=0.25, direction='left')
draw_fixed_support(ax, *nodes[2], size=0.25, direction='left')

# --- Vẽ lực tác dụng (mũi tên xuống tại nút 9) ---
arrow_len = 0.8
for nid, (fx, fy) in loads.items():
    x, y = nodes[nid]
    ax.annotate('', xy=(x, y), xytext=(x, y + arrow_len + 0.1),
                arrowprops=dict(arrowstyle='->', color='red', lw=2.5,
                                mutation_scale=18), zorder=5)
    ax.text(x, y + arrow_len + 0.2, f'{abs(fy):.0f} kN',
            fontsize=12, fontweight='bold', color='red',
            ha='center', va='bottom', zorder=5)

# --- Vẽ kích thước ---
dim_color = 'black'
dim_fontsize = 12

def draw_dimension_h(ax, x1, x2, y, label, offset=-1.2):
    yo = y + offset
    ax.plot([x1, x1], [y - 0.05, yo - 0.05], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.plot([x2, x2], [y - 0.05, yo - 0.05], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.annotate('', xy=(x1, yo), xytext=(x2, yo),
                arrowprops=dict(arrowstyle='<->', color=dim_color, lw=1.5))
    ax.text((x1 + x2) / 2, yo - 0.12, label,
            fontsize=dim_fontsize, ha='center', va='top', color=dim_color,
            fontweight='bold')

def draw_dimension_v(ax, x, y1, y2, label, offset=0.6):
    xo = x + offset
    ax.plot([x + 0.05, xo + 0.05], [y1, y1], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.plot([x + 0.05, xo + 0.05], [y2, y2], color=dim_color, linewidth=0.8,
            linestyle='--', zorder=1)
    ax.annotate('', xy=(xo, y1), xytext=(xo, y2),
                arrowprops=dict(arrowstyle='<->', color=dim_color, lw=1.5))
    ax.text(xo + 0.1, (y1 + y2) / 2, label,
            fontsize=dim_fontsize, ha='left', va='center', color=dim_color,
            fontweight='bold', rotation=90)

# Kích thước ngang: 4 nhịp × 2.5 m
draw_dimension_h(ax, nodes[1][0], nodes[3][0], 0, '2.5 m', offset=-1.2)
draw_dimension_h(ax, nodes[3][0], nodes[5][0], 0, '2.5 m', offset=-1.2)
draw_dimension_h(ax, nodes[5][0], nodes[7][0], 0, '2.5 m', offset=-1.2)
draw_dimension_h(ax, nodes[7][0], nodes[9][0], 0, '2.5 m', offset=-1.2)

# Kích thước đứng
draw_dimension_v(ax, nodes[9][0], nodes[9][1], nodes[8][1], '2.5 m', offset=0.6)

ax.set_xlim(-0.8, 4*S + 1.2)
ax.set_ylim(-2.2, S + 0.8)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\17bar_truss.png', dpi=200, bbox_inches='tight')
print("Đã lưu hình: 17bar_truss.png")
