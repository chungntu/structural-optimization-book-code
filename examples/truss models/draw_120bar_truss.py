import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# --- Dữ liệu giàn 120 thanh (dome 3D) - SI ---
# Generate node coordinates parametrically
nodes = {}

# Level 1 (apex): R=0, z=7.0 m
nodes[1] = (0, 0, 7.0)

# Level 2: 12 nodes at R=7.0 m, z=5.0 m
R2, z2 = 7.0, 5.0
for i in range(12):
    ang = np.radians(i * 30)
    nodes[2 + i] = (R2*np.cos(ang), R2*np.sin(ang), z2)

# Level 3: 24 nodes at R=12.5 m, z=3.0 m
R3, z3 = 12.5, 3.0
for i in range(24):
    ang = np.radians(i * 15)
    nodes[14 + i] = (R3*np.cos(ang), R3*np.sin(ang), z3)

# Level 4: 12 nodes at R=16.0 m, z=0 (supports)
R4, z4 = 16.0, 0
for i in range(12):
    ang = np.radians(i * 30)
    nodes[38 + i] = (R4*np.cos(ang), R4*np.sin(ang), z4)

# Bar connections
bars = [
    (1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12),(1,13),
    (2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11),(11,12),(12,13),(13,2),
    (2,14),(3,16),(4,18),(5,20),(6,22),(7,24),(8,26),(9,28),(10,30),(11,32),(12,34),(13,36),
    (2,15),(3,15),(3,17),(4,17),(4,19),(5,19),(5,21),(6,21),(6,23),(7,23),(7,25),(8,25),
    (8,27),(9,27),(9,29),(10,29),(10,31),(11,31),(11,33),(12,33),(12,35),(13,35),(13,37),(2,37),
    (14,15),(15,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),(22,23),(23,24),
    (24,25),(25,26),(26,27),(27,28),(28,29),(29,30),(30,31),(31,32),(32,33),(33,34),
    (34,35),(35,36),(36,37),(37,14),
    (14,38),(16,39),(18,40),(20,41),(22,42),(24,43),(26,44),(28,45),(30,46),(32,47),(34,48),(36,49),
    (15,38),(15,39),(17,39),(17,40),(19,40),(19,41),(21,41),(21,42),(23,42),(23,43),
    (25,43),(25,44),(27,44),(27,45),(29,45),(29,46),(31,46),(31,47),(33,47),(33,48),
    (35,48),(35,49),(37,49),(37,38),
]

fixed_nodes = list(range(38, 50))

# --- Vẽ hình 3D ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Vẽ thanh
for n1, n2 in bars:
    x = [nodes[n1][0], nodes[n2][0]]
    y = [nodes[n1][1], nodes[n2][1]]
    z = [nodes[n1][2], nodes[n2][2]]
    ax.plot(x, y, z, 'b-', linewidth=0.8, zorder=2)

# Vẽ nút
for nid, (x, y, z) in nodes.items():
    if nid in fixed_nodes:
        ax.scatter(x, y, z, c='green', s=50, marker='^', zorder=4, depthshade=False)
    elif nid == 1:
        ax.scatter(x, y, z, c='red', s=60, marker='o', zorder=4, depthshade=False)
    else:
        ax.scatter(x, y, z, c='black', s=15, marker='o', zorder=4, depthshade=False)

ax.set_xlabel('X (m)', fontsize=11)
ax.set_ylabel('Y (m)', fontsize=11)
ax.set_zlabel('Z (m)', fontsize=11)

# Lực tại đỉnh (nút 1)
ax.quiver(0, 0, 7.0, 0, 0, -1.5, color='red', arrow_length_ratio=0.3,
          linewidth=2.5, zorder=5)
ax.text(0.3, 0.3, 7.8, 'P', fontsize=12, fontweight='bold', color='red')

ax.view_init(elev=25, azim=135)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\120bar_truss.png', dpi=200, bbox_inches='tight')
print("Đã lưu hình: 120bar_truss.png")
