"""
Tối ưu hóa kết cấu khung thép bằng thuật toán Simulated Annealing (SA)
kết hợp với SAP2000 qua COM API (OAPI).

Bài toán:
    - Hàm mục tiêu: Cực tiểu hóa trọng lượng kết cấu
    - Biến thiết kế: Tiết diện thép W-section cho 8 nhóm thanh
    - Ràng buộc: Tất cả các thanh phải thỏa mãn tiêu chuẩn thiết kế thép AISC 360

Tài liệu tham khảo:
    - AISC 360-16, Chapter H, Equations H1-1a & H1-1b
    - Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983).
      "Optimization by Simulated Annealing". Science, 220(4598), 671-680.
"""

import os
import sys
import random
import math
import numpy as np
import win32com.client
import time
import matplotlib.pyplot as plt

# ============================================================================
# PHẦN 1: CẤU HÌNH VÀ THAM SỐ
# ============================================================================

# --- Danh sách tiết diện thép W-section (AISC) ---
# Mỗi tiết diện ký hiệu theo dạng: WdXw
#   d = chiều cao tiết diện (inch)
#   w = trọng lượng trên đơn vị chiều dài (lb/ft)
W_SECTIONS = [
    "W12X14", "W12X16", "W12X19", "W12X22", "W12X26", "W12X30", "W12X35", "W12X40", 
    "W12X45", "W12X50", "W12X53", "W12X58", "W12X65", "W12X72", "W12X79", "W12X87", 
    "W12X96", "W12X106", "W12X120", "W12X136", "W12X152", "W12X170", "W12X190", "W12X210", 
    "W12X230", "W12X252", "W12X279", "W12X305", "W12X336", "W14X22", "W14X26", "W14X30", 
    "W14X34", "W14X38", "W14X43", "W14X48", "W14X53", "W14X61", "W14X68", "W14X74", "W14X82", 
    "W14X90", "W14X99", "W14X109", "W14X120", "W14X132", "W14X145", "W14X159", "W14X176", 
    "W14X193", "W14X211", "W14X233", "W14X257", "W14X283", "W14X311", "W14X342", "W14X370", 
    "W14X398", "W14X426", "W14X455", "W14X500", "W14X550", "W14X605", "W14X665", "W14X730", 
    "W16X26", "W16X31", "W16X36", "W16X40", "W16X45", "W16X50", "W16X57", "W16X67", "W16X77", 
    "W16X89", "W16X100", "W18X35", "W18X40", "W18X46", "W18X50", "W18X55", "W18X60", "W18X65",
    "W18X71", "W18X76", "W18X86", "W18X97", "W18X106", "W18X119", "W18X130", "W18X143", "W18X158",
    "W18X175", "W21X44", "W21X48", "W21X50", "W21X55", "W21X57", "W21X62", "W21X68", "W21X73", 
    "W21X83", "W21X93", "W21X101", "W21X111", "W21X122", "W21X132", "W21X147", "W21X166", 
    "W21X182", "W21X201", "W24X55", "W24X62", "W24X68", "W24X76", "W24X84", "W24X94", 
    "W24X103", "W24X104", "W24X117", "W24X131", "W24X146", "W24X162", "W24X176", "W24X192",
    "W24X207", "W24X229", "W24X250", "W24X279", "W24X306", "W24X335", "W24X370", "W27X84",
    "W27X94", "W27X102", "W27X114", "W27X129", "W27X146", "W27X161", "W27X178", "W27X194",
    "W27X217", "W27X235", "W27X258", "W27X281", "W27X307", "W27X336", "W27X368", "W27X539", 
    "W30X90", "W30X99", "W30X108", "W30X116", "W30X124", "W30X132", "W30X148", "W30X173", 
    "W30X191", "W30X211", "W30X235", "W30X261", "W30X292", "W30X326", "W30X357", "W30X391",
    "W33X118", "W33X130", "W33X141", "W33X152", "W33X169", "W33X201", "W33X221", 
    "W33X241", "W33X263", "W33X291", "W33X318", "W33X354", "W33X387"
]

