import matplotlib.pyplot as plt

# ===== Font math (Computer Modern) =====
plt.rcParams.update({
    "mathtext.fontset": "cm",
    "font.family": "serif",
})

# ===== Figure =====
fig, ax = plt.subplots(figsize=(6.8, 3.8))

ax.set_xlim(0, 10)
ax.set_ylim(0, 6)

# Ẩn khung và ticks
for s in ax.spines.values():
    s.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# ===== Trục tọa độ =====
origin = (0, 0)
arrow_style = dict(
    arrowstyle="-|>",
    mutation_scale=12,
    lw=1.4,
    color="gray"
)

ax.annotate("", xy=(9.7, 0), xytext=origin, arrowprops=arrow_style)
ax.annotate("", xy=(0, 5.7), xytext=origin, arrowprops=arrow_style)

# Nhãn trục
ax.text(4.85, -0.55, r"$f_1$", fontsize=16, color="gray")
ax.text(-0.55, 2.85, r"$f_2$", fontsize=16, color="gray")

# ===== Dữ liệu điểm (xấp xỉ hình gốc) =====
blue = [
    (1.5, 4.6), (2.2, 4.6), (3.1, 5.0), (3.8, 4.7),
    (5.0, 5.0), (6.1, 4.8), (7.0, 5.2),

    (2.8, 3.8), (3.6, 3.9), (4.5, 4.2),
    (5.3, 3.8), (6.4, 4.1), (7.2, 4.0),

    (2.6, 2.9), (3.3, 3.1), (4.2, 3.0),
    (5.8, 3.1), (6.6, 3.0), (7.3, 3.2),

    (4.8, 2.2), (6.9, 2.4), (7.4, 2.0),
    (8.0, 1.6), (9.0, 2.2),
]

red = [
    (0.7, 5.2),
    (1.0, 3.9), (1.3, 3.6),
    (2.6, 2.5), (3.1, 2.3),
    (4.6, 1.7),
    (6.2, 1.0),
    (7.3, 1.2),
    (8.6, 0.8),
]

bx, by = zip(*blue)
rx, ry = zip(*red)

# ===== Scatter =====
ax.scatter(bx, by, s=28, facecolors="none", edgecolors="black", linewidths=0.8)
ax.scatter(rx, ry, s=28, color="black", edgecolors="black")

# ===== Giữ tỉ lệ trục vuông =====
ax.set_aspect("equal")

import os
script_dir = os.path.dirname(os.path.abspath(__file__))

# ===== Export PNG độ phân giải cao =====
plt.savefig(
    os.path.join(script_dir, "pareto_scatter.png"),
    dpi=600,
    bbox_inches="tight",
    pad_inches=0.05
)

plt.show()

