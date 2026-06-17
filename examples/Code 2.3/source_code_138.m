% --- 1. Thiet lap du lieu ---
x1_left = linspace(0.001, 0.499, 200); x1_right = linspace(0.501, 1.0, 200); x1_all = linspace(0, 1, 400);

% Cac ham rang buoc & Tinh toan
sigma1 = @(x) (2.*x.*(x-1))./(1-2.*x); y_sigma1 = sigma1(x1_right);
sigma2 = @(x) (1/sqrt(2))-x;           y_sigma2 = sigma2(x1_all);
sigma3 = @(x) (2.*x.^2)./(1-2.*x);     y_sigma3 = sigma3(x1_left);

% --- 2. Ve do thi ---
figure; set(gcf, 'Position', [100, 100, 600, 525]); hold on; axis([0 1 0 1]); box on;

% Ve cac duong rang buoc (Net dam + Net dut + Text)
plot(x1_right, y_sigma1, 'k-', 'LineWidth', 2); plot(x1_right-0.01, y_sigma1, 'k:', 'LineWidth', 1);
text(0.75, 0.95, '$\sigma_1=\sigma_0$', 'Interpreter', 'latex', 'FontSize', 12);

plot(x1_all, y_sigma2, 'k-', 'LineWidth', 2); plot(x1_all-0.01, y_sigma2-0.01, 'k:', 'LineWidth', 1);
text(0.02, 0.72, '$\sigma_2=\sigma_0$', 'Interpreter', 'latex', 'FontSize', 12);

plot(x1_left, y_sigma3, 'k-', 'LineWidth', 2); plot(x1_left-0.005, y_sigma3+0.01, 'k:', 'LineWidth', 1);
text(0.4, 0.95, '$\sigma_3=-\sigma_0$', 'Interpreter', 'latex', 'FontSize', 12);

% Ve Diem toi uu A
x_A = (2 + sqrt(2))/4; y_A = sqrt(2)/4;
plot(x_A, y_A, 'k+', 'MarkerSize', 10, 'LineWidth', 2);
text(x_A + 0.02, y_A + 0.02, 'A', 'FontSize', 14);

% Ve cac duong dong muc
C_opt = 3*x_A + y_A;
plot(x1_all, C_opt - 3*x1_all, 'k-', 'LineWidth', 0.8);
for os = [-1.5, -0.8, 0.8, 1.5], plot(x1_all, (C_opt+os) - 3*x1_all, 'k-', 'LineWidth', 0.5); end
text(0.5, 0.5, '$3x_1 + x_2 = \mathrm{const}$', 'Interpreter', 'latex', 'FontSize', 12, 'BackgroundColor', 'w');

% Nhan truc & Thiet lap cuoi cung
xlabel('$x_1$', 'Interpreter', 'latex', 'FontSize', 14);
ylabel('$x_2$', 'Interpreter', 'latex', 'FontSize', 14);
set(gca, 'TickDir', 'in', 'Layer', 'top'); hold off;
