% -------------------------------------------------------------
% TỐI ƯU HÓA CẤU TRÚC GIÀN DÙNG THUẬT TOÁN MMA
% -------------------------------------------------------------

clear; clc; close all;

%% 1. CẤU HÌNH & TẠO LƯỚI
E = 1e7;
Vol_frac = 0.10;

xmin = 1e-3;
xmax = 1.0;

% Thông số lưới (8x4)
nelx = 8; nely = 4; dx = 100; dy = 100;

[X, Y] = meshgrid(0:dx:nelx*dx, 0:dy:nely*dy);
nodes = [X(:), Y(:)];
num_nodes = size(nodes, 1);

bars = [];
node_map = reshape(1:num_nodes, nely+1, nelx+1);
for i = 1:nelx
    for j = 1:nely
        nBL = node_map(j, i);   nBR = node_map(j, i+1);
        nTL = node_map(j+1, i); nTR = node_map(j+1, i+1);
        bars = [bars; nBL nBR; nTL nTR; nBL nTL; nBR nTR; nBL nTR; nTL nBR];
    end
end
bars = unique(sort(bars, 2), 'rows');
num_bars = size(bars, 1);

dxy = nodes(bars(:,2), :) - nodes(bars(:,1), :);
L = sqrt(sum(dxy.^2, 2));
C = dxy(:,1) ./ L; 
S = dxy(:,2) ./ L;

GetKe = @(Area, len, c, s) (E * Area / len) * ...
    [ c^2  c*s -c^2 -c*s;  c*s  s^2 -c*s -s^2;
     -c^2 -c*s  c^2  c*s; -c*s -s^2  c*s  s^2];

%% 2. ĐIỀU KIỆN BIÊN & TẢI TRỌNG
total_dof = num_nodes * 2;

fixed_nodes = find(nodes(:,1) < 1e-6);          % biên trái ngàm (fix x,y)
fixed_dofs  = [2*fixed_nodes-1; 2*fixed_nodes];
free_dofs   = setdiff(1:total_dof, fixed_dofs(:));

load_node = find(nodes(:,1)==nelx*dx & nodes(:,2)==0);
F = zeros(total_dof, 1);
F(2*load_node) = -10000;

%% 3. THIẾT LẬP HIỂN THỊ SNAPSHOTS
max_iter = 500;

loop_snapshots = [1, 100, 200, 300, 400, 500];
figure('Name', 'Toi uu hoa gian (MMA) - Snapshots', ...
       'Color', 'w', 'Position', [50 50 1000 800]);

%% 4. THIẾT LẬP MMA
n = num_bars;   % số biến thiết kế
m = 1;          % 1 ràng buộc thể tích

x     = Vol_frac * xmax * ones(n,1);
xold1 = x;
xold2 = x;

low = xmin*ones(n,1);
upp = xmax*ones(n,1);

% Tham số MMA
a0 = 1;
a  = zeros(m,1);

% ---- SIẾT CHẶT: tăng "kỷ luật" ràng buộc ----
c_mma = 1e5*ones(m,1);     % thử 1e5; nếu cần siết hơn: 1e6
d_mma = zeros(m,1);

V_limit = Vol_frac * sum(xmax * L);

% Lưu lịch sử
C_hist = nan(max_iter,1);
g_hist = nan(max_iter,1);

fprintf('Dang chay toi uu hoa (MMA - siet chat)...\n');

%% 5. VÒNG LẶP TỐI ƯU HÓA (MMA)
C0 = [];   % scale compliance

