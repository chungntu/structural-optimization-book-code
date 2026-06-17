import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# --- Dữ liệu giàn 25 thanh (3D tower) - SI ---
nodes = {
    1:  (-1.0,   0,     5.0),
    2:  ( 1.0,   0,     5.0),
    3:  (-1.0,   1.0,   2.5),
    4:  ( 1.0,   1.0,   2.5),
    5:  ( 1.0,  -1.0,   2.5),
    6:  (-1.0,  -1.0,   2.5),
    7:  (-2.5,   2.5,   0),
    8:  ( 2.5,   2.5,   0),
    9:  ( 2.5,  -2.5,   0),
    10: (-2.5,  -2.5,   0),
}

bars = [
    (1,2), (1,4), (2,3), (1,5), (2,6), (2,5), (2,4), (1,3), (1,6),
    (3,6), (4,5), (3,4), (5,6),
    (3,10), (6,7), (4,9), (5,8),
    (3,8), (4,7), (6,9), (5,10),
    (3,7), (4,8), (5,9), (6,10),
]

fixed_nodes = [7, 8, 9, 10]

# --- Vẽ hình 3D ---
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Vẽ các thanh
for n1, n2 in bars:
    x = [nodes[n1][0], nodes[n2][0]]
    y = [nodes[n1][1], nodes[n2][1]]
    z = [nodes[n1][2], nodes[n2][2]]
    ax.plot(x, y, z, 'b-', linewidth=1.5, zorder=2)

# Vẽ các nút + nhãn
for nid, (x, y, z) in nodes.items():
    if nid in fixed_nodes:
        ax.scatter(x, y, z, c='green', s=80, marker='^', zorder=4, depthshade=False)
    else:
        ax.scatter(x, y, z, c='black', s=50, marker='o', zorder=4, depthshade=False)
    ax.text(x, y, z + 0.2, str(nid), fontsize=9, fontweight='bold',
            ha='center', va='bottom', zorder=5)

# Kích thước annotations (removed as requested)

ax.set_xlabel('X (m)', fontsize=11)
ax.set_ylabel('Y (m)', fontsize=11)
ax.set_zlabel('Z (m)', fontsize=11)
ax.view_init(elev=10, azim=60)

# Ẩn nền
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\25bar_truss.png', dpi=200, bbox_inches='tight')
print("Đã lưu hình: 25bar_truss.png")
