% -------------------------------------------------------------
% TỐI ƯU HÓA CẤU TRÚC GIÀN
% Phương pháp: Optimality Criteria (OC)
% -------------------------------------------------------------
clear; clc; close all;

%% 1. CẤU HÌNH & TẠO LƯỚI
E        = 1.0;
Vol_frac = 0.10;
xmin     = 1e-9;
xmax     = 1.0;

% Thông số lưới (8x4)
nelx = 8; 
nely = 4; 
dx   = 1; 
dy   = 1;

% Tạo tọa độ nút
[X, Y] = meshgrid(0:dx:nelx*dx, 0:dy:nely*dy);
nodes  = [X(:), Y(:)];
num_nodes = size(nodes, 1);

% Tạo phần tử thanh (Ground Structure)
bars = [];
node_map = reshape(1:num_nodes, nely+1, nelx+1);

for i = 1:nelx
    for j = 1:nely
        nBL = node_map(j, i);   nBR = node_map(j, i+1);
        nTL = node_map(j+1, i); nTR = node_map(j+1, i+1);
        % Kết nối: Ngang, Dọc, Chéo (X)
        bars = [bars; nBL nBR; nTL nTR; nBL nTL; nBR nTR; nBL nTR; nTL nBR];
    end
end

% Loại bỏ các thanh trùng lặp và sắp xếp
bars = unique(sort(bars, 2), 'rows');
num_bars = size(bars, 1);

% Tính toán đặc tính hình học (Chiều dài, Cos, Sin)
d = nodes(bars(:,2), :) - nodes(bars(:,1), :);
L = sqrt(sum(d.^2, 2));
C = d(:,1) ./ L; 
S = d(:,2) ./ L;

% Hàm tính ma trận độ cứng phần tử
GetKe = @(Area, len, c, s) (E * Area / len) * ...
    [ c^2  c*s -c^2 -c*s; 
      c*s  s^2 -c*s -s^2;
     -c^2 -c*s  c^2  c*s; 
     -c*s -s^2  c*s  s^2];

% --- Tối ưu: Tính trước Ke đơn vị (Area=1) cho tất cả các thanh ---
Ke0_store = cell(num_bars, 1);
for i = 1:num_bars
    Ke0_store{i} = GetKe(1, L(i), C(i), S(i));
end

%% 2. ĐIỀU KIỆN BIÊN & TẢI TRỌNG
total_dof = num_nodes * 2;
tol = 1e-6; % Sai số cho phép khi tìm tọa độ

% Ngàm cứng các nút tại biên trái (x = 0)
fixed_nodes = find(abs(nodes(:,1)) < tol); 
fixed_dofs  = [2*fixed_nodes-1; 2*fixed_nodes];
free_dofs   = setdiff(1:total_dof, fixed_dofs(:));

% Tải trọng tại góc dưới bên phải
load_node = find(abs(nodes(:,1) - nelx*dx) < tol & abs(nodes(:,2)) < tol);
F = zeros(total_dof, 1);
F(2*load_node) = -1;

%% 3. THIẾT LẬP HIỂN THỊ
max_iter = 200;
% Các mốc vòng lặp muốn hiển thị
loop_snapshots = [1, 20, 30, 50, 70, max_iter]; 

figure('Name', 'Qua trinh Toi uu hoa', 'Color', 'w', 'Position', [100 100 1000 700]);

% Khởi tạo biến thiết kế (Diện tích mặt cắt)
x = Vol_frac * xmax * ones(num_bars, 1);

%% 4. VÒNG LẶP TỐI ƯU HÓA
change = 1; 
iter = 0;
move = 0.3; % Giới hạn bước nhảy (Move limit)
C_hist = []; % Lịch sử độ mềm

fprintf('%-10s %-15s %-15s\n', 'Iter', 'Compliance', 'Change');

