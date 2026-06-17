clc; clear; close all;

% --- 1. Th\u00f4ng s\u1ed1 ban \u0111\u1ea7u ---
A1_opt = 0.25; % T\u1ecda \u0111\u1ed9 \u0111i\u1ec3m t\u1ed1i \u01b0u
A2_opt = 0.25;
L_axis = 1.2;  % Gi\u1edbi h\u1ea1n tr\u1ee5c

% --- 2. Kh\u1edfi t\u1ea1o \u0111\u1ed3 th\u1ecb ---
figure('Color', 'w', 'Units', 'pixels', 'Position', [100, 100, 650, 550]);
hold on; axis off; axis equal;
axis([-0.1 L_axis+0.1 -0.15 L_axis+0.1]);
set(gca, 'FontSize', 12);

% --- 3. V\u1ebd v\u00f9ng kh\u1ea3 thi (M\u00e0u x\u00e1m) ---
% T\u1ea1o bi\u00ean cong v\u00e0 \u0111a gi\u00e1c v\u00f9ng kh\u1ea3 thi
t = linspace(0, pi/2, 50);
r_curve = 0.95;
x_curve = A1_opt + r_curve * cos(t);
y_curve = (A2_opt + r_curve * sin(t)) .* (1 - 0.15*t);
fill([A1_opt, 1.2, x_curve, A1_opt, A1_opt], ...
     [A2_opt, A2_opt, y_curve, 1.2, A2_opt], ...
     [0.85 0.85 0.85], 'EdgeColor', 'none');

% --- 4. V\u1ebd bi\u00ean r\u00e0ng bu\u1ed9c ---
plot([A1_opt, A1_opt], [A2_opt, 1.2], 'k-', 'LineWidth', 2); % Bi\u00ean d\u1ecdc
plot([A1_opt, 1.2], [A2_opt, A2_opt], 'k-', 'LineWidth', 2); % Bi\u00ean ngang

% --- 5. V\u1ebd h\u00e0m m\u1ee5c ti\u00eau & Gradient ---
delta = 0.25; len_line = 0.35;
cx = A1_opt + delta; cy = A2_opt + delta;
% \u0110\u01b0\u1eddng \u0111\u1ed3ng m\u1ee9c (d\u1ed1c -1)
plot([cx - len_line, cx + len_line], [cy + len_line, cy - len_line], 'k-', 'LineWidth', 1.5);
% Vector gradient (vu\u00f4ng g\u00f3c)
quiver(cx, cy, -0.15, -0.15, 'k', 'LineWidth', 1.2, 'MaxHeadSize', 0.8, 'AutoScale', 'off');
text(cx + 0.15, cy + 0.05, '$A_1 + A_2 = \mathrm{const.}$', 'Interpreter', 'latex', 'FontSize', 14);

% --- 6. V\u1ebd tr\u1ee5c t\u1ecda \u0111\u1ed9 ---
plot([0 L_axis], [0 0], 'k-', 'LineWidth', 1); % Tr\u1ee5c ho\u00e0nh
text(L_axis, -0.05, '$A_1$', 'Interpreter', 'latex', 'FontSize', 14);
plot([0 0], [0 L_axis], 'k-', 'LineWidth', 1); % Tr\u1ee5c tung
text(-0.08, L_axis, '$A_2$', 'Interpreter', 'latex', 'FontSize', 14);
% M\u0169i t\u00ean tr\u1ee5c
plot(L_axis, 0, 'k>', 'MarkerFaceColor', 'k', 'MarkerSize', 5);
plot(0, L_axis, 'k^', 'MarkerFaceColor', 'k', 'MarkerSize', 5);

% --- 7. \u0110i\u1ec3m t\u1ed1i \u01b0u ---
plot(A1_opt, A2_opt, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 5);
text(A1_opt + 0.02, A2_opt + 0.04, 't\u1ed1i \u01b0u', 'FontSize', 12);

% --- 8. Ch\u00fa th\u00edch tr\u1ee5c & C\u00f4ng th\u1ee9c ---
% Gi\u00f3ng v\u00e0 ghi ch\u00fa A1*
plot([A1_opt A1_opt], [0 -0.03], 'k-');
plot([A1_opt A1_opt], [0 A2_opt], 'k:', 'LineWidth', 0.5);
text(A1_opt - 0.1, -0.15, '$A_1^* = \frac{F \cos \alpha}{\sigma_0}$', 'Interpreter', 'latex', 'FontSize', 14);

% Gi\u00f3ng v\u00e0 ghi ch\u00fa A2*
plot([0 -0.03], [A2_opt A2_opt], 'k-');
plot([0 A1_opt], [A2_opt A2_opt], 'k:', 'LineWidth', 0.5);
text(-0.45, A2_opt, '$A_2^* = \frac{F \sin \alpha}{\sigma_0}$', 'Interpreter', 'latex', 'FontSize', 14);

hold off;

