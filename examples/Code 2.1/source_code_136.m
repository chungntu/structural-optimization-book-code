clc; clear; close all;

% --- 1. Thông số ban đầu ---
A1_opt = 0.25; % Tọa độ điểm tối ưu
A2_opt = 0.25; 
L_axis = 1.2;  % Giới hạn trục

% --- 2. Khởi tạo đồ thị ---
figure('Color', 'w', 'Units', 'pixels', 'Position', [100, 100, 650, 550]);
hold on; axis off; axis equal;
axis([-0.1 L_axis+0.1 -0.15 L_axis+0.1]);
set(gca, 'FontSize', 12);

% --- 3. Vẽ vùng khả thi (Màu xám) ---
% Tạo biên cong và đa giác vùng khả thi
t = linspace(0, pi/2, 50);
r_curve = 0.95; 
x_curve = A1_opt + r_curve * cos(t); 
y_curve = (A2_opt + r_curve * sin(t)) .* (1 - 0.15*t); 
fill([A1_opt, 1.2, x_curve, A1_opt, A1_opt], ...
     [A2_opt, A2_opt, y_curve, 1.2, A2_opt], ...
     [0.85 0.85 0.85], 'EdgeColor', 'none');

% --- 4. Vẽ biên ràng buộc ---
plot([A1_opt, A1_opt], [A2_opt, 1.2], 'k-', 'LineWidth', 2); % Biên dọc
plot([A1_opt, 1.2], [A2_opt, A2_opt], 'k-', 'LineWidth', 2); % Biên ngang

% --- 5. Vẽ hàm mục tiêu & Gradient ---
delta = 0.25; len_line = 0.35;
cx = A1_opt + delta; cy = A2_opt + delta;
% Đường đồng mức (dốc -1)
plot([cx - len_line, cx + len_line], [cy + len_line, cy - len_line], 'k-', 'LineWidth', 1.5);
% Vector gradient (vuông góc)
quiver(cx, cy, -0.15, -0.15, 'k', 'LineWidth', 1.2, 'MaxHeadSize', 0.8, 'AutoScale', 'off');
text(cx + 0.15, cy + 0.05, '$A_1 + A_2 = \mathrm{const.}$', 'Interpreter', 'latex', 'FontSize', 14);

% --- 6. Vẽ trục tọa độ ---
plot([0 L_axis], [0 0], 'k-', 'LineWidth', 1); % Trục hoành
text(L_axis, -0.05, '$A_1$', 'Interpreter', 'latex', 'FontSize', 14);
plot([0 0], [0 L_axis], 'k-', 'LineWidth', 1); % Trục tung
text(-0.08, L_axis, '$A_2$', 'Interpreter', 'latex', 'FontSize', 14);
% Mũi tên trục
plot(L_axis, 0, 'k>', 'MarkerFaceColor', 'k', 'MarkerSize', 5);
plot(0, L_axis, 'k^', 'MarkerFaceColor', 'k', 'MarkerSize', 5);

% --- 7. Điểm tối ưu ---
plot(A1_opt, A2_opt, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 5);
text(A1_opt + 0.02, A2_opt + 0.04, 'tối ưu', 'FontSize', 12);

% --- 8. Chú thích trục & Công thức ---
% Gióng và ghi chú A1*
plot([A1_opt A1_opt], [0 -0.03], 'k-');
plot([A1_opt A1_opt], [0 A2_opt], 'k:', 'LineWidth', 0.5); 
text(A1_opt - 0.1, -0.15, '$A_1^* = \frac{F \cos \alpha}{\sigma_0}$', 'Interpreter', 'latex', 'FontSize', 14);

% Gióng và ghi chú A2*
plot([0 -0.03], [A2_opt A2_opt], 'k-');
plot([0 A1_opt], [A2_opt A2_opt], 'k:', 'LineWidth', 0.5); 
text(-0.45, A2_opt, '$A_2^* = \frac{F \sin \alpha}{\sigma_0}$', 'Interpreter', 'latex', 'FontSize', 14);

hold off;saveas(gcf, 'figure_2_2.png');