# --- Tham số mô hình SAP2000 ---
MODEL_FILE = "model_v24_2.sdb"                              # Tên file mô hình SAP2000
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))     # Thư mục chứa file code
MODEL_PATH = os.path.join(CURRENT_DIR, MODEL_FILE)           # Đường dẫn đầy đủ đến mô hình
JOINTS = ["1", "10", "19", "28", "37"]                       # Các nút gối tựa (dùng để tính trọng lượng)
NUM_ELEMENTS = 8                                              # Số nhóm thanh cần tối ưu (G1 → G8)

# --- Tham số thuật toán Simulated Annealing ---
INITIAL_TEMP = 100      # Nhiệt độ ban đầu T₀
COOLING_RATE = 0.98      # Hệ số làm nguội α (T_mới = α × T_cũ)
MIN_TEMP = 0.1           # Nhiệt độ dừng T_min
MAX_ITER = 80            # Số vòng lặp tối đa
PENALTY_FACTOR = 1000    # Hệ số phạt cho lời giải không khả thi
RESTART_THRESHOLD = 10   # Số vòng không cải thiện trước khi khởi động lại

# --- Thiết lập Random Seed để kết quả luôn giống nhau mỗi lần chạy ---
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ============================================================================
# PHẦN 2: GIAO TIẾP VỚI SAP2000 (OAPI)
# ============================================================================

def start_sap():
    """
    Kết nối hoặc khởi tạo phiên làm việc SAP2000 qua COM API.
    
    Returns:
        sap_object: Đối tượng ứng dụng SAP2000
        sap_model:  Đối tượng mô hình SAP2000
    """
    try:
        # Thử kết nối đến SAP2000 đang mở
        try:
            sap_object = win32com.client.GetActiveObject("CSI.SAP2000.API.SapObject")
            print("Đã kết nối đến SAP2000 đang chạy")
        except:
            # Nếu chưa mở, khởi tạo SAP2000 mới
            print("Đang khởi tạo SAP2000 mới...")
            sap_object = win32com.client.Dispatch("CSI.SAP2000.API.SapObject")
        
        # Khởi động ứng dụng SAP2000
        ret = sap_object.ApplicationStart()
        if ret != 0:
            raise Exception("Không thể khởi động SAP2000")
        
        # Khởi tạo mô hình rỗng
        sap_model = sap_object.SapModel
        ret = sap_model.InitializeNewModel()
        if ret != 0:
            raise Exception("Không thể khởi tạo mô hình mới")
        
        return sap_object, sap_model
        
    except Exception as e:
        print(f"Lỗi khi khởi động SAP2000: {str(e)}")
        raise

def assign_sections(sap_model, solution):
    """
    Gán tiết diện W-section cho từng nhóm thanh trong mô hình.
    
    Mỗi phần tử trong lời giải là chỉ số (index) tương ứng với 
    một tiết diện trong danh sách W_SECTIONS.
    
    Args:
        sap_model: Đối tượng mô hình SAP2000
        solution:  Mảng [s₁, s₂, ..., s₈], trong đó sᵢ là chỉ số tiết diện cho nhóm Gᵢ
    """
    for i in range(len(solution)):
        group_name = f"G{i+1}"                          # Tên nhóm thanh: G1, G2, ..., G8
        section_name = W_SECTIONS[solution[i]]           # Tra tiết diện từ danh sách
        # ItemType=1: gán cho tất cả thanh trong nhóm
        sap_model.FrameObj.SetSection(group_name, section_name, ItemType=1)

