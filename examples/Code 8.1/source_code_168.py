"""
Ví dụ 6: Tối ưu hóa dầm công xôn bằng thuật toán Simulated Annealing (SA)

Mô tả bài toán:
  - Dầm công xôn dài L = 3m, chia thành 5 đoạn, mỗi đoạn dài 0.6m
  - Mặt cắt ngang hình tròn rỗng (r_outer, r_inner)
  - Vật liệu: Thép S270 (E = 210 GPa, σ_yield = 270 MPa)
  - Lực tập trung F = 500 kN tại đầu tự do

Mục tiêu:
  - Tối thiểu hóa Khối lượng dầm

Biến thiết kế (10 biến):
  - r_outer[1..5]: bán kính ngoài của 5 đoạn, 1 ≤ r_outer ≤ 30 cm (≤ L/10)
  - r_inner[1..5]: bán kính trong của 5 đoạn (cm)

Ràng buộc:
  1. Chuyển vị tại đầu dầm ≤ 2 cm
  2. r_outer[i] > r_inner[i]  (mặt cắt hợp lệ)
  3. r_outer[i] > r_inner[i+1] và r_outer[i+1] > r_inner[i]  (thành ống chồng lấn → hàn được)
  4. Ứng suất max < σ_yield = 270 MPa
  5. Bán kính ngoài ≤ L/10 = 30 cm
  6. Chiều dày thành ống: 0.1 cm ≤ (r_outer − r_inner) ≤ 5 cm
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.interpolate import CubicSpline
import os

# ============================================================
# 1. THÔNG SỐ BÀI TOÁN
# ============================================================

L = 3.0                    # Chiều dài dầm (m)
NUM_SEGMENTS = 5            # Số đoạn
SEG_LEN = L / NUM_SEGMENTS  # Chiều dài mỗi đoạn (m)

E = 210e9                   # Mô-đun đàn hồi Young (Pa)
RHO = 7850                  # Khối lượng riêng thép (kg/m³)
SIGMA_YIELD = 270e6         # Giới hạn chảy (Pa)
MAX_DISP = 0.02             # Chuyển vị cho phép tại đầu dầm (m)
F = 500000                  # Lực tập trung tại đầu tự do (N) = 500 kN

# Giới hạn biến thiết kế (cm)
R_OUT_MAX = L * 100 / 10       # r_outer ≤ L/10 = 30 cm
R_OUT_MIN = 1.0                # Bán kính ngoài tối thiểu (cm)
T_MIN = 0.1                    # Chiều dày thành ống tối thiểu (cm) = 1 mm
T_MAX = 5.0                    # Chiều dày thành ống tối đa (cm) = 5 cm

# ============================================================
# 2. CÁC HÀM TÍNH TOÁN KẾT CẤU (Phần tử hữu hạn dầm)
# ============================================================

def area(r_out, r_in):
    """Diện tích mặt cắt tròn rỗng."""
    return np.pi * (r_out**2 - r_in**2)

def moment_of_inertia(r_out, r_in):
    """Mô-men quán tính mặt cắt tròn rỗng."""
    return np.pi * (r_out**4 - r_in**4) / 4

def beam_stiffness_matrix(r_outer, r_inner):
    """
    Lắp ghép ma trận độ cứng tổng thể cho dầm.
    Mỗi nút có 2 bậc tự do: chuyển vị đứng (v) và góc xoay (θ).
    Tổng cộng: (NUM_SEGMENTS + 1) nút × 2 = 12 bậc tự do.
    """
    n_dof = 2 * (NUM_SEGMENTS + 1)
    K = np.zeros((n_dof, n_dof))

    for i in range(NUM_SEGMENTS):
        I_i = moment_of_inertia(r_outer[i], r_inner[i])
        le = SEG_LEN  # chiều dài phần tử

        # Ma trận độ cứng phần tử dầm Euler-Bernoulli (4×4)
        k_e = (E * I_i) * np.array([
            [ 12/le**3,  6/le**2, -12/le**3,  6/le**2],
            [  6/le**2,  4/le,     -6/le**2,  2/le   ],
            [-12/le**3, -6/le**2,  12/le**3, -6/le**2],
            [  6/le**2,  2/le,     -6/le**2,  4/le   ]
        ])

        # Ghép vào ma trận tổng thể
        dofs = [2*i, 2*i+1, 2*i+2, 2*i+3]
        for j in range(4):
            for k in range(4):
                K[dofs[j], dofs[k]] += k_e[j, k]

    return K

def solve_displacement(r_outer, r_inner):
    """
    Giải hệ phương trình K·u = F để tính chuyển vị.
    Điều kiện biên: ngàm tại đầu trái (v₁ = 0, θ₁ = 0).
    Trả về: vector chuyển vị đầy đủ (bao gồm cả nút ngàm).
    """
    K = beam_stiffness_matrix(r_outer, r_inner)

    # Loại bỏ 2 bậc tự do đầu tiên (ngàm)
    K_red = K[2:, 2:]

    # Vector tải trọng (lực F tại nút thứ 2, tức bậc tự do đầu tiên sau ngàm)
    F_vec = np.zeros(K_red.shape[0])
    F_vec[0] = F

    # Giải hệ phương trình
    u_red = np.linalg.solve(K_red, F_vec)

    # Ghép lại vector chuyển vị đầy đủ (thêm 2 giá trị = 0 tại ngàm)
    u_full = np.zeros(2 * (NUM_SEGMENTS + 1))
    u_full[2:] = u_red
    return u_full

def tip_displacement(r_outer, r_inner):
    """Chuyển vị đứng tại đầu tự do của dầm (nút cuối)."""
    u = solve_displacement(r_outer, r_inner)
    return u[-2]   # bậc tự do chuyển vị đứng tại nút cuối

def max_stress(r_outer, r_inner):
    """
    Tính ứng suất lớn nhất trong dầm theo công thức uốn: σ = M·c / I.
    Với dầm công xôn chịu lực tập trung tại đầu: M(x) = F·(L − x).
    """
    sigma_max = 0.0
    for i in range(NUM_SEGMENTS):
        x_mid = (i + 0.5) * SEG_LEN         # vị trí giữa đoạn
        M = F * (L - x_mid)                  # mô-men uốn tại giữa đoạn
        c = r_outer[i]                       # khoảng cách đến thớ ngoài cùng
        I_i = moment_of_inertia(r_outer[i], r_inner[i])
        sigma = abs(M * c / I_i)
        sigma_max = max(sigma_max, sigma)
    return sigma_max

# ============================================================
# 3. HÀM MỤC TIÊU VÀ RÀNG BUỘC
# ============================================================

def objective(params):
    """
    Hàm mục tiêu: Khối lượng dầm (kg).
    params = [r_out1..r_out5, r_in1..r_in5] (đơn vị: cm)
    """
    r_out = params[:NUM_SEGMENTS] / 100   # chuyển sang mét
    r_in = params[NUM_SEGMENTS:] / 100
    weight = 0.0
    for i in range(NUM_SEGMENTS):
        weight += area(r_out[i], r_in[i]) * SEG_LEN * RHO
    return weight

def is_feasible(params):
    """
    Kiểm tra tất cả ràng buộc. Trả về True nếu thiết kế thỏa mãn.

    Ràng buộc:
      (1) Chuyển vị đầu dầm ≤ MAX_DISP
      (2) r_outer[i] > r_inner[i]  ∀i
      (3) r_outer[i+1] > r_inner[i]  ∀i (ràng buộc hàn)
      (4) Ứng suất max < SIGMA_YIELD
      (5) r_outer[i] ≤ R_OUT_MAX (đường kính ngoài ≤ L/10)
      (6) T_MIN ≤ (r_outer[i] − r_inner[i]) ≤ T_MAX (chiều dày thành ống)
    """
    r_out = params[:NUM_SEGMENTS]
    r_in = params[NUM_SEGMENTS:]
    r_out_m = r_out / 100   # chuyển sang mét
    r_in_m = r_in / 100

    # (2) Ràng buộc bán kính: r_outer > r_inner
    if np.any(r_out <= r_in):
        return False

    # (5) Ràng buộc giới hạn trên bán kính ngoài
    if np.any(r_out > R_OUT_MAX) or np.any(r_out < R_OUT_MIN):
        return False

    # (6) Ràng buộc chiều dày thành ống
    thickness = r_out - r_in
    if np.any(thickness < T_MIN) or np.any(thickness > T_MAX):
        return False

    # (3) Ràng buộc hàn: thành ống hai đoạn kề nhau phải chồng lấn
    for i in range(NUM_SEGMENTS - 1):
        if r_out[i] <= r_in[i + 1]:       # r_outer[i] > r_inner[i+1]
            return False
        if r_out[i + 1] <= r_in[i]:       # r_outer[i+1] > r_inner[i]
            return False

    # (1) Ràng buộc chuyển vị
    disp = abs(tip_displacement(r_out_m, r_in_m))
    if disp > MAX_DISP:
        return False

    # (4) Ràng buộc ứng suất
    sigma = max_stress(r_out_m, r_in_m)
    if sigma > SIGMA_YIELD:
        return False

    return True

# ============================================================
# 4. THUẬT TOÁN SIMULATED ANNEALING (SA)
# ============================================================

def simulated_annealing(x0, n_iter=5000, T0=100.0, alpha=0.99):
    """
    Thuật toán Simulated Annealing (Luyện kim mô phỏng).

    Tham số:
      x0     : Nghiệm ban đầu (vector biến thiết kế)
      n_iter : Số vòng lặp tối đa
      T0     : Nhiệt độ ban đầu
      alpha  : Tốc độ làm nguội (0 < alpha < 1)

    Thuật toán:
      1. Bắt đầu với nghiệm x_current, tính f(x_current)
      2. Lặp:
         a. Tạo nghiệm lân cận x_new = x_current + nhiễu ngẫu nhiên
         b. Nếu x_new không thỏa ràng buộc → bỏ qua
         c. Tính Δf = f(x_new) − f(x_current)
         d. Nếu Δf < 0 → chấp nhận (nghiệm tốt hơn)
         e. Nếu Δf ≥ 0 → chấp nhận với xác suất p = exp(−Δf / T)
         f. Giảm nhiệt độ: T = T0 × alpha^k
      3. Trả về nghiệm tốt nhất tìm được
    """
    # --- Khởi tạo ---
    x_current = x0.copy()
    f_current = objective(x_current)
    x_best = x_current.copy()
    f_best = f_current

    # Tìm điểm xuất phát khả thi (nếu x0 vi phạm ràng buộc)
    if not is_feasible(x_current):
        print("Nghiệm ban đầu vi phạm ràng buộc. Tìm điểm khả thi...")
        for _ in range(10000):
            # Tạo nghệm ngẫu nhiên trong giới hạn biến
            r_out_trial = np.random.uniform(R_OUT_MIN, R_OUT_MAX, NUM_SEGMENTS)
            r_out_trial = np.sort(r_out_trial)[::-1]  # giảm dần (hợp lý cho dầm công xôn)
            t_trial = np.random.uniform(T_MIN, T_MAX, NUM_SEGMENTS)
            r_in_trial = r_out_trial - t_trial
            x_trial = np.concatenate([r_out_trial, r_in_trial])
            if is_feasible(x_trial):
                x_current = x_trial.copy()
                x_best = x_trial.copy()
                f_current = objective(x_trial)
                f_best = f_current
                print(f"  Đã tìm được điểm khả thi, khối lượng = {f_best:.2f} kg")
                break
        else:
            print("  CẢNH BÁO: Không tìm được điểm khả thi.")

    # --- Vòng lặp SA ---
    history = []            # lưu lịch sử f_best qua các vòng lặp
    step_size = 1.0         # kích thước bước nhiễu
    n_reject = 0            # đếm số lần liên tiếp bị từ chối

    for k in range(n_iter):
        # Nhiệt độ hiện tại: T_k = T0 × alpha^k
        T_k = T0 * (alpha ** k)

        # Tự điều chỉnh bước: giảm bước nếu bị từ chối quá nhiều
        if n_reject > 50:
            step_size *= 0.9
            n_reject = 0

        # Bước 2a: Tạo nghiệm lân cận
        perturbation = np.random.uniform(-step_size, step_size, len(x_current))
        x_new = x_current + perturbation

        # Giới hạn biên cho biến thiết kế
        x_new[:NUM_SEGMENTS] = np.clip(x_new[:NUM_SEGMENTS], R_OUT_MIN, R_OUT_MAX)
        x_new[NUM_SEGMENTS:] = np.clip(
            x_new[NUM_SEGMENTS:],
            x_new[:NUM_SEGMENTS] - T_MAX,   # r_inner ≥ r_outer − T_MAX
            x_new[:NUM_SEGMENTS] - T_MIN    # r_inner ≤ r_outer − T_MIN
        )
        x_new = np.maximum(x_new, 0.1)     # đảm bảo bán kính trong > 0

        # Bước 2b: Kiểm tra ràng buộc
        if not is_feasible(x_new):
            n_reject += 1
            history.append(f_best)
            continue

        # Bước 2c: Tính chênh lệch hàm mục tiêu
        f_new = objective(x_new)
        delta_f = f_new - f_current

        # Bước 2d-e: Quyết định chấp nhận hay từ chối
        if delta_f < 0:
            # Nghiệm tốt hơn → luôn chấp nhận
            accept = True
        else:
            # Nghiệm kém hơn → chấp nhận với xác suất p = exp(−Δf / T)
            p = np.exp(-delta_f / T_k)
            accept = (np.random.random() < p)

        if accept:
            x_current = x_new.copy()
            f_current = f_new
            n_reject = 0

            # Cập nhật nghiệm tốt nhất
            if f_current < f_best:
                x_best = x_current.copy()
                f_best = f_current
        else:
            n_reject += 1

        # Lưu lịch sử
        history.append(f_best)

        # In tiến trình mỗi 500 vòng
        if k % 500 == 0:
            print(f"  Vòng lặp {k:5d} | f_best = {f_best:.2f} kg | T = {T_k:.6f}")

    return x_best, f_best, history

# ============================================================
# 5. HIỂN THỊ KẾT QUẢ
# ============================================================

def plot_history(history, save_dir):
    """Vẽ biểu đồ lịch sử hội tụ của thuật toán SA."""
    plt.figure(figsize=(10, 6))
    plt.plot(history, linewidth=1.5)
    plt.xlabel('Vòng lặp')
    plt.ylabel('Khối lượng (kg)')
    plt.title('Quá trình hội tụ - Simulated Annealing')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(save_dir, 'optimization_history.png'),
                dpi=300, bbox_inches='tight')
    print(f"  Đã lưu: optimization_history.png")

def plot_deformed_beam(params, save_dir):
    """Vẽ hình dạng biến dạng của dầm sau tối ưu."""
    r_out_m = params[:NUM_SEGMENTS] / 100
    r_in_m = params[NUM_SEGMENTS:] / 100

    # Giải chuyển vị
    u_full = solve_displacement(r_out_m, r_in_m)

    # Lấy chuyển vị đứng tại các nút (đảo dấu để hiển thị võng xuống)
    v_nodes = -u_full[0::2]
    x_nodes = np.linspace(0, L, NUM_SEGMENTS + 1)

    # Nội suy mịn bằng spline bậc 3
    cs = CubicSpline(x_nodes, v_nodes)
    x_smooth = np.linspace(0, L, 200)
    v_smooth = cs(x_smooth)

    # --- Vẽ đồ thị ---
    plt.figure(figsize=(12, 5))

    # Dầm ban đầu (chưa biến dạng)
    plt.plot(x_nodes, np.zeros_like(x_nodes), 'k-', lw=2, label='Dầm ban đầu')

    # Dầm biến dạng
    plt.plot(x_smooth, v_smooth, 'r-', lw=2, label='Dầm biến dạng')
    plt.plot(x_nodes, v_nodes, 'ro', ms=6)

    # Ghi chú chuyển vị tại từng nút
    for x, v in zip(x_nodes, v_nodes):
        plt.annotate(f"{abs(v)*100:.2f} cm", (x, v),
                     textcoords="offset points", xytext=(0, -15),
                     ha='center', fontsize=9,
                     bbox=dict(boxstyle="round,pad=0.3",
                               fc="white", ec="gray", alpha=0.8))

    # Mũi tên lực
    plt.arrow(L, 0, 0, v_nodes[-1] / 2,
              head_width=0.05, head_length=abs(v_nodes[-1] / 4),
              fc='blue', ec='blue', lw=1.5)
    plt.text(L + 0.05, v_nodes[-1] / 2, f"F = {F/1000:.0f} kN",
             color='blue', fontsize=10, ha='left', va='center')

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title('Chuyển vị dầm sau tối ưu')
    plt.xlabel('Chiều dài (m)')
    plt.ylabel('Chuyển vị (m)')
    plt.legend(loc='upper right')

    # Giới hạn trục
    v_min = min(v_nodes)
    y_range = abs(v_min) if abs(v_min) > 0.001 else 0.001
    plt.xlim(0, L + 0.2)
    plt.ylim(v_min * 1.3, y_range * 0.3)

    plt.savefig(os.path.join(save_dir, 'deformed_beam.png'),
                dpi=300, bbox_inches='tight')
    print(f"  Đã lưu: deformed_beam.png")

def plot_beam_shape(params, save_dir):
    """
    Vẽ hình dạng dầm tối ưu:
      - Subplot 1: Sơ đồ dầm nhìn từ mặt bên (side view)
      - Subplot 2: Các mặt cắt ngang hình tròn rỗng (cross sections)
    """
    r_out = params[:NUM_SEGMENTS]   # cm
    r_in = params[NUM_SEGMENTS:]    # cm

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9),
                                   gridspec_kw={'height_ratios': [1, 1.5]})
    plt.subplots_adjust(hspace=0.45)

    # ------------------------------------------------------------------
    # SUBPLOT 1: SƠ ĐỒ DẦM (SIDE VIEW)
    # ------------------------------------------------------------------
    colors = plt.cm.Blues(np.linspace(0.3, 0.7, NUM_SEGMENTS))
    current_x = 0
    for i in range(NUM_SEGMENTS):
        # Vùng thành ống (tô màu)
        rect_fill_top = patches.Rectangle(
            (current_x, r_in[i]), SEG_LEN, r_out[i] - r_in[i],
            facecolor=colors[i], edgecolor='none', alpha=0.4)
        rect_fill_bot = patches.Rectangle(
            (current_x, -r_out[i]), SEG_LEN, r_out[i] - r_in[i],
            facecolor=colors[i], edgecolor='none', alpha=0.4)
        ax1.add_patch(rect_fill_top)
        ax1.add_patch(rect_fill_bot)

        # Biên ngoài (nét liền)
        rect_outer = patches.Rectangle(
            (current_x, -r_out[i]), SEG_LEN, r_out[i] * 2,
            linewidth=2, edgecolor='black', facecolor='none')
        # Biên trong (nét đứt)
        rect_inner = patches.Rectangle(
            (current_x, -r_in[i]), SEG_LEN, r_in[i] * 2,
            linewidth=1, edgecolor='gray', linestyle='--', facecolor='none')

        ax1.add_patch(rect_outer)
        ax1.add_patch(rect_inner)

        # Nhãn đoạn
        ax1.text(current_x + SEG_LEN / 2, r_out[i] + 3,
                 f"Đoạn {i+1}", ha='center', fontsize=9, fontweight='bold')
        # Kích thước bán kính ngoài
        ax1.text(current_x + SEG_LEN / 2, -r_out[i] - 4,
                 f"R={r_out[i]:.1f}", ha='center', fontsize=8, color='blue')

        current_x += SEG_LEN

    # Vẽ ký hiệu ngàm (hatch)
    ax1.add_patch(patches.Rectangle(
        (-0.08, -max(r_out) * 1.1), 0.08, max(r_out) * 2.2,
        facecolor='gray', edgecolor='black', hatch='///', linewidth=2))

    # Mũi tên lực tại đầu tự do
    r_max = max(r_out)
    ax1.annotate('', xy=(L, 0), xytext=(L, r_max * 1.5),
                 arrowprops=dict(facecolor='red', edgecolor='red',
                                 shrink=0.05, width=3, headwidth=10))
    ax1.text(L + 0.05, r_max * 1.3, f'F = {F/1000:.0f} kN',
             color='red', fontsize=11, fontweight='bold', ha='left')

    # Đường trục dầm
    ax1.axhline(y=0, color='gray', linestyle='-.', linewidth=0.8, alpha=0.5)

    ax1.set_xlim(-0.15, L + 0.4)
    ax1.set_ylim(-r_max * 1.6, r_max * 1.8)
    ax1.set_title('Sơ đồ dầm công xôn (nhìn từ mặt bên)', fontsize=13)
    ax1.set_xlabel('Chiều dài (m)')
    ax1.set_ylabel('Kích thước (cm)')
    ax1.grid(True, linestyle=':', alpha=0.5)

    # ------------------------------------------------------------------
    # SUBPLOT 2: MẶT CẮT NGANG (CROSS SECTIONS) — hình tròn rỗng
    # ------------------------------------------------------------------
    spacing = max(r_out) * 2.8   # khoảng cách giữa các mặt cắt
    for i in range(NUM_SEGMENTS):
        cx = i * spacing   # tâm mặt cắt

        # Vòng tròn ngoài (tô xám)
        circle_out = patches.Circle(
            (cx, 0), r_out[i],
            facecolor='lightsteelblue', edgecolor='black', linewidth=1.5)
        # Vòng tròn trong (đục trắng)
        circle_in = patches.Circle(
            (cx, 0), r_in[i],
            facecolor='white', edgecolor='black', linewidth=1)

        ax2.add_patch(circle_out)
        ax2.add_patch(circle_in)

        # Nhãn mặt cắt
        t_i = r_out[i] - r_in[i]
        ax2.text(cx, -r_out[i] - 5,
                 f"Mặt cắt {i+1}\nt = {t_i:.2f} cm",
                 ha='center', fontsize=9, va='top')

        # Đường ghi kích thước bán kính ngoài
        ax2.plot([cx, cx + r_out[i]], [0, 0], 'b-', linewidth=0.8)
        ax2.plot(cx + r_out[i], 0, 'b|', markersize=8)
        ax2.text(cx + r_out[i] / 2, 1.5,
                 f"R={r_out[i]:.1f}", ha='center', fontsize=7, color='blue')

    total_width = (NUM_SEGMENTS - 1) * spacing
    ax2.set_xlim(-r_max * 1.5, total_width + r_max * 1.5)
    ax2.set_ylim(-r_max * 2, r_max * 1.8)
    ax2.set_aspect('equal')
    ax2.axis('off')
    ax2.set_title('Chi tiết các mặt cắt ngang − ống tròn rỗng', fontsize=13)

    plt.savefig(os.path.join(save_dir, 'beam_cross_sections.png'),
                dpi=300, bbox_inches='tight')
    print(f"  Đã lưu: beam_cross_sections.png")

def print_results(params, f_best):
    """In kết quả tối ưu ra console."""
    r_out = params[:NUM_SEGMENTS]
    r_in = params[NUM_SEGMENTS:]
    r_out_m = r_out / 100
    r_in_m = r_in / 100

    print("\n" + "=" * 50)
    print("KẾT QUẢ TỐI ƯU")
    print("=" * 50)
    print(f"Khối lượng tối ưu: {f_best:.2f} kg")
    print(f"\nKích thước mặt cắt tối ưu (cm):")
    print(f"  {'Đoạn':<8} {'r_outer':>10} {'r_inner':>10} {'t (dày)':>10}")
    print(f"  {'-'*38}")
    for i in range(NUM_SEGMENTS):
        t_i = r_out[i] - r_in[i]
        print(f"  {i+1:<8} {r_out[i]:>10.2f} {r_in[i]:>10.2f} {t_i:>10.2f}")

    disp = abs(tip_displacement(r_out_m, r_in_m))
    sigma = max_stress(r_out_m, r_in_m)
    print(f"\nChuyển vị đầu dầm:  {disp*100:.2f} cm  (giới hạn: {MAX_DISP*100:.0f} cm)")
    print(f"Ứng suất lớn nhất:  {sigma/1e6:.2f} MPa (giới hạn: {SIGMA_YIELD/1e6:.0f} MPa)")
    print("=" * 50)

def save_results(params, f_best, save_dir):
    """Lưu kết quả ra file text."""
    r_out = params[:NUM_SEGMENTS]
    r_in = params[NUM_SEGMENTS:]
    r_out_m = r_out / 100
    r_in_m = r_in / 100

    path = os.path.join(save_dir, 'optimization_results.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"Khối lượng tối ưu: {f_best:.2f} kg\n\n")
        f.write(f"Kích thước mặt cắt tối ưu (cm):\n")
        for i in range(NUM_SEGMENTS):
            f.write(f"  Đoạn {i+1}: r_outer = {r_out[i]:.2f}, r_inner = {r_in[i]:.2f}\n")
        disp = abs(tip_displacement(r_out_m, r_in_m))
        sigma = max_stress(r_out_m, r_in_m)
        f.write(f"\nChuyển vị đầu dầm: {disp*100:.2f} cm\n")
        f.write(f"Ứng suất lớn nhất: {sigma/1e6:.2f} MPa\n")
    print(f"  Đã lưu: optimization_results.txt")

# ============================================================
# 6. CHƯƠNG TRÌNH CHÍNH
# ============================================================

def generate_random_initial(seed=None):
    """
    Tạo nghiệm ban đầu ngẫu nhiên trong miền khả thi.
    r_outer giảm dần (hợp lý cho dầm công xôn), chiều dày trong [T_MIN, T_MAX].
    """
    if seed is not None:
        np.random.seed(seed)

    # Sinh r_outer ngẫu nhiên rồi sắp giảm dần
    r_out = np.random.uniform(R_OUT_MIN + T_MAX, R_OUT_MAX, NUM_SEGMENTS)
    r_out = np.sort(r_out)[::-1]

    # Sinh chiều dày ngẫu nhiên
    t = np.random.uniform(T_MIN, T_MAX, NUM_SEGMENTS)
    r_in = r_out - t

    return np.concatenate([r_out, r_in])

def main():
    save_dir = os.path.dirname(os.path.abspath(__file__))

    # --- Thông số chạy nhiều lần ---
    N_RUNS = 50         # số lần chạy SA
    N_ITER = 5000       # số vòng lặp mỗi lần
    T0 = 100.0          # nhiệt độ ban đầu
    ALPHA = 0.99        # tốc độ làm nguội

    # In thông tin bài toán
    print("=" * 60)
    print("TỐI ƯU HÓA DẦM CÔNG XÔN - SIMULATED ANNEALING")
    print(f"Chạy {N_RUNS} lần từ các điểm xuất phát ngẫu nhiên khác nhau")
    print("=" * 60)
    print(f"Chiều dài dầm:  L = {L} m ({NUM_SEGMENTS} đoạn)")
    print(f"Lực tập trung:  F = {F/1000:.0f} kN")
    print(f"Vật liệu:       Thép S270 (σ_y = {SIGMA_YIELD/1e6:.0f} MPa)")
    print(f"Biến thiết kế:  {2*NUM_SEGMENTS} biến (r_outer, r_inner)")
    print(f"Giới hạn:       r_outer ≤ {R_OUT_MAX} cm, "
          f"chiều dày {T_MIN}–{T_MAX} cm")

    # --- Chạy SA nhiều lần ---
    all_results = []     # [(x_best, f_best, history), ...]
    all_f_best = []

    for run in range(N_RUNS):
        print(f"\n{'─'*60}")
        print(f"LẦN CHẠY {run + 1}/{N_RUNS}")
        print(f"{'─'*60}")

        # Tạo nghiệm ban đầu ngẫu nhiên
        x0 = generate_random_initial(seed=run * 42 + 7)

        # Kiểm tra khả thi
        w0 = objective(x0)
        feas = is_feasible(x0)
        print(f"  Nghiệm ban đầu: Khối lượng = {w0:.2f} kg, Khả thi: {feas}")

        # Chạy SA
        x_best, f_best, history = simulated_annealing(
            x0, n_iter=N_ITER, T0=T0, alpha=ALPHA
        )

        all_results.append((x_best, f_best, history))
        all_f_best.append(f_best)
        print(f"  → Kết quả: Khối lượng = {f_best:.2f} kg")

    # --- Thống kê tổng hợp ---
    all_f_best = np.array(all_f_best)
    idx_best = np.argmin(all_f_best)
    idx_worst = np.argmax(all_f_best)

    print(f"\n{'='*60}")
    print(f"THỐNG KÊ TỔNG HỢP ({N_RUNS} lần chạy)")
    print(f"{'='*60}")
    print(f"\n  {'Lần':<6} {'Khối lượng (kg)':>16}")
    print(f"  {'-'*24}")
    for i, f in enumerate(all_f_best):
        marker = " ← TỐT NHẤT" if i == idx_best else ""
        print(f"  {i+1:<6} {f:>16.2f}{marker}")

    print(f"\n  {'─'*30}")
    print(f"  Tốt nhất  (lần {idx_best+1}): {all_f_best[idx_best]:.2f} kg")
    print(f"  Kém nhất  (lần {idx_worst+1}): {all_f_best[idx_worst]:.2f} kg")
    print(f"  Trung bình:          {np.mean(all_f_best):.2f} kg")
    print(f"  Độ lệch chuẩn:      {np.std(all_f_best):.2f} kg")
    print(f"  Hệ số biến thiên:   {np.std(all_f_best)/np.mean(all_f_best)*100:.1f}%")
    print(f"{'='*60}")

    # --- In chi tiết nghiệm tốt nhất ---
    x_global_best, f_global_best, history_best = all_results[idx_best]
    print(f"\nCHI TIẾT NGHIỆM TỐT NHẤT (lần chạy {idx_best + 1}):")
    print_results(x_global_best, f_global_best)
    save_results(x_global_best, f_global_best, save_dir)

    # --- Vẽ đồ thị cho nghiệm tốt nhất ---
    print("\nĐang vẽ đồ thị cho nghiệm tốt nhất...")
    plot_history(history_best, save_dir)
    plot_deformed_beam(x_global_best, save_dir)
    plot_beam_shape(x_global_best, save_dir)

    # --- Vẽ biểu đồ so sánh các lần chạy ---
    plt.figure(figsize=(10, 5))
    plt.bar(range(1, N_RUNS + 1), all_f_best,
            color=['green' if i == idx_best else 'steelblue'
                   for i in range(N_RUNS)],
            edgecolor='black', linewidth=0.5)
    plt.axhline(y=np.mean(all_f_best), color='red', linestyle='--',
                linewidth=1.5, label=f'Trung bình = {np.mean(all_f_best):.2f} kg')
    plt.xlabel('Lần chạy')
    plt.ylabel('Khối lượng tối ưu (kg)')
    plt.title(f'So sánh {N_RUNS} lần chạy SA từ các điểm xuất phát khác nhau')
    plt.legend()
    plt.grid(True, axis='y', linestyle=':', alpha=0.5)
    plt.xticks(range(1, N_RUNS + 1))
    plt.savefig(os.path.join(save_dir, 'multi_run_comparison.png'),
                dpi=300, bbox_inches='tight')
    print(f"  Đã lưu: multi_run_comparison.png")

    print("\nHoàn thành!")

if __name__ == "__main__":
    main()

