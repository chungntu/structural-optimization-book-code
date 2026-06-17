% --- Kh\u1edfi t\u1ea1o ---
clc; clear; close all;

% --- 1. Thi\u1ebft l\u1eadp d\u1eef li\u1ec7u ---
% T\u1ea1o l\u01b0\u1edbi \u0111i\u1ec3m cho t\u1eebng v\u00f9ng
x1_left = linspace(0.001, 0.249, 200);  % V\u00f9ng Sigma 3
x1_right = linspace(0.252, 1.0, 500);   % V\u00f9ng Sigma 1
x1_all = linspace(0, 1.0, 200);         % V\u00f9ng Sigma 2

% --- 2. C\u00e1c h\u00e0m r\u00e0ng bu\u1ed9c ---
sigma1_func = @(x) (2.*x - 4.*x.^2) ./ (4.*x - 1);
sigma2_func = @(x) (1 / sqrt(2)) - x;
sigma3_func = @(x) (4 .* x.^2) ./ (1 - 4.*x);

% --- 3. T\u00ednh c\u00e1c \u0111i\u1ec3m \u0111\u1eb7c bi\u1ec7t ---
k = 1 / sqrt(2);
x_A = k / (4*k - 1);
y_A = sigma2_func(x_A);
x_B = 0.5;
y_B = 0;

% --- 4. V\u1ebd \u0111\u1ed3 th\u1ecb ---
figure('Color', 'w', 'Units', 'pixels', 'Position', [100, 100, 700, 600]);
hold on; axis([0 1 0 1]); box on;

% \u0110\u1ed9 l\u1ec7ch n\u00e9t \u0111\u1ee9t (t\u1ea1o b\u00f3ng)
off = 0.015;

% --- V\u1ebd Sigma 3 (Tr\u00e1i) ---
y_s3 = sigma3_func(x1_left);
mask_s3 = (y_s3 >= -0.1) & (y_s3 <= 1.2);
x3_plot = x1_left(mask_s3);
y3_plot = y_s3(mask_s3);
% 1. \u0110\u01b0\u1eddng b\u00f3ng
plot(x3_plot - off, y3_plot, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1);
% 2. \u0110\u01b0\u1eddng ch\u00ednh
plot(x3_plot, y3_plot, 'k-', 'LineWidth', 1.2);
text(0.09, 0.92, '$\sigma_3=2\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- V\u1ebd Sigma 2 (Th\u1eb3ng) ---
y_s2 = sigma2_func(x1_all);
% 1. \u0110\u01b0\u1eddng b\u00f3ng
plot(x1_all - off/2, y_s2 - off/2, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1);
% 2. \u0110\u01b0\u1eddng ch\u00ednh
plot(x1_all, y_s2, 'k-', 'LineWidth', 1.2);
text(0.02, 0.72, '$\sigma_2=\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- V\u1ebd Sigma 1 (Ph\u1ea3i) ---
y_s1 = sigma1_func(x1_right);
mask_s1 = (y_s1 >= -0.1) & (y_s1 <= 1.2);
x1_plot = x1_right(mask_s1);
y1_plot = y_s1(mask_s1);
% 1. \u0110\u01b0\u1eddng b\u00f3ng
plot(x1_plot - off, y1_plot, ':', 'Color', [0.2 0.2 0.2], 'LineWidth', 1);
% 2. \u0110\u01b0\u1eddng ch\u00ednh
plot(x1_plot, y1_plot, 'k-', 'LineWidth', 1.2);
text(0.37, 0.55, '$\sigma_1=2\sigma_0$', 'Interpreter', 'latex', 'FontSize', 10);

% --- Chi ti\u1ebft kh\u00e1c ---
% \u0110i\u1ec3m A
plot(x_A, y_A, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x_A + 0.02, y_A + 0.02, 'A', 'FontSize', 12, 'FontWeight', 'bold');

% \u0110i\u1ec3m B
plot(x_B, y_B, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x_B + 0.01, 0.02, 'B', 'FontSize', 12, 'FontWeight', 'bold');

% \u0110\u01b0\u1eddng \u0111\u1ed3ng m\u1ee9c
contours = [1.1, 1.6, 2.1, 2.6];
for i = 1:length(contours)
    C = contours(i);
    plot(x1_all, C - 2*x1_all, '-', 'Color', [0.4 0.4 0.4], 'LineWidth', 0.5);
end

% Nh\u00e3n ph\u01b0\u01a1ng tr\u00ecnh
text(0.69, 0.75, '$2x_1+x_2=\mathrm{const}$', 'Interpreter', 'latex', 'FontSize', 10);

% Tr\u1ee5c v\u00e0 \u0110\u1ecbnh d\u1ea1ng
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 12);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 12);
set(gca, 'TickDir', 'in');
set(gca, 'XTick', 0:0.1:1.1);
set(gca, 'YTick', 0:0.1:1.1);
set(gca, 'LineWidth', 1);
hold off;