def open_model(sap_model):
    """
    Mở file mô hình SAP2000 và lưu bản sao tạm thời.
    
    Returns:
        sap_model: Đối tượng mô hình SAP2000 đã mở
    """
    # Mở file mô hình gốc
    ret = sap_model.File.OpenFile(MODEL_PATH)
    if ret != 0:
        raise Exception(f"Không thể mở file mô hình: {MODEL_FILE}")
    
    # Lưu bản sao tạm thời (tránh ghi đè file gốc)
    temp_path = os.path.join(CURRENT_DIR, "model_temp3.sdb")
    sap_model.File.Save(temp_path)
    
    return sap_model

def run_analysis(sap_model):
    """
    Chạy phân tích kết cấu trong SAP2000.
    """
    sap_model.Analyze.RunAnalysis()

def check_design(sap_model):
    """
    Chạy kiểm tra thiết kế thép theo AISC 360.
    
    SAP2000 sẽ kiểm tra tất cả thanh theo tiêu chuẩn AISC:
    - Kiểm tra bền (strength)
    - Kiểm tra ổn định (stability) 
    - Tỷ số demand/capacity (D/C ratio)
    
    Returns:
        num_not_passed: Số thanh không thỏa mãn (0 = tất cả đạt)
    """
    # Chạy thiết kế thép
    sap_model.DesignSteel.StartDesign()
    
    # Kiểm tra kết quả: có bao nhiêu thanh không đạt?
    ret, num_not_passed, failed, not_checked, failed_frames = \
        sap_model.DesignSteel.VerifyPassed()
    
    return num_not_passed

def get_weight(sap_model):
    """
    Tính tổng trọng lượng kết cấu từ phản lực gối tựa.
    
    Trọng lượng = Tổng phản lực đứng (F3) tại tất cả gối tựa,
    lấy từ trường hợp tải "weight" (trọng lượng bản thân).
    
    Returns:
        weight: Tổng trọng lượng kết cấu (kips)
    """
    # Chọn trường hợp tải "weight" để xuất kết quả
    sap_model.Results.Setup.SetCaseSelectedForOutput("weight")
    
    # Khởi tạo biến đầu ra cho hàm JointReact
    NumberResults = 0
    Obj = []; Elm = []; LoadCase = []; StepType = []; StepNum = []
    F1 = []; F2 = []; F3 = []; M1 = []; M2 = []; M3 = []
    
    # Tính tổng phản lực đứng tại tất cả gối tựa
    weight = 0
    for joint in JOINTS:
        result = sap_model.Results.JointReact(
            joint, 1, NumberResults, Obj, Elm, LoadCase,
            StepType, StepNum, F1, F2, F3, M1, M2, M3
        )
        # result[9] chứa mảng F3 (phản lực theo phương đứng)
        weight += result[9][0]
    
    return weight

# ============================================================================
# PHẦN 3: ĐỊNH NGHĨA BÀI TOÁN TỐI ƯU
# ============================================================================

def objective_function(sap_model, solution):
    """
    Đánh giá lời giải: tính trọng lượng và kiểm tra ràng buộc.
    
    Quy trình:
        1. Mở mô hình SAP2000
        2. Gán tiết diện theo lời giải
        3. Chạy phân tích kết cấu
        4. Kiểm tra thiết kế thép (ràng buộc)
        5. Tính trọng lượng kết cấu (hàm mục tiêu)
    
    Args:
        sap_model: Đối tượng mô hình SAP2000
        solution:  Mảng chỉ số tiết diện [s₁, s₂, ..., s₈]
    
    Returns:
        weight:         Trọng lượng kết cấu (kips)
        num_not_passed: Số thanh không thỏa mãn ràng buộc
    """
    # Bước 1: Mở mô hình và lưu bản sao tạm
    sap_model = open_model(sap_model)
    
    # Bước 2: Gán tiết diện cho từng nhóm thanh
    assign_sections(sap_model, solution)
    
    # Bước 3: Chạy phân tích kết cấu
    run_analysis(sap_model)
    
    # Bước 4: Kiểm tra ràng buộc thiết kế thép (AISC 360)
    num_not_passed = check_design(sap_model)
    
    # Bước 5: Tính trọng lượng kết cấu
    weight = get_weight(sap_model)
    
    # In kết quả
    feasible = (num_not_passed == 0)
    sections = [W_SECTIONS[i] for i in solution]
    print(f"  Tiết diện: {sections}")
    print(f"  Trọng lượng: {weight:.2f} kips | Khả thi: {feasible}")
    
    return weight, num_not_passed

