% --- Khởi tạo ---
clc; clear; close all;

% --- 1. Thiết lập dữ liệu ---
% Tạo lưới điểm cho từng vùng
x1_left = linspace(0.001, 0.249, 200);  % Vùng Sigma 3
x1_right = linspace(0.252, 1.0, 500);   % Vùng Sigma 1
x1_all = linspace(0, 1.0, 200);         % Vùng Sigma 2

% --- 2. Các hàm ràng buộc ---
sigma1_func = @(x) (2.*x - 4.*x.^2) ./ (4.*x - 1);
sigma2_func = @(x) (1 / sqrt(2)) - x;
sigma3_func = @(x) (4 .* x.^2) ./ (1 - 4.*x);

% --- 3. Tính các điểm đặc biệt ---
% Điểm A: Giao của Sigma 1 & 2
k = 1 / sqrt(2);
x_A = k / (4*k - 1); 
y_A = sigma2_func(x_A);

% Điểm B: Giao Sigma 1 với trục hoành
x_B = 0.5;
y_B = 0;

% --- 4. Vẽ đồ thị ---
figure('Color', 'w', 'Units', 'pixels', 'Position', [100, 100, 700, 600]);
hold on; axis([0 1 0 1]); box on;

% Độ lệch nét đứt (tạo bóng)
off = 0.015;

% --- Vẽ Sigma 3 (Trái) ---
y_s3 = sigma3_func(x1_left);
mask_s3 = (y_s3 >= -0.1) & (y_s3 <= 1.2);
x3_plot = x1_left(mask_s3);
y3_plot = y_s3(mask_s3);
% 1. Đường bóng
plot(x3_plot - off, y3_plot, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1);
% 2. Đường chính
plot(x3_plot, y3_plot, 'k-', 'LineWidth', 1.2);
text(0.08, 0.92, '$\sigma_3=2\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Vẽ Sigma 2 (Thẳng) ---
y_s2 = sigma2_func(x1_all);
% 1. Đường bóng
plot(x1_all - off/2, y_s2 - off/2, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1);
% 2. Đường chính
plot(x1_all, y_s2, 'k-', 'LineWidth', 1.2);
text(0.02, 0.72, '$\sigma_2=\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Vẽ Sigma 1 (Phải) ---
y_s1 = sigma1_func(x1_right);
mask_s1 = (y_s1 >= -0.1) & (y_s1 <= 1.2);
x1_plot = x1_right(mask_s1);
y1_plot = y_s1(mask_s1);
% 1. Đường bóng
plot(x1_plot - off, y1_plot, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1);
% 2. Đường chính
plot(x1_plot, y1_plot, 'k-', 'LineWidth', 1.2);
text(0.33, 0.95, '$\sigma_1=2\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Các chi tiết khác ---
% Điểm A
plot(x_A, y_A, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x_A + 0.02, y_A + 0.02, 'A', 'FontSize', 12, 'FontWeight', 'bold');

% Điểm B
plot(x_B, y_B, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x_B + 0.02, 0.02, 'B', 'FontSize', 12, 'FontWeight', 'bold');

% --- Đường đồng mức (Contours) ---
C_opt = sqrt(2); % Giá trị tối ưu
contours = [C_opt, 1.8, 2.2, 2.6]; 

for i = 1:length(contours)
    C = contours(i);
    y_contour = C - 2*sqrt(2)*x1_all; % Phương trình contour
    plot(x1_all, y_contour, '-', 'Color', [0.4 0.4 0.4], 'LineWidth', 0.5);
end

% Nhãn hàm mục tiêu
text(0.65, 0.8, '$2^{1.5}x_1+x_2=\mathrm{const}$', 'Interpreter', 'latex', 'FontSize', 10);

% Trục và Định dạng
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 12);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 12);
set(gca, 'TickDir', 'in');
set(gca, 'XTick', 0:0.1:1.1);
set(gca, 'YTick', 0:0.1:1.1);
set(gca, 'LineWidth', 1);

hold off;
