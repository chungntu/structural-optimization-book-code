import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_beam_diagram():
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # 1. Vẽ thân dầm (hình chữ nhật nét đứt, bo góc)
    # pad=0.1 mở rộng viền ra ngoài -> đáy thực tế ở y = 1.1 - 0.1 = 1.0
    beam = patches.FancyBboxPatch((1, 1.1), 10, 1.8, 
                                  boxstyle="round,pad=0.1", 
                                  linestyle='--', 
                                  edgecolor='black', 
                                  facecolor='none', 
                                  linewidth=1.5)
    ax.add_patch(beam)

    # 2. Vẽ gối đỡ (hình tam giác và gạch chéo)
    # Đỉnh tam giác ở y=1.0 -> vừa chạm đáy dầm (visual bottom = 1.0)
    # Gối bên trái
    left_support = plt.Polygon([[1.0, 0.5], [1.4, 1.0], [1.8, 0.5]], 
                                closed=True, fill=False, lw=1.5)
    ax.add_patch(left_support)
    ax.plot([0.8, 2.0], [0.5, 0.5], color='black', lw=1.5)
    for i in range(5):
        ax.plot([0.85 + i*0.25, 1.05 + i*0.25], [0.35, 0.5], color='black', lw=1)

    # Gối bên phải
    right_support = plt.Polygon([[10.2, 0.5], [10.6, 1.0], [11.0, 0.5]], 
                                 closed=True, fill=False, lw=1.5)
    ax.add_patch(right_support)
    ax.plot([10.0, 11.2], [0.5, 0.5], color='black', lw=1.5)
    for i in range(5):
        ax.plot([10.05 + i*0.25, 10.25 + i*0.25], [0.35, 0.5], color='black', lw=1)

    # 3. Vẽ các mũi tên lực (F và các mũi tên phụ)
    ax.annotate('', xy=(6, 3.1), xytext=(6, 4.5),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=2))
    ax.text(6, 4.6, '$F$', fontsize=30, ha='center', fontweight='bold', fontfamily='Times New Roman')

    ax.annotate('', xy=(5, 3.1), xytext=(5, 3.6),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))
    ax.annotate('', xy=(7, 3.1), xytext=(7, 3.6),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.5))

    # 4. Vẽ 2 lỗ rỗng dạng đường cong mềm phức tạp (không phải ellipse)
    theta = np.linspace(0, 2*np.pi, 200)
    
    # Lỗ bên trái - blob bất đối xứng
    r_left = 0.55 + 0.12*np.sin(3*theta) + 0.08*np.cos(2*theta) + 0.06*np.sin(4*theta - 1)
    cx_l, cy_l = 3.5, 2.05
    ax.plot(cx_l + r_left*1.2*np.cos(theta), 
            cy_l + r_left*0.7*np.sin(theta), 
            linestyle='--', color='black', lw=1)
    
    # Lỗ bên phải - blob khác
    r_right = 0.55 + 0.10*np.cos(3*theta + 0.5) + 0.09*np.sin(2*theta) + 0.05*np.cos(5*theta)
    cx_r, cy_r = 8.5, 2.05
    ax.plot(cx_r + r_right*1.2*np.cos(theta), 
            cy_r + r_right*0.7*np.sin(theta), 
            linestyle='--', color='black', lw=1)

    # 5. Dấu hỏi chấm ở giữa
    ax.text(6, 1.9, '?', fontsize=60, ha='center', va='center', fontfamily='Times New Roman')

    # Thiết lập khung nhìn
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(r'D:\BOOK\fas.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()

if __name__ == "__main__":
    draw_beam_diagram()