def penalized_cost(weight, num_not_passed):
    """
    Tính chi phí có phạt (penalized cost) cho lời giải.
    
    Phương pháp hàm phạt (penalty function):
        - Nếu lời giải khả thi (tất cả thanh đạt): chi phí = trọng lượng
        - Nếu lời giải KHÔNG khả thi: chi phí = trọng lượng × PENALTY_FACTOR
    
    Hệ số phạt lớn (= 1000) đảm bảo lời giải vi phạm ràng buộc 
    hầu như luôn bị loại bỏ trong quá trình tối ưu.
    
    Args:
        weight:         Trọng lượng kết cấu
        num_not_passed: Số thanh vi phạm ràng buộc
    
    Returns:
        cost: Chi phí sau khi áp dụng hàm phạt
    """
    if num_not_passed > 0:
        return weight * PENALTY_FACTOR  # Phạt nặng nếu vi phạm
    else:
        return weight                    # Giữ nguyên nếu khả thi

# ============================================================================
# PHẦN 4: THUẬT TOÁN SIMULATED ANNEALING (SA)
# ============================================================================

def generate_initial_solution():
    """
    Tạo lời giải ban đầu.
    
    Sử dụng tiết diện bảo thủ (W14X90, index = 41) cho tất cả nhóm thanh
    để đảm bảo lời giải ban đầu là khả thi, giúp thuật toán hội tụ nhanh hơn.
    
    Returns:
        Mảng [41, 41, ..., 41] có NUM_ELEMENTS phần tử
    """
    return [41 for _ in range(NUM_ELEMENTS)]

def generate_neighbor(current_solution):
    """
    Tạo lời giải lân cận bằng cách thay đổi ngẫu nhiên 1-2 tiết diện.
    
    Cơ chế tạo lân cận (neighborhood structure):
        1. Chọn ngẫu nhiên 1 hoặc 2 nhóm thanh
        2. Thay thế tiết diện của mỗi nhóm bằng một tiết diện ngẫu nhiên khác
    
    Thay đổi 1-2 phần tử giúp cân bằng giữa:
        - Khám phá (exploration): thay đổi đủ lớn để thoát cực trị địa phương
        - Khai thác (exploitation): thay đổi đủ nhỏ để cải thiện dần lời giải
    
    Args:
        current_solution: Lời giải hiện tại [s₁, s₂, ..., s₈]
    
    Returns:
        neighbor: Lời giải lân cận
    """
    neighbor = current_solution.copy()
    
    # Chọn ngẫu nhiên số phần tử cần thay đổi (1 hoặc 2)
    num_changes = random.randint(1, 2)
    
    for _ in range(num_changes):
        # Chọn ngẫu nhiên nhóm thanh cần thay đổi
        idx = random.randint(0, NUM_ELEMENTS - 1)
        
        # Chọn tiết diện mới (khác tiết diện hiện tại)
        old_section = neighbor[idx]
        new_section = old_section
        while new_section == old_section:
            new_section = random.randint(0, len(W_SECTIONS) - 1)
        
        neighbor[idx] = new_section
    
    return neighbor

