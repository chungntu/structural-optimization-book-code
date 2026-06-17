import numpy as np
import matplotlib.pyplot as plt

# --- 1. Cấu hình hệ thống hiển thị ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 11

# --- 2. Khởi tạo dữ liệu ---
x = np.linspace(0, 11, 400)
y = np.linspace(0, 11, 400)
X, Y = np.meshgrid(x, y)
Z = (X - 5)**2 + (Y - 4)**2  # Hàm mục tiêu f(x)

# --- 3. Thiết lập khung hình ---
# Sử dụng kích thước 6x6 để đảm bảo khung hình vuông
fig, ax = plt.subplots(figsize=(6, 6), dpi=200)

# --- 4. Vẽ các thành phần hình học ---
# a) Miền khả dĩ (Feasible Region)
x_fill = np.linspace(0, 4, 100)
y_fill = (10 - x_fill)/2
ax.fill_between(x_fill, 0, y_fill, color='#d9d9d9', alpha=0.7)
ax.text(1.5, 2, 'Miền khả dĩ', fontsize=11, ha='center', color='black')

# b) Đường biên ràng buộc (Boundaries)
ax.plot(x, (10 - x)/2, 'k-', linewidth=1.2)                 # Biên g1
ax.axvline(x=4, color='k', linewidth=1.2, ymin=0, ymax=1)   # Biên g2

# c) Đường đồng mức (Contour Lines)
levels = [0.5, 2, 5, 9, 14, 20]
contours = ax.contour(X, Y, Z, levels=levels, colors='black', linewidths=0.6, alpha=0.7)

# d) Các điểm đặc biệt
# Điểm tối ưu x*
ax.plot(4, 3, 'ko', markersize=5)
ax.text(2.8, 2.6, r'$x^*(4,3)$', fontsize=11, fontweight='bold')

# Tâm hàm mục tiêu T
ax.plot(5, 4, 'ko', markersize=3)
ax.text(5.1, 4.0, r'$T(5,4)$', fontsize=11)

# --- 5. Biểu diễn Vector Gradient ---
x0, y0 = 4, 3
arrow_width = 0.008
head_width = 4

# Vector -grad(f)
ax.quiver(x0, y0, 1, 1, angles='xy', scale_units='xy', scale=1, 
          color='#d62728', width=arrow_width, headwidth=head_width, label=r'$-\nabla f$')
ax.text(4.9, 3.5, r'$-\nabla f$', color='#d62728', fontsize=11)

# Vector grad(g1)
s1 = 0.6
ax.quiver(x0, y0, 1*s1, 2*s1, angles='xy', scale_units='xy', scale=1, 
          color='#1f77b4', width=arrow_width, headwidth=head_width)
ax.text(4.0, 4.3, r'$\nabla g_1$', color='#1f77b4', fontsize=11)

# Vector grad(g2)
s2 = 1.2
ax.quiver(x0, y0, 1*s2, 0*s2, angles='xy', scale_units='xy', scale=1, 
          color='#1f77b4', width=arrow_width, headwidth=head_width)
ax.text(5.2, 2.6, r'$\nabla g_2$', color='#1f77b4', fontsize=11)

# --- 6. Hoàn thiện bố cục và chú thích ---
# Thiết lập giới hạn trục (vuông vức 0-11)
ax.set_xlim(0, 11)
ax.set_ylim(0, 11) 

# Tên trục
ax.set_xlabel(r'$x_1$', fontsize=12, loc='right')
ax.set_ylabel(r'$x_2$', fontsize=12, loc='top')

# Nhãn phương trình
ax.text(1.5, 4.6, r'$g_1=0$', fontsize=11, rotation=0)
ax.text(6.5, 1.0, r'$g_1(x) = x_1 + 2x_2 - 10 \leq 0$', fontsize=10)
ax.text(4.2, 0.5, r'$g_2=0$', fontsize=10)
ax.text(0.5, 8.5, r'$g_2(x) = x_1 - 4 \leq 0$', fontsize=10)
ax.text(6.5, 8.5, r'$f(x) = (x_1 - 5)^2 + (x_2 - 4)^2$', fontsize=10)

# Cấu hình hiển thị trục (Center spines)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')

# Thiết lập tỷ lệ 1:1 (Aspect Ratio)
ax.set_aspect('equal')

plt.tight_layout()
plt.show()