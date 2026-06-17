%% TRỰC QUAN HÓA TÍNH LỒI - LÕM
clc; clear; close all;

% Dữ liệu lưới cho bề mặt 3D
[X, Y] = meshgrid(linspace(-2, 2, 60));

%% HÌNH 1: HÀM LỒI CHẶT f(x) = x^2 (Parabol)
figure('Color', 'w', 'Position', [50, 400, 500, 400]);
x1 = linspace(-2, 2, 100);
y1 = x1.^2;
plot(x1, y1, 'b-', 'LineWidth', 2.5);
grid on; box on;
title('\bf $$f(x_1) = x_1^2$$', 'Interpreter', 'latex', 'FontSize', 14);
xlabel('$$x_1$$', 'Interpreter', 'latex', 'FontSize', 12);
ylabel('$$f$$', 'Interpreter', 'latex', 'FontSize', 12);
set(gca, 'FontSize', 10);

%% HÌNH 2: HÀM LỒI (KHÔNG CHẶT)
% f(x1, x2) = x1^2 (Máng xối)
figure('Color', 'w', 'Position', [560, 400, 500, 400]);
Z1 = X.^2; 
surf(X, Y, Z1, 'EdgeColor', 'none', 'FaceAlpha', 0.85);
hold on;
colormap('parula');
% Đường chỉ thị đáy phẳng (trục dọc)
plot3([0 0], [-2 2], [0 0], 'r-', 'LineWidth', 3);
view(45, 20); 
axis square; grid on; box on;
camlight; lighting gouraud; 
title('\bf $$f(x_1, x_2) = x_1^2$$', 'Interpreter', 'latex', 'FontSize', 14);
xlabel('$$x_1$$', 'Interpreter', 'latex');
ylabel('$$x_2$$', 'Interpreter', 'latex');
zlabel('$$f$$', 'Interpreter', 'latex');
rotate3d on;

%% HÌNH 3: HÀM KHÔNG LỒI - KHÔNG LÕM f(x1, x2) = x1 * x2 (Yên ngựa)
figure('Color', 'w', 'Position', [1070, 400, 500, 400]);
Z2 = X .* Y;
surf(X, Y, Z2, 'EdgeColor', 'none', 'FaceAlpha', 0.9);
hold on;
colormap('jet');
view(15, 15);
axis square; grid on; box on;
camlight; lighting gouraud;
title('\bf $$f(x_1, x_2) = x_1 x_2$$', 'Interpreter', 'latex', 'FontSize', 14);
xlabel('$$x_1$$', 'Interpreter', 'latex');
ylabel('$$x_2$$', 'Interpreter', 'latex');
zlabel('$$f$$', 'Interpreter', 'latex');
rotate3d on;