def acceptance_probability(old_cost, new_cost, temperature):
    """
    Tính xác suất chấp nhận lời giải mới theo tiêu chuẩn Metropolis.
    
    Công thức Boltzmann:
        - Nếu f(x_mới) < f(x_cũ):  P = 1.0        (luôn chấp nhận lời giải tốt hơn)
        - Nếu f(x_mới) ≥ f(x_cũ):  P = exp(-(f_mới - f_cũ) / T)
    
    Ý nghĩa:
        - Nhiệt độ T cao → P lớn → dễ chấp nhận lời giải xấu hơn (khám phá)
        - Nhiệt độ T thấp → P nhỏ → chỉ chấp nhận lời giải tốt hơn (khai thác)
    
    Args:
        old_cost:    Chi phí lời giải hiện tại f(x_cũ)
        new_cost:    Chi phí lời giải mới f(x_mới)
        temperature: Nhiệt độ hiện tại T
    
    Returns:
        Xác suất chấp nhận P ∈ [0, 1]
    """
    # Trường hợp 1: Lời giải mới TỐT HƠN → luôn chấp nhận
    if new_cost < old_cost:
        return 1.0
    
    # Trường hợp 2: Lời giải mới XẤU HƠN → chấp nhận theo xác suất Boltzmann
    delta = new_cost - old_cost           # Δf = f_mới - f_cũ > 0
    return math.exp(-delta / temperature)  # P = exp(-Δf / T)

