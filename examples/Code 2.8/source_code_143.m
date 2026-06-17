% --- Khởi tạo ---
clc; clear; close all;

% --- 1. Thiết lập lưới dữ liệu ---
x1_vals = linspace(0.01, 1.6, 500); 
x2_vals = linspace(0, 5.5, 500);
[X1, X2] = meshgrid(x1_vals, x2_vals);

% --- 2. Tính toán ràng buộc (Constraint) ---
% Phương trình: (4x1^2 + 200x2^2 + 40x1x2) / (x1^2 * (2x1 + 11x2)^2) = 1
Numer = 4.*X1.^2 + 200.*X2.^2 + 40.*X1.*X2;
Denom = X1.^2 .* (2.*X1 + 11.*X2).^2;
Constraint = Numer ./ Denom;

% Trích xuất tọa độ đường cong từ dữ liệu contour
C_data = contourc(x1_vals, x2_vals, Constraint, [1 1]);

% Xử lý dữ liệu để vẽ liên tục
idx = 1;
x_curve = [];
y_curve = [];
while idx < size(C_data, 2)
    len = C_data(2, idx);
    x_curve = [x_curve, C_data(1, idx+1 : idx+len), NaN];
    y_curve = [y_curve, C_data(2, idx+1 : idx+len), NaN];
    idx = idx + len + 1;
end

% --- 3. Vẽ đồ thị ---
figure('Color', 'w', 'Units', 'pixels', 'Position', [100, 100, 650, 550]);
hold on; axis([0 1.5 0 5]); box on;

% --- A. Vẽ hàm mục tiêu (11x1 + x2 = C) ---
C_values = [2, 5, 8, 11, 14, 17]; 

for i = 1:length(C_values)
    C = C_values(i);
    y_line = C - 11 * x1_vals; % Phương trình đường thẳng
    
    % Chỉ vẽ phần nằm trong giới hạn trục
    mask = y_line >= 0 & y_line <= 5.5;
    if any(mask)
        plot(x1_vals(mask), y_line(mask), '-', 'Color', [0.5 0.5 0.5], 'LineWidth', 0.8);
    end
end

% Nhãn hàm mục tiêu
text(0.55, 4.3, '$11x_1+x_2=\mathrm{const.}$', 'Interpreter', 'latex', 'FontSize', 11);

% --- B. Vẽ đường cong ràng buộc ---
off = 0.008; % Độ lệch tạo bóng

% 1. Đường bóng (Nét đứt)
plot(x_curve - off, y_curve, ':', 'Color', [0.4 0.4 0.4], 'LineWidth', 1);

% 2. Đường chính (Nét liền đậm)
plot(x_curve, y_curve, 'k-', 'LineWidth', 1.5);

% Nhãn ràng buộc
text(1.28, 3.5, '$\mathbf{u}^T\mathbf{u}=\delta_0^2$', 'Interpreter', 'latex', ...
     'FontSize', 12, 'FontWeight', 'bold');

% --- 4. Định dạng trục ---
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 14);

% Tùy chỉnh Tick marks
set(gca, 'TickDir', 'in');
set(gca, 'XTick', 0:0.5:1.5);
set(gca, 'YTick', 0:0.5:5);
set(gca, 'LineWidth', 1, 'FontSize', 10);

hold off;
