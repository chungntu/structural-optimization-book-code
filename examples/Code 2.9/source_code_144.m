clear; clc; close all;

% Thiết lập cửa sổ hiển thị chính
figure('Color', 'w', 'Units', 'pixels', 'Position', [50, 50, 1000, 500]);

%% =========================================================================
% HÌNH 1: CẬN CẢNH TRUNG BÌNH (BÊN TRÁI)
% =========================================================================

subplot(1, 2, 1); hold on; box on; axis([0.95 1.1 0 0.2]);

% 1. Khởi tạo lưới dữ liệu và tính toán hàm ràng buộc
x1_vals = linspace(0.94, 1.11, 400);
x2_vals = linspace(0, 0.21, 400);
[X1, X2] = meshgrid(x1_vals, x2_vals);

% Công thức ràng buộc: (4x1^2 + 200x2^2 + 40x1x2) / (x1^2 * (2x1 + 11x2)^2)
Numer = 4.*X1.^2 + 200.*X2.^2 + 40.*X1.*X2;
Denom = X1.^2 .* (2.*X1 + 11.*X2).^2;
Constraint = Numer ./ Denom;

% Trích xuất đường đẳng mức (Level Set) tại giá trị bằng 1
C_data = contourc(x1_vals, x2_vals, Constraint, [1 1]);
idx = 1; x_curve = []; y_curve = [];
while idx < size(C_data, 2)
    len = C_data(2, idx);
    x_curve = [x_curve, C_data(1, idx+1 : idx+len), NaN];
    y_curve = [y_curve, C_data(2, idx+1 : idx+len), NaN];
    idx = idx + len + 1;
end

% 2. Vẽ các đường mức hàm mục tiêu (11x1 + x2 = C)
% Phân bổ các đường thẳng dựa trên giao điểm trục hoành
x_intercepts = 0.96 : 0.04 : 1.12; 
C_vals_1 = 11 * x_intercepts;

for C = C_vals_1
    y_line = C - 11 * x1_vals;
    mask = y_line >= -0.01 & y_line <= 0.21; % Giới hạn vẽ trong khung hình
    if any(mask)
        plot(x1_vals(mask), y_line(mask), '-', 'Color', [0.4 0.4 0.4], 'LineWidth', 0.8);
    end
end

% 3. Hiển thị đường ràng buộc (kèm hiệu ứng bóng đổ)
off1 = 0.002; 
plot(x_curve - off1, y_curve, ':', 'Color', [0.4 0.4 0.4], 'LineWidth', 1);
plot(x_curve, y_curve, 'k-', 'LineWidth', 1.5);

% Định dạng trục và nhãn
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 14);
set(gca, 'TickDir', 'in', 'LineWidth', 1, 'FontSize', 12, ...
    'XTick', 0.95:0.05:1.1, 'YTick', 0:0.02:0.2);

%% =========================================================================
% HÌNH 2: CẬN CẢNH CHI TIẾT (BÊN PHẢI)
% =========================================================================

subplot(1, 2, 2); hold on; box on; axis([0.995 0.997 0.005 0.025]); 

% 1. Khởi tạo lưới dữ liệu siêu mịn cho khu vực tối ưu
x1_vals_2 = linspace(0.994, 0.998, 500);
x2_vals_2 = linspace(0.004, 0.026, 500);
[X1_2, X2_2] = meshgrid(x1_vals_2, x2_vals_2);

Numer_2 = 4.*X1_2.^2 + 200.*X2_2.^2 + 40.*X1_2.*X2_2;
Denom_2 = X1_2.^2 .* (2.*X1_2 + 11.*X2_2).^2;
Constraint_2 = Numer_2 ./ Denom_2;

% Trích xuất đường cong ràng buộc mịn
C_data_2 = contourc(x1_vals_2, x2_vals_2, Constraint_2, [1 1]);
idx = 1; x_curve_2 = []; y_curve_2 = [];
while idx < size(C_data_2, 2)
    len = C_data_2(2, idx);
    x_curve_2 = [x_curve_2, C_data_2(1, idx+1 : idx+len), NaN];
    y_curve_2 = [y_curve_2, C_data_2(2, idx+1 : idx+len), NaN];
    idx = idx + len + 1;
end

% 2. Vẽ hệ thống hàm mục tiêu song song dày đặc
x_targets = 0.995 : 0.0004 : 0.998; 
C_vals_2 = 11 * x_targets + 0.01545; % Căn chỉnh tại độ cao y = 0.015

for C = C_vals_2
    y_line = C - 11 * x1_vals_2;
    mask = y_line >= 0 & y_line <= 0.03;
    if any(mask)
        plot(x1_vals_2(mask), y_line(mask), '-', 'Color', [0.4 0.4 0.4], 'LineWidth', 0.8);
    end
end

% 3. Hiển thị đường ràng buộc mịn
off2 = 0.00005; 

plot(x_curve_2 - off2, y_curve_2, ':', 'Color', [0.4 0.4 0.4], 'LineWidth', 1);
plot(x_curve_2, y_curve_2, 'k-', 'LineWidth', 1.5);

% 4. Đánh dấu điểm tối ưu A
x_A = 0.995259; y_A = 0.0170132;
plot(x_A, y_A, 'k+', 'MarkerSize', 9, 'LineWidth', 1.5); 
text(x_A + 0.0001, y_A + 0.001, 'A', 'FontSize', 12, 'FontWeight', 'bold');

% Định dạng trục và nhãn chi tiết
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 14);
set(gca, 'TickDir', 'in', 'LineWidth', 1, 'FontSize', 12);
xticks([0.995 0.9955 0.996 0.9965 0.997]);
yticks([0.005 0.01 0.015 0.02 0.025]);
xtickformat('%.4f'); 

hold off;