def simulated_annealing(sap_model):
    """
    Vòng lặp chính của thuật toán Simulated Annealing.
    
    Pseudocode:
        1. Tạo lời giải ban đầu x₀, tính f(x₀)
        2. Đặt T = T₀, x* = x₀ (lời giải tốt nhất)
        3. Lặp cho đến khi T < T_min hoặc đạt MAX_ITER:
            3.1. Tạo lời giải lân cận x' từ x hiện tại
            3.2. Tính f(x') và chi phí có phạt
            3.3. Nếu random() < P(f(x), f(x'), T):
                    Chấp nhận: x ← x'
                    Nếu f(x') < f(x*): cập nhật x* ← x'
            3.4. Giảm nhiệt độ: T ← α × T
        4. Trả về x* (lời giải tốt nhất)
    
    Args:
        sap_model: Đối tượng mô hình SAP2000
    
    Returns:
        best_solution: Mảng tiết diện tối ưu
        best_weight:   Trọng lượng tối ưu
        best_feasible: True nếu lời giải tốt nhất thỏa mãn ràng buộc
    """
    
    # ----- Bước 1: Khởi tạo lời giải ban đầu -----
    print("=" * 60)
    print("THUẬT TOÁN SIMULATED ANNEALING")
    print("=" * 60)
    
    current_x = generate_initial_solution()
    print(f"\nLời giải ban đầu: {[W_SECTIONS[i] for i in current_x]}")
    
    # Đánh giá lời giải ban đầu
    current_w, current_violations = objective_function(sap_model, current_x)
    current_cost = penalized_cost(current_w, current_violations)
    
    print(f"\nTrọng lượng ban đầu: {current_w:.2f} kips")
    print(f"Khả thi: {current_violations == 0}")
    
    # ----- Bước 2: Khởi tạo lời giải tốt nhất -----
    best_x = current_x.copy()
    best_cost = current_cost
    best_w = current_w
    best_violations = current_violations
    
    # ----- Khởi tạo biến theo dõi -----
    temperature = INITIAL_TEMP             # Nhiệt độ hiện tại T
    iteration = 0                           # Bộ đếm vòng lặp
    no_improve_count = 0                    # Bộ đếm vòng không cải thiện
    history = []                            # Lịch sử các lời giải tốt nhất
    
    # Dữ liệu cho đồ thị hội tụ
    weight_list = [current_w]
    iter_list = [0]
    feasible_list = [current_violations == 0]
    
    # ----- Bước 3: Vòng lặp chính -----
    print(f"\n{'='*60}")
    print(f"Bắt đầu tối ưu hóa: T₀={INITIAL_TEMP}, α={COOLING_RATE}, MaxIter={MAX_ITER}")
    print(f"{'='*60}")
    
    while temperature > MIN_TEMP and iteration < MAX_ITER:
        iteration += 1
        
        # --- Bước 3.1: Tạo lời giải lân cận ---
        neighbor_x = generate_neighbor(current_x)
        
        # --- Bước 3.2: Đánh giá lời giải mới ---
        print(f"\n--- Vòng lặp {iteration} | T = {temperature:.2f} ---")
        neighbor_w, neighbor_violations = objective_function(sap_model, neighbor_x)
        neighbor_cost = penalized_cost(neighbor_w, neighbor_violations)
        
        # --- Bước 3.3: Quyết định chấp nhận theo tiêu chuẩn Metropolis ---
        P = acceptance_probability(current_cost, neighbor_cost, temperature)
        r = random.random()   # Số ngẫu nhiên r ∈ [0, 1)
        
        if r < P:
            # CHẤP NHẬN lời giải mới
            current_x = neighbor_x
            current_cost = neighbor_cost
            current_w = neighbor_w
            current_violations = neighbor_violations
            
            result_str = "✓ CHẤP NHẬN"
            if neighbor_cost >= current_cost:
                result_str += f" (P={P:.4f}, r={r:.4f})"
            
            # Cập nhật lời giải tốt nhất nếu cần
            if neighbor_cost < best_cost or \
               (neighbor_cost == best_cost and neighbor_violations < best_violations):
                best_x = neighbor_x.copy()
                best_cost = neighbor_cost
                best_w = neighbor_w
                best_violations = neighbor_violations
                no_improve_count = 0
                
                history.append((best_x.copy(), best_w, best_violations == 0))
                print(f"  ★ LỜI GIẢI TỐT NHẤT MỚI! W = {best_w:.2f} kips")
            else:
                no_improve_count += 1
        else:
            # TỪ CHỐI lời giải mới
            no_improve_count += 1
            result_str = f"✗ TỪ CHỐI (P={P:.4f}, r={r:.4f})"
        
        print(f"  {result_str}")
        
        # Lưu dữ liệu cho đồ thị
        weight_list.append(current_w)
        iter_list.append(iteration)
        feasible_list.append(current_violations == 0)
        
        # --- Bước 3.4: Giảm nhiệt độ ---
        temperature *= COOLING_RATE    # T ← α × T
        
        # Khởi động lại từ lời giải tốt nhất nếu không cải thiện quá lâu
        if no_improve_count >= RESTART_THRESHOLD:
            print(f"\n  ↻ Khởi động lại từ lời giải tốt nhất "
                  f"(không cải thiện {RESTART_THRESHOLD} vòng)")
            current_x = best_x.copy()
            current_cost = best_cost
            current_w = best_w
            current_violations = best_violations
            no_improve_count = 0
    
    # ----- Bước 4: Kết quả cuối cùng -----
    best_feasible = (best_violations == 0)
    
    print(f"\n{'='*60}")
    print(f"KẾT QUẢ TỐI ƯU HÓA")
    print(f"{'='*60}")
    print(f"Tiết diện tối ưu: {[W_SECTIONS[i] for i in best_x]}")
    print(f"Trọng lượng:      {best_w:.2f} kips")
    print(f"Khả thi:          {best_feasible}")
    print(f"Số vòng lặp:      {iteration}")
    
    # In lịch sử cải thiện
    if history:
        print(f"\nLịch sử cải thiện lời giải tốt nhất:")
        for idx, (sol, w, feasible) in enumerate(history):
            print(f"  {idx+1}. W = {w:.2f} kips | Khả thi: {feasible}")
            print(f"     Tiết diện: {[W_SECTIONS[i] for i in sol]}")
    
    # Vẽ đồ thị hội tụ
    plot_convergence(iter_list, weight_list, feasible_list)
    
    return best_x, best_w, best_feasible

# ============================================================================
# PHẦN 5: KẾT QUẢ VÀ TRỰC QUAN HÓA
# ============================================================================

