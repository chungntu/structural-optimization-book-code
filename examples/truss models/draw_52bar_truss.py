import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# --- 52-Bar Truss Topology ---
cos45 = np.cos(np.pi/4)

# Shape variables (nominal initial values for visualization)
ZA = 6.0   
XB = 2.0   
ZB = 5.0   
XF = 4.0   
ZF = 3.0   
R_base = 6.0  

# Translate MATLAB dnkoor logic to Python dictionary
nodes = {
    1:  (0, 0, ZA),
    2:  (XB, 0, ZB),
    3:  (0, XB, ZB),
    4:  (-XB, 0, ZB),
    5:  (0, -XB, ZB),
    6:  (XF, 0, ZF),
    7:  (XF*cos45, XF*cos45, ZF),
    8:  (0, XF, ZF),
    9:  (-XF*cos45, XF*cos45, ZF),
    10: (-XF, 0, ZF),
    11: (-XF*cos45, -XF*cos45, ZF),
    12: (0, -XF, ZF),
    13: (XF*cos45, -XF*cos45, ZF),
    14: (R_base, 0, 0),
    15: (R_base*cos45, R_base*cos45, 0),
    16: (0, R_base, 0),
    17: (-R_base*cos45, R_base*cos45, 0),
    18: (-R_base, 0, 0),
    19: (-R_base*cos45, -R_base*cos45, 0),
    20: (0, -R_base, 0),
    21: (R_base*cos45, -R_base*cos45, 0),
}

# Translate MATLAB eldn logic (52 bars)
bars = [
    (1,4), (1,5), (1,2), (1,3),
    (4,10), (5,12), (2,6), (3,8),
    (4,11), (11,5), (5,13), (2,13), (2,7), (3,7), (3,9), (4,9),
    (4,5), (5,2), (2,3), (3,4),
    (10,11), (11,12), (12,13), (13,6), (6,7), (7,8), (8,9), (9,10),
    (10,18), (11,19), (12,20), (13,21), (6,14), (7,15), (8,16), (9,17),
    (10,19), (12,19), (12,21), (6,21), (6,15), (8,15), (8,17), (10,17),
    (11,18), (11,20), (13,20), (13,14), (7,14), (7,16), (9,16), (9,18)
]

mass_nodes = list(range(1, 14))    
fixed_nodes = list(range(14, 22))  

# --- 3D Plotting ---
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# Draw bars
for n1, n2 in bars:
    x = [nodes[n1][0], nodes[n2][0]]
    y = [nodes[n1][1], nodes[n2][1]]
    z = [nodes[n1][2], nodes[n2][2]]
    ax.plot(x, y, z, 'b-', linewidth=1.5, zorder=2)

# Draw nodes
for nid, (x, y, z) in nodes.items():
    if nid in fixed_nodes:
        ax.scatter(x, y, z, c='forestgreen', s=120, marker='^', zorder=4, depthshade=False, label='Fixed Supports' if nid==14 else "")
    else:
        ax.scatter(x, y, z, c='k', s=40, marker='o', zorder=4, depthshade=False)

# Draw Added Mass (Downward triangles or arrows)
for nid in mass_nodes:
    x, y, z_pos = nodes[nid]
    ax.scatter(x, y, z_pos, c='red', s=60, marker='v', zorder=5, depthshade=False, label='50 kg Added Mass' if nid==1 else "")

# Visual Helper Rings (dashed lines)
# Upper Ring
ring_b = [2, 3, 4, 5, 2]
xb = [nodes[n][0] for n in ring_b]
yb = [nodes[n][1] for n in ring_b]
zb = [nodes[n][2] for n in ring_b]
ax.plot(xb, yb, zb, 'purple', linestyle='--', linewidth=0.8, alpha=0.5)

# Middle Ring
ring_f = [6, 7, 8, 9, 10, 11, 12, 13, 6]
xf = [nodes[n][0] for n in ring_f]
yf = [nodes[n][1] for n in ring_f]
zf = [nodes[n][2] for n in ring_f]
ax.plot(xf, yf, zf, 'purple', linestyle='--', linewidth=0.8, alpha=0.5)

# Bottom Fixed Base
ring_base = [14, 15, 16, 17, 18, 19, 20, 21, 14]
xbase = [nodes[n][0] for n in ring_base]
ybase = [nodes[n][1] for n in ring_base]
zbase = [nodes[n][2] for n in ring_base]
ax.plot(xbase, ybase, zbase, 'g--', linewidth=0.8, alpha=0.5)

# Annotations for the 5 Shape Variables
def draw_dim_line(ax, p1, p2, text, color='indigo'):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=color, linewidth=1.5, linestyle='-.')
    mid = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2)
    ax.text(mid[0], mid[1], mid[2], text, color=color, fontweight='bold', fontsize=12)

# ZA (Height)
draw_dim_line(ax, (0, 0, 0), (0, 0, ZA), ' ZA ', 'magenta')
# ZB (Upper Ring Height)
draw_dim_line(ax, (XB, 0, 0), (XB, 0, ZB), ' ZB ', 'm')
# ZF (Lower Ring Height)
draw_dim_line(ax, (XF, 0, 0), (XF, 0, ZF), ' ZF ', 'm')

# XB (Upper Radius)
draw_dim_line(ax, (0, 0, ZB), (XB, 0, ZB), ' XB ', 'darkorange')
# XF (Lower Radius)
draw_dim_line(ax, (0, 0, ZF), (XF, 0, ZF), ' XF ', 'darkorange')

# Legend and View Config
ax.legend(loc='upper right', fontsize=11)
ax.set_xlabel('X (m)', fontsize=12)
ax.set_ylabel('Y (m)', fontsize=12)
ax.set_zlabel('Z (m)', fontsize=12)

# Better viewing angle for the dome (rotated to 75 degrees as requested)
ax.view_init(elev=20, azim=50)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\52bar_truss.png', dpi=200, bbox_inches='tight')
print("Modification complete.")
