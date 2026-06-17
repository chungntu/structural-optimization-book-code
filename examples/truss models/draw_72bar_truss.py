import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# --- Dữ liệu giàn 72 thanh (3D, 4 tầng) - SI ---
nodes = {
    1: (0, 0, 0), 2: (3.0, 0, 0), 3: (3.0, 3.0, 0), 4: (0, 3.0, 0),
    5: (0, 0, 1.5), 6: (3.0, 0, 1.5), 7: (3.0, 3.0, 1.5), 8: (0, 3.0, 1.5),
    9: (0, 0, 3.0), 10: (3.0, 0, 3.0), 11: (3.0, 3.0, 3.0), 12: (0, 3.0, 3.0),
    13: (0, 0, 4.5), 14: (3.0, 0, 4.5), 15: (3.0, 3.0, 4.5), 16: (0, 3.0, 4.5),
    17: (0, 0, 6.0), 18: (3.0, 0, 6.0), 19: (3.0, 3.0, 6.0), 20: (0, 3.0, 6.0),
}

bars = [
    (1,5),(2,6),(3,7),(4,8),(2,5),(1,6),(2,7),(3,6),(3,8),(4,7),(1,8),(4,5),
    (5,6),(6,7),(7,8),(8,5),(5,7),(6,8),
    (5,9),(6,10),(7,11),(8,12),(9,6),(5,10),(6,11),(7,10),(7,12),(8,11),(5,12),(8,9),
    (9,10),(10,11),(11,12),(12,9),(9,11),(10,12),
    (9,13),(10,14),(11,15),(12,16),(10,13),(9,14),(10,15),(11,14),(11,16),(12,15),(9,16),(12,13),
    (13,14),(14,15),(15,16),(13,16),(13,15),(14,16),
    (13,17),(14,18),(15,19),(16,20),(14,17),(13,18),(14,19),(15,18),(15,20),(16,19),(13,20),(16,17),
    (17,18),(18,19),(19,20),(20,17),(17,19),(18,20),
]

fixed_nodes = [1, 2, 3, 4]

# --- Vẽ hình 3D ---
fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')

# Vẽ các thanh
for n1, n2 in bars:
    x = [nodes[n1][0], nodes[n2][0]]
    y = [nodes[n1][1], nodes[n2][1]]
    z = [nodes[n1][2], nodes[n2][2]]
    ax.plot(x, y, z, 'b-', linewidth=1.2, zorder=2)

# Vẽ các nút + nhãn
for nid, (x, y, z) in nodes.items():
    if nid in fixed_nodes:
        ax.scatter(x, y, z, c='green', s=80, marker='^', zorder=4, depthshade=False)
    else:
        ax.scatter(x, y, z, c='black', s=30, marker='o', zorder=4, depthshade=False)
    ax.text(x, y, z + 0.15, str(nid), fontsize=8, fontweight='bold',
            ha='center', va='bottom', zorder=5)

ax.set_xlabel('X (m)', fontsize=11)
ax.set_ylabel('Y (m)', fontsize=11)
ax.set_zlabel('Z (m)', fontsize=11)
ax.view_init(elev=20, azim=60)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\72bar_truss.png', dpi=200, bbox_inches='tight')
print("Đã lưu hình: 72bar_truss.png")
