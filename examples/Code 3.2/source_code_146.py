import numpy as np
import matplotlib.pyplot as plt

# --- Cấu hình Matplotlib ---
# Thiết lập font LaTeX (Computer Modern)
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'serif'

# --- 1. Chuẩn bị dữ liệu ---
x = np.linspace(-0.2, 1.3, 400)
y = np.linspace(-0.2, 1.3, 400)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2  # Hàm mục tiêu

# --- 2. Khởi tạo hình vẽ ---
fig, ax = plt.subplots(figsize=(7, 7))

# --- 3. Vẽ đồ thị ---
# Đường đồng mức (Contours)
contours = ax.contour(X, Y, Z, levels=np.arange(0, 2.6, 0.5), cmap='viridis')

# Đường ràng buộc (Constraint): x1 + x2 = 1
x_line = np.linspace(-0.2, 1.2, 100)
y_line = 1 - x_line
line_color = '#1f77b4'
ax.plot(x_line, y_line, color=line_color, linewidth=2)

# Điểm tối ưu (Optimal point)
ax.plot(0.5, 0.5, 'o', color=line_color, markersize=8, zorder=5)

# Vector Gradient (Hướng giảm)
ax.arrow(0.5, 0.5, -0.15, -0.15, 
         head_width=0.04, head_length=0.06, 
         fc='black', ec='black', linewidth=2, zorder=5)

# --- 4. Thêm nhãn chú thích (Annotations) ---

# Nhãn hàm mục tiêu
ax.text(0.8, 1.15, r'$g_0(\mathbf{x}) = x_1^2 + x_2^2$', 
        fontsize=14, color='black', 
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# Nhãn ràng buộc g1(x)
ax.text(0.75, 0.3, r'$g_1(\mathbf{x}) = 1 - x_1 - x_2 \leq 0$', 
        fontsize=14, color=line_color, ha='left')

# Nhãn điểm tối ưu
ax.text(0.52, 0.52, r'$\mathbf{x}^* (0.5, 0.5)$', 
        fontsize=14, color=line_color,
        ha='left', va='bottom', zorder=10)

# Nhãn Gradient
ax.text(0.3, 0.3, r'$-\nabla g_0$', fontsize=13, ha='right')

# --- 5. Hoàn thiện hiển thị ---
# Thiết lập trục và lưới
ax.set_xlabel('$x_1$', fontsize=14)
ax.set_ylabel('$x_2$', fontsize=14)
ax.set_xlim([-0.2, 1.3])
ax.set_ylim([-0.2, 1.3])
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_aspect('equal')

plt.tight_layout()
plt.show()