for iter = 1:max_iter
    % --- PHÂN TÍCH FEM ---
    K = sparse(total_dof, total_dof);
    for i = 1:n
        Ke = GetKe(x(i), L(i), C(i), S(i));
        idx = [2*bars(i,1)-1, 2*bars(i,1), 2*bars(i,2)-1, 2*bars(i,2)];
        K(idx, idx) = K(idx, idx) + Ke;
    end

    u = zeros(total_dof, 1);
    u(free_dofs) = K(free_dofs, free_dofs) \ F(free_dofs);

    compliance = F' * u;

    if iter == 1
        C0 = max(compliance, 1e-12);  
    end

    C_hist(iter) = compliance;

    % --- ĐỘ NHẠY MỤC TIÊU: dC/dx ---
    dc = zeros(n,1);
    for i = 1:n
        Ke0 = GetKe(1, L(i), C(i), S(i));   % tuyến tính theo Area
        idx = [2*bars(i,1)-1, 2*bars(i,1), 2*bars(i,2)-1, 2*bars(i,2)];
        ue = u(idx);
        dc(i) = -ue' * Ke0 * ue;
    end

    % --- RÀNG BUỘC THỂ TÍCH: g(x) <= 0 ---
    g = sum(x.*L)/V_limit - 1;
    g_hist(iter) = g;

    dgdx = (L / V_limit)';   % 1 x n

    % --- SCALE MỤC TIÊU cho MMA ---
    f0val = compliance / C0;
    df0dx = dc / C0;

    fval = g;                % m x 1
    dfdx = dgdx;             % m x n

    % --- SIẾT MOVE LIMIT bằng low/upp trước khi gọi MMA ---
    move = 0.05;                    
    range = move*(xmax - xmin);
    low = max(xmin, x - range);
    upp = min(xmax, x + range);

    % --- GỌI MMA SUBPROBLEM ---
    [xmma,~,~,~,~,~,~,~,~,low,upp] = mmasub( ...
        m,n,iter,x,xmin*ones(n,1),xmax*ones(n,1),xold1,xold2, ...
        f0val,df0dx,fval,dfdx,low,upp,a0,a,c_mma,d_mma);

    % --- (TUỲ CHỌN) ÉP FEASIBLE MỖI VÒNG: KHÔNG VƯỢT THỂ TÍCH ---
    if sum(xmma.*L) > V_limit
        xmma = xmma * (V_limit / sum(xmma.*L));
        xmma = min(xmax, max(xmin, xmma));
    end

    % --- CẬP NHẬT ---
    xold2 = xold1;
    xold1 = x;
    x = xmma;

    change = max(abs(x - xold1));

    % --- VẼ SNAPSHOT ---
    if ismember(iter, loop_snapshots)
        idx_in_list = find(loop_snapshots == iter);
        subplot(3,2,idx_in_list);
        hold on; axis equal; axis off;
        title(sprintf('Vòng lặp: %d | C=%.2e', iter, compliance));

        [~, sort_ids] = sort(x);
        for k = 1:n
            bar_id = sort_ids(k);
            val = x(bar_id);
            if val > 0.01
                n1 = nodes(bars(bar_id,1), :);
                n2 = nodes(bars(bar_id,2), :);

                dof_idx = [2*bars(bar_id,1)-1, 2*bars(bar_id,1), 2*bars(bar_id,2)-1, 2*bars(bar_id,2)];
                u_local = u(dof_idx);
                axial_def = (u_local(3) - u_local(1)) * C(bar_id) + ...
                            (u_local(4) - u_local(2)) * S(bar_id);

                if axial_def > 1e-12
                    col = 'b'; % kéo
                elseif axial_def < -1e-12
                    col = 'r'; % nén
                else
                    col = 'k';
                end

                width = 6 * val / xmax;
                plot([n1(1) n2(1)], [n1(2) n2(2)], '-', 'Color', col, 'LineWidth', width);
            end
        end
        plot(nodes(fixed_nodes,1), nodes(fixed_nodes,2), 'ks', 'MarkerFaceColor', 'k', 'MarkerSize', 4);
        drawnow;
    end

    fprintf('iter=%3d | C=%.3e | g=%.3e | change=%.3e\n', iter, compliance, g, change);

    % --- TIÊU CHÍ DỪNG: vừa change nhỏ vừa ràng buộc gần 0 ---
    if (change < 1e-6) && (abs(g) < 1e-6)
        fprintf('Hoi tu! iter=%d | C=%.3e | g=%.3e\n', iter, compliance, g);
        break;
    end
end

iter_end = find(~isnan(C_hist), 1, 'last');
fprintf('Hoan thanh! Vong lap cuoi: %d, C: %.3e, g: %.3e\n', ...
    iter_end, C_hist(iter_end), g_hist(iter_end));