while (change > 1e-6) && (iter < max_iter)
    iter = iter + 1;
    x_old = x;
    
    % --- PHÂN TÍCH FEM ---
    K = sparse(total_dof, total_dof);
    for i = 1:num_bars
        % Ke = Ke0 * x(i) (Vì vật liệu tuyến tính)
        Ke = Ke0_store{i} * x(i);
        
        idx = [2*bars(i,1)-1, 2*bars(i,1), 2*bars(i,2)-1, 2*bars(i,2)];
        K(idx, idx) = K(idx, idx) + Ke;
    end
    
    % Giải hệ phương trình cân bằng: K*u = F
    u = zeros(total_dof, 1);
    u(free_dofs) = K(free_dofs, free_dofs) \ F(free_dofs);
    
    % Tính độ mềm (Compliance)
    compliance = F' * u;
    C_hist = [C_hist; compliance];
    
    % --- TÍNH ĐỘ NHẠY (SENSITIVITY) ---
    dc = zeros(num_bars, 1);
    for i = 1:num_bars
        idx = [2*bars(i,1)-1, 2*bars(i,1), 2*bars(i,2)-1, 2*bars(i,2)];
        ue = u(idx);
        % dc = -ue^T * Ke0 * ue
        dc(i) = -ue' * Ke0_store{i} * ue;
    end
    
    % --- CẬP NHẬT BIẾN THIẾT KẾ (OPTIMALITY CRITERIA) ---
    l1 = 0; l2 = 1e9; 
    V_limit = Vol_frac * sum(xmax * L);
    
    % Phương pháp chia đôi (Bisection) để tìm nhân tử Lagrange
    while (l2 - l1)/(l1 + l2) > 1e-6
        l_mid = 0.5 * (l2 + l1);
        B = -dc ./ (l_mid * L);
        
        % Cập nhật x với move limit và giới hạn biên
        x_new = max(xmin, max(x - move, min(xmax, min(x + move, x .* sqrt(B)))));
        
        if sum(x_new .* L) > V_limit
            l1 = l_mid;
        else
            l2 = l_mid;
        end
    end
    
    change = max(abs(x_new - x));
    x = x_new;
    
    % In tiến độ ra màn hình
    fprintf('%-10d %-15.4e %-15.4e\n', iter, compliance, change);
    
    % --- VẼ HÌNH SNAPSHOT ---
    % Vẽ nếu iter nằm trong danh sách HOẶC là vòng lặp cuối cùng (hội tụ)
    is_snapshot = ismember(iter, loop_snapshots);
    is_final    = (change <= 1e-6) || (iter == max_iter);
    
    if is_snapshot || is_final
        % Xác định vị trí subplot
        if is_snapshot
            idx_in_list = find(loop_snapshots == iter, 1);
        else
            % Nếu hội tụ sớm, vẽ vào ô cuối cùng
            idx_in_list = length(loop_snapshots);
        end
        
        if idx_in_list <= 6 % Chỉ vẽ nếu còn chỗ trong lưới 3x2
            subplot(3, 2, idx_in_list);
            cla; hold on; axis equal; axis off;
            title(sprintf('Iter: %d | C = %.2e', iter, compliance));
            
            % Sắp xếp để vẽ thanh nhỏ trước, thanh lớn sau
            [~, sort_ids] = sort(x);
            
            for k = 1:num_bars
                bar_id = sort_ids(k);
                val = x(bar_id);
                
                % Chỉ vẽ các thanh có diện tích đáng kể
                if val > 0.01 
                    n1 = nodes(bars(bar_id,1), :);
                    n2 = nodes(bars(bar_id,2), :);
                    
                    % Tính biến dạng dọc trục để tô màu
                    dof_idx = [2*bars(bar_id,1)-1, 2*bars(bar_id,1), ...
                               2*bars(bar_id,2)-1, 2*bars(bar_id,2)];
                    u_local = u(dof_idx);
                    
                    axial_def = (u_local(3) - u_local(1)) * C(bar_id) + ...
                                (u_local(4) - u_local(2)) * S(bar_id);
                    
                    if axial_def > 1e-12
                        col = 'b'; % Xanh: Kéo
                    elseif axial_def < -1e-12
                        col = 'r'; % Đỏ: Nén
                    else
                        col = [0.2 0.2 0.2]; % Xám: Không chịu lực
                    end
                    
                    % Độ dày nét vẽ tỷ lệ với diện tích mặt cắt
                    width = 6 * val / xmax;
                    plot([n1(1) n2(1)], [n1(2) n2(2)], '-', 'Color', col, 'LineWidth', width);
                end
            end
            % Vẽ các nút cố định
            plot(nodes(fixed_nodes,1), nodes(fixed_nodes,2), 'ks', ...
                'MarkerFaceColor', 'k', 'MarkerSize', 5);
            drawnow;
        end
    end
end

fprintf('Hoan thanh! Vong lap: %d, Do mem cuoi cung: %.4e\n', iter, compliance);

%% 5. ĐỒ THỊ HỘI TỤ
figure('Name', 'Lich su hoi tu', 'Color', 'w');
plot(1:iter, C_hist, '-o', 'Color', 'b', 'LineWidth', 1.5, 'MarkerSize', 4, 'MarkerFaceColor', 'b');
grid on;
xlabel('Vòng lặp (Iterations)');
ylabel('Độ mềm (Compliance)');
title(['Hội tụ tại vòng lặp ', num2str(iter)]);
