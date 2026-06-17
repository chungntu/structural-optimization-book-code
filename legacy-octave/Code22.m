rt3 = sqrt(3);
% --- 1. Thi\u1ebft l\u1eadp th\u00f4ng s\u1ed1 & L\u01b0\u1edbi ---
x1_int = rt3/4; x2_int = 1/rt3;         % Giao \u0111i\u1ec3m tr\u1ee5c
x1_opt = rt3/7; x2_opt = rt3/7;         % \u0110i\u1ec3m t\u1ed1i \u01b0u
[X1, X2] = meshgrid(linspace(1e-3, 0.9, 800), linspace(1e-3, 0.9, 800));
F = 4./(3*X1) + 1./X2;                  % H\u00e0m m\u1ee5c ti\u00eau

% --- 2. V\u1ebd \u0111\u1ed3 th\u1ecb ---
figure('Color', 'w'); hold on; box off; pbaspect([1 1 1]);

% Mi\u1ec1n ch\u1ea5p nh\u1eadn (Tam gi\u00e1c x\u00e1m)
fill([0, 0, x1_int], [0, x2_int, 0], [0.85 0.85 0.85], 'EdgeColor', 'none');

% \u0110\u01b0\u1eddng r\u00e0ng bu\u1ed9c
x_line = linspace(0, x1_int, 200);
plot(x_line, x2_int - (4/3)*x_line, 'k', 'LineWidth', 2);

% \u0110\u01b0\u1eddng \u0111\u1ed3ng m\u1ee9c & Nh\u00e3n
[C, h] = contour(X1, X2, F, [7, 9.43, 14], 'k', 'LineWidth', 1);
clabel(C, h, 'FontSize', 10, 'LabelSpacing', 300);

% \u0110\u00e1nh d\u1ea5u \u0111i\u1ec3m t\u1ed1i \u01b0u
plot(x1_opt, x2_opt, 'ko', 'MarkerSize', 4, 'MarkerFaceColor', 'k');
text(x1_opt + 0.02, x2_opt + 0.02, 'opt.', 'FontSize', 10);

% --- 3. \u0110\u1ecbnh d\u1ea1ng tr\u1ee5c ---
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 10);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 10);
axis([0 0.9 0 0.9]);

% C\u00e0i \u0111\u1eb7t Ticks & Font LaTeX
set(gca, 'XTick', x1_int, 'XTickLabel', {'$\frac{\sqrt{3}}{4}$'}, ...
         'YTick', x2_int, 'YTickLabel', {'$\frac{1}{\sqrt{3}}$'}, ...
         'TickLabelInterpreter', 'latex', 'FontSize', 10);
hold off;