def plot_convergence(iter_list, weight_list, feasible_list):
    """
    Vẽ đồ thị quá trình hội tụ của thuật toán SA.
    
    - Điểm xanh (●): lời giải khả thi
    - Điểm đỏ  (×): lời giải không khả thi
    - Đường xanh:    trọng lượng theo vòng lặp
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Vẽ đường trọng lượng
    ax.plot(iter_list, weight_list, 'b-', linewidth=1, alpha=0.7, label='Trọng lượng')
    
    # Phân loại điểm khả thi / không khả thi
    f_iters = [iter_list[i] for i, f in enumerate(feasible_list) if f]
    f_weights = [weight_list[i] for i, f in enumerate(feasible_list) if f]
    nf_iters = [iter_list[i] for i, f in enumerate(feasible_list) if not f]
    nf_weights = [weight_list[i] for i, f in enumerate(feasible_list) if not f]
    
    # Vẽ điểm phân tán
    ax.scatter(f_iters, f_weights, c='green', marker='o', s=30, 
               label='Khả thi', zorder=5)
    ax.scatter(nf_iters, nf_weights, c='red', marker='x', s=30, 
               label='Không khả thi', zorder=5)
    
    # Định dạng đồ thị
    ax.set_xlabel('Vòng lặp', fontsize=12)
    ax.set_ylabel('Trọng lượng (kips)', fontsize=12)
    ax.set_title('Quá trình hội tụ - Simulated Annealing', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(CURRENT_DIR, 'optimization_progress.png'), dpi=150)
    plt.show()
    print(f"Đã lưu đồ thị: optimization_progress.png")

def print_summary(solution, weight, feasible):
    """In bảng tóm tắt kết quả tối ưu."""
    print(f"\n{'='*60}")
    print(f"TÓM TẮT KẾT QUẢ TỐI ƯU HÓA")
    print(f"{'='*60}")
    print(f"{'Nhóm thanh':<12} {'Tiết diện':<15}")
    print(f"{'-'*27}")
    for i, idx in enumerate(solution):
        print(f"  G{i+1:<9} {W_SECTIONS[idx]:<15}")
    print(f"{'-'*27}")
    print(f"Trọng lượng tối ưu: {weight:.2f} kips")
    print(f"Tất cả thanh đạt:  {feasible}")
    print(f"{'='*60}")

# ============================================================================
# PHẦN 6: CHƯƠNG TRÌNH CHÍNH
# ============================================================================

def main():
    """
    Chương trình chính: khởi động SAP2000, chạy tối ưu hóa, lưu kết quả.
    """
    try:
        # Bước 1: Khởi động SAP2000
        print("Đang kết nối SAP2000...")
        sap_object, sap_model = start_sap()
        
        # Bước 2: Chạy tối ưu hóa bằng Simulated Annealing
        best_solution, best_weight, best_feasible = simulated_annealing(sap_model)
        
        # Bước 3: Áp dụng lời giải tốt nhất và lưu mô hình
        if best_feasible:
            print("\nĐang áp dụng lời giải tối ưu vào mô hình...")
            objective_function(sap_model, best_solution)
            
            output_path = os.path.join(CURRENT_DIR, "model_optimized.sdb")
            sap_model.File.Save(output_path)
            print(f"Đã lưu mô hình tối ưu: {output_path}")
        else:
            print("\n⚠ Cảnh báo: Lời giải tốt nhất KHÔNG khả thi. Không lưu mô hình.")
        
        # In tóm tắt
        print_summary(best_solution, best_weight, best_feasible)
        
    except Exception as e:
        print(f"\nLỗi: {str(e)}")
    
    finally:
        # Đóng SAP2000
        if 'sap_object' in locals():
            try:
                print("\nĐang đóng SAP2000...")
                sap_object.ApplicationExit(False)
                print("Đã đóng SAP2000 thành công")
            except:
                print("Lỗi khi đóng SAP2000")

if __name__ == "__main__":
    main()
