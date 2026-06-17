% =========================================================================
% Xấp xỉ CONLIN
% =========================================================================

clc; clear; close all;

% 1. ĐỊNH NGHĨA HÀM SỐ VÀ ĐẠO HÀM
g = @(x) x + x.^2 - (1/40).*x.^4;
dg = @(x) 1 + 2.*x - (1/10).*x.^3;

% Tạo miền giá trị x để vẽ
x = linspace(0.1, 9, 500); 
y_true = g(x);

% 2. TÍNH TOÁN TẠI X1 = 1
x1 = 1;
g1 = g(x1);
dg1 = dg(x1);
gL1 = g1 + dg1 .* (x - x1);               % Tuyến tính
gR1 = g1 + dg1 .* (x1 ./ x) .* (x - x1);  % Nghịch đảo

% 3. TÍNH TOÁN TẠI X2 = 6
x2 = 6;
g2 = g(x2);
dg2 = dg(x2);
gL2 = g2 + dg2 .* (x - x2);               % Tuyến tính
gR2 = g2 + dg2 .* (x2 ./ x) .* (x - x2);  % Nghịch đảo

% 4. VẼ ĐỒ THỊ
figure('Color', 'w', 'Position', [100, 100, 800, 500]);
hold on; grid on; box on;

% --- Vẽ các đường ---
plot(x, y_true, 'k-', 'LineWidth', 2);     % Hàm gốc
plot(x, gL1, 'k--', 'LineWidth', 1.5);     % CONLIN tại x=1 (Tuyến tính)
plot(x, gR1, 'k:', 'LineWidth', 1.2);      % So sánh tại x=1
plot(x, gR2, 'b-.', 'LineWidth', 1.5);     % CONLIN tại x=6 (Nghịch đảo)
plot(x, gL2, 'b:', 'LineWidth', 1.2);      % So sánh tại x=6

% --- Đánh dấu điểm ---
plot(x1, g1, 'ro', 'MarkerFaceColor', 'r');
plot(x2, g2, 'ro', 'MarkerFaceColor', 'r');

% 5. TRANG TRÍ & CHÚ THÍCH (TEXT NGANG)
ylim([-5 18]);
xlim([0 9]);
xlabel('x');
ylabel('g(x)');

% Chú thích trực tiếp (Text nằm ngang mặc định)
text(4, 15, 'g', 'FontSize', 16, 'FontWeight', 'bold');

% Khu vực x = 1
text(2.6, 8.5, 'g^C = g^L', 'FontSize', 16); % Đã bỏ Rotation
text(2.6, 4.5, 'g^R', 'FontSize', 16);       % Đã bỏ Rotation

% Khu vực x = 6
text(7.2, 5, 'g^C = g^R', 'FontSize', 16);
text(6.8, -2, 'g^L', 'FontSize', 16);

hold off;