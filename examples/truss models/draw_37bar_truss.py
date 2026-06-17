import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --- 37-Bar Truss Topology ---
# Bottom chord nodes (y=0): 1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20
# Top chord nodes (variable y): 3, 5, 7, 9, 11, 13, 15, 17, 19
# Symmetric about x=5 (node 11)

# Parabolic shape for visual setup
y3 = 1.0; y5 = 1.4; y7 = 1.7; y9 = 1.9; y11 = 2.0

nodes = {
    1:  (0, 0),
    2:  (1, 0),   3:  (1, y3),
    4:  (2, 0),   5:  (2, y5),
    6:  (3, 0),   7:  (3, y7),
    8:  (4, 0),   9:  (4, y9),
    10: (5, 0),   11: (5, y11),
    12: (6, 0),   13: (6, y9),
    14: (7, 0),   15: (7, y7),
    16: (8, 0),   17: (8, y5),
    18: (9, 0),   19: (9, y3),
    20: (10, 0),
}

# Variable top/web bars (1-27)
bars_top = [
    (1,3),(2,3),(3,4),(3,5),(4,5),(5,6),(5,7),(6,7),
    (7,8),(7,9),(8,9),(9,10),(9,11),(10,11),
    (10,13),(11,13),(12,13),(12,15),(13,15),(14,15),
    (14,17),(15,17),(16,17),(16,19),(17,19),(18,19),(19,20),
]

# Bottom chord bars (28-37) - fixed area A = 40 cm^2
bars_bottom = [
    (1,2),(2,4),(4,6),(6,8),(8,10),(10,12),(12,14),(14,16),(16,18),(18,20),
]

mass_nodes = [2, 4, 6, 8, 10, 12, 14, 16, 18]  # Added mass 10kg at bottom nodes

# --- Drawing ---
fig, ax = plt.subplots(1, 1, figsize=(16, 6))

# Bottom chord (thicker, red to denote fixed)
for n1, n2 in bars_bottom:
    x = [nodes[n1][0], nodes[n2][0]]
    y = [nodes[n1][1], nodes[n2][1]]
    ax.plot(x, y, 'darkred', linewidth=3, zorder=2)

# Top/web structure 
for n1, n2 in bars_top:
    x = [nodes[n1][0], nodes[n2][0]]
    y = [nodes[n1][1], nodes[n2][1]]
    ax.plot(x, y, 'b-', linewidth=1.5, zorder=2)

# Nodes
for nid, (x, y) in nodes.items():
    ax.plot(x, y, 'ko', markersize=6, zorder=4)

# Support Constraints
def draw_pin_support(ax, x, y, size=0.25):
    triangle = plt.Polygon(
        [(x, y), (x - size*0.6, y - size), (x + size*0.6, y - size)],
        closed=True, fill=False, edgecolor='green', linewidth=2, zorder=3
    )
    ax.add_patch(triangle)
    ax.plot([x - size*0.8, x + size*0.8], [y - size, y - size],
            'g-', linewidth=2, zorder=3)
    n_hash = 5
    for i in range(n_hash):
        xi = x - size*0.8 + i * (2*size*0.8) / (n_hash - 1)
        ax.plot([xi, xi - size*0.15], [y - size, y - size - size*0.2],
                'g-', linewidth=1.5, zorder=3)

draw_pin_support(ax, *nodes[1], size=0.3)
draw_pin_support(ax, *nodes[20], size=0.3)

# Added Mass (Boxes or weights at the bottom nodes)
for nid in mass_nodes:
    x, y = nodes[nid]
    # Draw a little blue weight box attached below the node
    box = patches.Rectangle((x-0.1, y-0.4), 0.2, 0.3, linewidth=1, edgecolor='navy', facecolor='cornflowerblue', zorder=5)
    ax.add_patch(box)
    ax.plot([x, x], [y, y-0.1], 'k-', lw=1.5, zorder=4)

ax.text(5, -0.6, 'Added mass (10 kg) at lower nodes', fontsize=10, fontweight='bold',
        color='navy', ha='center', va='top', zorder=5)

# Highlight Shape variables (y variable)
var_nodes = [(3, 'y₃'), (5, 'y₅'), (7, 'y₇'), (9, 'y₉'), (11, 'y₁₁')]
for nid, label in var_nodes:
    x, y = nodes[nid]
    ax.annotate('', xy=(x, 0.15), xytext=(x, y - 0.1),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=1.2,
                                linestyle='--'), zorder=3)
    ax.text(x + 0.15, y / 2, label, fontsize=10, color='purple',
            fontweight='bold', ha='left', va='center', zorder=5)

ax.text(5, y11 + 0.4, 'Symmetric Design', fontsize=12, fontweight='bold',
        color='purple', ha='center', va='bottom', zorder=5)
ax.plot([5, 5], [y11 + 0.1, y11 + 0.35], 'purple', linewidth=1.5,
        linestyle='-.', zorder=3)

# Legend text for Fixed beams
ax.plot([], [], 'darkred', lw=3, label='Fixed Area ($4 \\times 10^{-3} m^2$)')
ax.plot([], [], 'b-', lw=1.5, label='Design Variables ($14$ Sizing Groups)')
ax.legend(loc='upper right', fontsize=10)

# Dimensions
y_dim = -1.5
ax.annotate('', xy=(0, y_dim), xytext=(10, y_dim),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax.text(5, y_dim - 0.15, '10 \\times 1.0 m = 10.0 m', fontsize=12,
        fontweight='bold', ha='center', va='top', color='black')
ax.plot([0, 0], [0, y_dim + 0.1], 'k--', linewidth=0.7, zorder=1)
ax.plot([10, 10], [0, y_dim + 0.1], 'k--', linewidth=0.7, zorder=1)

ax.set_xlim(-1, 11)
ax.set_ylim(-2.2, y11 + 1.2)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig(r'd:\BOOK\Book 8 TOI UU\truss models\37bar_truss.png',
            dpi=200, bbox_inches='tight')
print("Successfully saved 37bar_truss.png")
