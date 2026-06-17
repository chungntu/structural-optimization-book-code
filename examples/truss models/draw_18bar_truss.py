import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# --- Dữ liệu giàn 18 thanh trước khi tối ưu ---
# Quy đổi hệ tọa độ sang SI (mét)
d = 6.35  # bay width (m) = 250 in
h = 6.35  # height (m) = 250 in

nodes = {
    1:  (5*d, h),
    2:  (4*d, h),
    3:  (4*d, 0),
    4:  (3*d, h),
    5:  (3*d, 0),
    6:  (2*d, h),
    7:  (2*d, 0),
    8:  (1*d, h),
    9:  (1*d, 0),
    10: (0*d, h),
    11: (0*d, 0),
}

bars = [
    (1,2), (1,3), (2,3), (2,4), (3,4), (3,5), (4,5), (4,6),
    (5,6), (5,7), (6,7), (6,8), (7,8), (7,9), (8,9), (8,10),
    (9,10), (9,11),
]

fixed_nodes = [10, 11]
loads = {
    1: (0, -89000), 
    2: (0, -89000), 
    4: (0, -89000),
    6: (0, -89000), 
    8: (0, -89000)
}

# --- Vẽ hình ---
fig, ax = plt.subplots(1, 1, figsize=(16, 6))

for n1, n2 in bars:
    x1, y1 = nodes[n1]
    x2, y2 = nodes[n2]
    ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2, zorder=2)

for nid, (x, y) in nodes.items():
    ax.plot(x, y, 'ko', markersize=7, zorder=4)

# Gối cố định
def draw_fixed_support(ax, x, y, size=8, direction='right'):
    s = size
    if direction == 'right':
        triangle = plt.Polygon(
            [(x, y), (x + s*0.7, y - s/2), (x + s*0.7, y + s/2)],
            closed=True, fill=False, edgecolor='green', linewidth=2, zorder=3)
        ax.add_patch(triangle)
        ax.plot([x + s*0.7, x + s*0.7], [y - s*0.7, y + s*0.7],
                'g-', linewidth=2, zorder=3)
        n_hash = 5
        for i in range(n_hash):
            yi = y - s*0.7 + i * (2*s*0.7) / (n_hash - 1)
            ax.plot([x + s*0.7, x + s*0.7 + s*0.2], [yi, yi - s*0.15],
                    'g-', linewidth=1.5, zorder=3)
    elif direction == 'down':
        triangle = plt.Polygon(
            [(x, y), (x - s/2, y - s*0.7), (x + s/2, y - s*0.7)],
            closed=True, fill=False, edgecolor='green', linewidth=2, zorder=3)
        ax.add_patch(triangle)
        ax.plot([x - s*0.7, x + s*0.7], [y - s*0.7, y - s*0.7],
                'g-', linewidth=2, zorder=3)
        n_hash = 5
        for i in range(n_hash):
            xi = x - s*0.7 + i * (2*s*0.7) / (n_hash - 1)
            ax.plot([xi, xi - s*0.15], [y - s*0.7, y - s*0.7 - s*0.2],
                    'g-', linewidth=1.5, zorder=3)
    elif direction == 'left':
        triangle = plt.Polygon(
            [(x, y), (x - s*0.7, y - s/2), (x - s*0.7, y + s/2)],
            closed=True, fill=False, edgecolor='green', linewidth=2, zorder=3)
        ax.add_patch(triangle)
        ax.plot([x - s*0.7, x - s*0.7], [y - s*0.7, y + s*0.7],
                'g-', linewidth=2, zorder=3)
        n_hash = 5
        for i in range(n_hash):
            yi = y + s*0.7 - i * (2*s*0.7) / (n_hash - 1)
            ax.plot([x - s*0.7, x - s*0.7 - s*0.2], [yi, yi + s*0.15],
                    'g-', linewidth=1.5, zorder=3)

# Vẽ gối tựa ngàm trái
draw_fixed_support(ax, *nodes[10], size=1.0, direction='left')
draw_fixed_support(ax, *nodes[11], size=1.0, direction='left')

# Lực tác dụng
arrow_len = 3.0
for nid, (fx, fy) in loads.items():
    x, y = nodes[nid]
    if fy < 0:
        ax.annotate('', xy=(x, y), xytext=(x, y + arrow_len),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2.5,
                                    mutation_scale=18), zorder=5)
        ax.text(x, y + arrow_len + 0.3, f'{abs(fy)/1000:.0f} kN',
                fontsize=10, fontweight='bold', color='red',
                ha='center', va='bottom', zorder=5)
    elif fy > 0:
        ax.annotate('', xy=(x, y), xytext=(x, y - arrow_len),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2.5,
                                    mutation_scale=18), zorder=5)
        ax.text(x, y - arrow_len - 0.3, f'{abs(fy)/1000:.0f} kN',
                fontsize=10, fontweight='bold', color='red',
                ha='center', va='top', zorder=5)

# Kích thước
def draw_dimension_h(ax, x1, x2, y, label, offset=-2.5):
    yo = y + offset
    ax.plot([x1, x1], [y - 0.3, yo - 0.3], color='black', linewidth=0.8,
            linestyle='--', zorder=1)
    ax.plot([x2, x2], [y - 0.3, yo - 0.3], color='black', linewidth=0.8,
            linestyle='--', zorder=1)
    ax.annotate('', xy=(x1, yo), xytext=(x2, yo),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text((x1+x2)/2, yo - 0.5, label, fontsize=11, ha='center', va='top',
            fontweight='bold')

def draw_dimension_v(ax, x, y1, y2, label, offset=-3.0):
    xo = x + offset
    ax.plot([x + 0.3, xo + 0.3], [y1, y1], color='black', linewidth=0.8,
            linestyle='--', zorder=1)
    ax.plot([x + 0.3, xo + 0.3], [y2, y2], color='black', linewidth=0.8,
            linestyle='--', zorder=1)
    ax.annotate('', xy=(xo, y1), xytext=(xo, y2),
                arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
    ax.text(xo + 0.5, (y1+y2)/2, label, fontsize=11, ha='left', va='center',
            fontweight='bold', rotation=90)

# Kích thước hệ Mét
for i in range(5):
    draw_dimension_h(ax, i*d, (i+1)*d, y=-1.5, label='6.35 m', offset=-0.5)

draw_dimension_h(ax, 0, 5*d, y=-2.5, label='5 × 6.35 m = 31.75 m', offset=-1.5)
draw_dimension_v(ax, 5*d, 0, h, '6.35 m', offset=3.0)

ax.set_xlim(-2.0, 5*d + 5.0)
ax.set_ylim(-5.0, h + 5.5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\18bar_truss.png', dpi=200, bbox_inches='tight')
print("Đã lưu hình: 18bar_truss.png")
