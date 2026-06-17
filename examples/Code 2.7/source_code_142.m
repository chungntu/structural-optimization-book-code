% --- Khởi tạo ---
clc; clear; close all;

% --- 1. Thiết lập dữ liệu ---
% Tạo lưới điểm cho từng vùng ràng buộc
x1_left = linspace(0.001, 0.249, 200);  % Vùng Sigma 3
x1_right = linspace(0.252, 1.0, 500);   % Vùng Sigma 1
x1_all = linspace(0, 1.0, 200);         % Vùng Sigma 2

% --- 2. Các hàm ràng buộc ---
sigma1_func = @(x) (2.*x - 4.*x.^2) ./ (4.*x - 1);
sigma2_func = @(x) (1 / sqrt(2)) - x;
sigma3_func = @(x) (4 .* x.^2) ./ (1 - 4.*x);

% --- 3. Tính toán điểm đặc biệt ---
% Điểm A: Giao của Sigma 1 & Sigma 2
k = 1 / sqrt(2);
x_A = k / (4*k - 1);
y_A = sigma2_func(x_A);

% Điểm B: Giao Sigma 1 với trục hoành
x_B = 0.5;
y_B = 0;

% Điểm C: Giao Sigma 2 với trục hoành (x = 1/sqrt(2))
x_C = 1 / sqrt(2);
y_C = 0;

% --- 4. Vẽ đồ thị ---
figure('Color', 'w', 'Units', 'pixels', 'Position', [100, 100, 700, 600]);
hold on; axis([0 1 0 1]); box on;

% Độ lệch tạo bóng (shadow)
off = 0.015;

% --- Vẽ Sigma 3 (Trái) ---
y_s3 = sigma3_func(x1_left);
mask_s3 = (y_s3 >= -0.1) & (y_s3 <= 1.2);
x3_plot = x1_left(mask_s3);
y3_plot = y_s3(mask_s3);
plot(x3_plot - off, y3_plot, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1); % Bóng
plot(x3_plot, y3_plot, 'k-', 'LineWidth', 1.2); % Chính
text(0.09, 0.89, '$\sigma_3=2\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Vẽ Sigma 2 (Thẳng) ---
y_s2 = sigma2_func(x1_all);
plot(x1_all - off/2, y_s2 - off/2, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1); % Bóng
plot(x1_all, y_s2, 'k-', 'LineWidth', 1.2); % Chính
text(0.02, 0.72, '$\sigma_2=\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Vẽ Sigma 1 (Phải) ---
y_s1 = sigma1_func(x1_right);
mask_s1 = (y_s1 >= -0.1) & (y_s1 <= 1.2);
x1_plot = x1_right(mask_s1);
y1_plot = y_s1(mask_s1);
plot(x1_plot - off, y1_plot, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1); % Bóng
plot(x1_plot, y1_plot, 'k-', 'LineWidth', 1.2); % Chính
text(0.34, 0.79, '$\sigma_1=2\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Đánh dấu các điểm A, B, C ---
plot(x_A, y_A, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x_A + 0.01, y_A + 0.02, 'A', 'FontSize', 12, 'FontWeight', 'bold');

plot(x_B, y_B, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x_B + 0.01, 0.02, 'B', 'FontSize', 12, 'FontWeight', 'bold');

plot(x_C, y_C, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x_C + 0.01, 0.02, 'C', 'FontSize', 12, 'FontWeight', 'bold');

% --- Đường đồng mức (Hàm mục tiêu: f = x1 + x2) ---
% Hệ số góc -1, song song với Sigma 2
contours = [0.9, 1.1, 1.3, 1.5]; 
for i = 1:length(contours)
    C = contours(i);
    % Phương trình: x2 = C - x1
    plot(x1_all, C - x1_all, '-', 'Color', [0.4 0.4 0.4], 'LineWidth', 0.5);
end

% Nhãn hàm mục tiêu
text(0.7, 0.82, '$x_1+x_2=\mathrm{const}$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Định dạng trục ---
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 12);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 12);
set(gca, 'TickDir', 'in', 'LineWidth', 1);
set(gca, 'XTick', 0:0.1:1.1, 'YTick', 0:0.1:1.1);

hold off;
