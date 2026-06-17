"""
============================================================
Ví dụ 7.x – Tối ưu đa mục tiêu giàn hai thanh
Phương pháp tổng trọng số (Weighted-Sum) → Biên Pareto
============================================================
Hai mục tiêu:
  f1 = khối lượng giàn (kg)
  f2 = |v_C| – chuyển vị đứng tại nút C (mm)

Ràng buộc:
  |σ_i| ≤ σ_allow   (i = 1, 2)
  A_min ≤ A_i ≤ A_max

Biến thiết kế: x = [A1, A2]  (m²)
============================================================
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")                   # backend không cần GUI
import matplotlib.pyplot as plt
matplotlib.rcParams.update({
    "font.size": 12,
    "font.family": "serif",
    "axes.grid": True,
    "grid.alpha": 0.3,
})

# ═══════════════════════════════════════════════════════════
# 1. DỮ LIỆU BÀI TOÁN
# ═══════════════════════════════════════════════════════════
L   = 2.0           # m  – khoảng cách AB
h   = 1.0           # m  – chiều cao nút C
P   = 50e3          # N  – tải trọng
E   = 200e9         # Pa – mô đun đàn hồi
rho = 7850          # kg/m³ – khối lượng riêng
sig_allow = 150e6   # Pa – ứng suất cho phép
A_min = 200e-6      # m² (= 200 mm²)
A_max = 4000e-6     # m² (= 4000 mm²)

# Tọa độ nút (m)
node_A = np.array([0.0, 0.0])
node_B = np.array([L,   0.0])
node_C = np.array([L/2, h  ])

# Chiều dài thanh
L1 = np.linalg.norm(node_C - node_A)   # |AC|
L2 = np.linalg.norm(node_C - node_B)   # |BC|

# Cosin chỉ phương (từ gối đến nút C)
c1 = (node_C[0] - node_A[0]) / L1
s1 = (node_C[1] - node_A[1]) / L1
c2 = (node_C[0] - node_B[0]) / L2
s2 = (node_C[1] - node_B[1]) / L2

print(f"Chiều dài thanh: L1 = {L1:.4f} m, L2 = {L2:.4f} m")
print(f"Thanh AC: cosθ = {c1:.4f}, sinθ = {s1:.4f}")
print(f"Thanh BC: cosθ = {c2:.4f}, sinθ = {s2:.4f}")
print()

# ═══════════════════════════════════════════════════════════
# 2. PHÂN TÍCH KẾT CẤU (Phương pháp độ cứng trực tiếp)
# ═══════════════════════════════════════════════════════════
def analyze(A1, A2):
    """
    Phân tích giàn hai thanh bằng phương pháp độ cứng.
    Trả về: (u_C, v_C, σ1, σ2)
      u_C, v_C : chuyển vị nút C theo x, y (m)
      σ1, σ2   : ứng suất dọc trong thanh AC, BC (Pa)
    """
    # Ma trận độ cứng phần tử (2×2, đã rút gọn về DOF nút C)
    k1 = (E * A1 / L1) * np.array([[c1**2, c1*s1],
                                    [c1*s1, s1**2]])
    k2 = (E * A2 / L2) * np.array([[c2**2, c2*s2],
                                    [c2*s2, s2**2]])
    # Ma trận độ cứng tổng thể
    K = k1 + k2

    # Vector tải
    F = np.array([0.0, -P])

    # Giải hệ phương trình: K · d = F
    d = np.linalg.solve(K, F)
    u_C, v_C = d

    # Biến dạng dọc → ứng suất
    delta1 = c1 * u_C + s1 * v_C          # biến dạng thanh AC
    sigma1 = E * delta1 / L1

    delta2 = c2 * u_C + s2 * v_C          # biến dạng thanh BC
    sigma2 = E * delta2 / L2

    return u_C, v_C, sigma1, sigma2

# ═══════════════════════════════════════════════════════════
# 3. HÀM MỤC TIÊU VÀ RÀNG BUỘC
# ═══════════════════════════════════════════════════════════
def f1_mass(x):
    """Khối lượng giàn (kg)."""
    A1, A2 = x
    return rho * (L1 * A1 + L2 * A2)

def f2_disp(x):
    """Chuyển vị đứng tuyệt đối tại C (mm)."""
    A1, A2 = x
    _, v_C, _, _ = analyze(A1, A2)
    return abs(v_C) * 1e3              # đổi m → mm

def stress_con1(x):
    """g1 = σ_allow − |σ1| ≥ 0"""
    A1, A2 = x
    _, _, sig1, _ = analyze(A1, A2)
    return sig_allow - abs(sig1)

def stress_con2(x):
    """g2 = σ_allow − |σ2| ≥ 0"""
    A1, A2 = x
    _, _, _, sig2 = analyze(A1, A2)
    return sig_allow - abs(sig2)

# ═══════════════════════════════════════════════════════════
# 4. CHUẨN HÓA MỤC TIÊU (utopia–nadir)
# ═══════════════════════════════════════════════════════════
bounds = [(A_min, A_max), (A_min, A_max)]
cons   = [{"type": "ineq", "fun": stress_con1},
          {"type": "ineq", "fun": stress_con2}]
x0     = np.array([1e-3, 1e-3])        # điểm xuất phát (1000 mm²)

# Tối ưu riêng f1
res1 = minimize(f1_mass, x0, method="SLSQP",
                bounds=bounds, constraints=cons)
f1_min = f1_mass(res1.x)
f2_at_f1min = f2_disp(res1.x)

# Tối ưu riêng f2
res2 = minimize(f2_disp, x0, method="SLSQP",
                bounds=bounds, constraints=cons)
f2_min = f2_disp(res2.x)
f1_at_f2min = f1_mass(res2.x)

# Giá trị nadir (cận trên) cho chuẩn hóa
f1_max = f1_at_f2min
f2_max = f2_at_f1min

print("── Kết quả tối ưu đơn mục tiêu ──")
print(f"  min f1 → f1 = {f1_min:.3f} kg, f2 = {f2_at_f1min:.4f} mm")
print(f"  min f2 → f1 = {f1_at_f2min:.3f} kg, f2 = {f2_min:.4f} mm")
print(f"  Chuẩn hóa: f1 ∈ [{f1_min:.3f}, {f1_max:.3f}] kg")
print(f"              f2 ∈ [{f2_min:.4f}, {f2_max:.4f}] mm\n")

# ═══════════════════════════════════════════════════════════
# 5. GIẢI BẰNG PHƯƠNG PHÁP TỔNG TRỌNG SỐ
# ═══════════════════════════════════════════════════════════
def weighted_obj(x, w):
    """F(x;w) = w·f̃1 + (1−w)·f̃2"""
    f1_norm = (f1_mass(x) - f1_min) / (f1_max - f1_min + 1e-30)
    f2_norm = (f2_disp(x) - f2_min) / (f2_max - f2_min + 1e-30)
    return w * f1_norm + (1 - w) * f2_norm

# Quét w từ 0 đến 1
n_pts = 51                              # nhiều điểm hơn cho đường mượt
weights = np.linspace(0, 1, n_pts)

results = []                            # [(w, A1, A2, f1, f2)]
for w in weights:
    res = minimize(weighted_obj, x0, args=(w,), method="SLSQP",
                   bounds=bounds, constraints=cons,
                   options={"ftol": 1e-12, "maxiter": 500})
    A1_opt, A2_opt = res.x
    f1_val = f1_mass(res.x)
    f2_val = f2_disp(res.x)
    results.append((w, A1_opt, A2_opt, f1_val, f2_val))

results = np.array(results)

# In bảng kết quả (mỗi bước 0.1)
print("── Bảng kết quả Pareto ──")
print(f"{'w':>5s} {'A1(mm²)':>10s} {'A2(mm²)':>10s} "
      f"{'f1(kg)':>10s} {'f2(mm)':>10s}")
print("-" * 50)
for row in results:
    w, A1, A2, f1, f2 = row
    if np.isclose(w * 10 % 1, 0, atol=0.02) or w == weights[-1]:
        print(f"{w:5.2f} {A1*1e6:10.1f} {A2*1e6:10.1f} "
              f"{f1:10.3f} {f2:10.4f}")
print()

# ═══════════════════════════════════════════════════════════
# 6. VẼ ĐỒ THỊ
# ═══════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 6))

# ── Biên Pareto ────────────────────────────────────
f1_arr = results[:, 3]
f2_arr = results[:, 4]
sc = ax.scatter(f1_arr, f2_arr, c=results[:, 0], cmap="Greys",
                edgecolors="k", s=80, zorder=5)
ax.plot(f1_arr, f2_arr, "k--", lw=0.8, alpha=0.5)


cbar = fig.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label("Trọng số w")
ax.set_xlabel("$f_1$ – Khối lượng (kg)")
ax.set_ylabel("$f_2$ – Chuyển vị $|v_C|$ (mm)")

plt.tight_layout()
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "pareto_front_two_bar_truss.png")
plt.savefig(save_path, dpi=600, bbox_inches="tight")

print(f"✓ Đồ thị đã lưu: {save_path}")

# ═══════════════════════════════════════════════════════════
# 7. NHẬN XÉT BIÊN PARETO 
# ═══════════════════════════════════════════════════════════
print("""
── NHẬN XÉT ──
• Đường Pareto cho thấy mối quan hệ đánh đổi giữa khối lượng
  và chuyển vị: giảm khối lượng → tăng chuyển vị và ngược lại.
• Vùng w nhỏ (ưu tiên chuyển vị): tăng thêm khối lượng chỉ
  giảm rất ít chuyển vị → "bão hòa" về chuyển vị.
• Vùng w lớn (ưu tiên khối lượng): giảm thêm một ít khối lượng
  sẽ khiến chuyển vị tăng mạnh → "bão hòa" về khối lượng.
• Vùng giữa (w ≈ 0.3–0.6): mỗi đơn vị khối lượng tiết kiệm
  được "đổi" lượng chuyển vị tăng hợp lý → vùng thiết kế hiệu quả.
• Phương án thiết kế đề xuất: chọn điểm "đầu gối" (knee point)
  trên đường Pareto, thường ở w ≈ 0.4–0.5, cân bằng tốt nhất
  giữa hai mục tiêu.
""")


