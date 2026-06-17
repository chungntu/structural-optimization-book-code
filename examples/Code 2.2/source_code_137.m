rt3 = sqrt(3);
% --- 1. Thiết lập thông số & Lưới ---
x1_int = rt3/4; x2_int = 1/rt3;         % Giao điểm trục
x1_opt = rt3/7; x2_opt = rt3/7;         % Điểm tối ưu
[X1, X2] = meshgrid(linspace(1e-3, 0.9, 800), linspace(1e-3, 0.9, 800));
F = 4./(3*X1) + 1./X2;                  % Hàm mục tiêu

% --- 2. Vẽ đồ thị ---
figure('Color', 'w'); hold on; box off; pbaspect([1 1 1]);

% Miền chấp nhận (Tam giác xám)
fill([0, 0, x1_int], [0, x2_int, 0], [0.85 0.85 0.85], 'EdgeColor', 'none');

% Đường ràng buộc
x_line = linspace(0, x1_int, 200);
plot(x_line, x2_int - (4/3)*x_line, 'k', 'LineWidth', 2);

% Đường đồng mức & Nhãn
[C, h] = contour(X1, X2, F, [7, 9.43, 14], 'k', 'LineWidth', 1);
clabel(C, h, 'FontSize', 10, 'LabelSpacing', 300);

% Đánh dấu điểm tối ưu
plot(x1_opt, x2_opt, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x1_opt + 0.02, x2_opt + 0.02, 'opt.', 'FontSize', 10);

% --- 3. Định dạng trục ---
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 10);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 10);
axis([0 0.9 0 0.9]);

% Cài đặt Ticks & Font LaTeX
set(gca, 'XTick', x1_int, 'XTickLabel', {'$\frac{\sqrt{3}}{4}$'}, ...
         'YTick', x2_int, 'YTickLabel', {'$\frac{1}{\sqrt{3}}$'}, ...
         'TickLabelInterpreter', 'latex', 'FontSize', 10);
hold off;
