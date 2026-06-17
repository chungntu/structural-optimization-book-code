% SCRIPT: 3D_KKT_Visualization_Final.m
% MÔ TẢ:
%   Minh họa trực quan điều kiện Karush-Kuhn-Tucker (KKT) trong không gian 3D.
%   Biểu diễn điểm tiếp xúc giữa mặt cầu mục tiêu f(x) và mặt phẳng ràng buộc g(x).
%   Hiển thị tính đồng phương của các vector gradient tại điểm tối ưu.
% 
%% 1. Khởi tạo môi trường và Cấu hình đồ họa
clear; clc; close all;

figure('Color', 'w', 'Position', [100, 100, 900, 800]); 
hold on;
grid on; box on; axis equal; 

%% 2. Định nghĩa Thông số Bài toán
% Điểm tối ưu cục bộ (Local Optimum / Stationary Point)
Opt = [1, 1, 1]; 

% Bán kính mặt cầu tại điểm tối ưu
R_opt = sqrt(3); 

%% 3. Trực quan hóa Mặt phẳng Ràng buộc (Constraint Plane)
% Tạo lưới tọa độ cho mặt phẳng
[X_plane, Y_plane] = meshgrid(linspace(-1, 4.5, 50)); 

% Phương trình mặt phẳng: z = 3 - x - y
Z_plane = 3 - X_plane - Y_plane;

% Vẽ mặt phẳng ràng buộc
surf(X_plane, Y_plane, Z_plane, 'FaceColor', [0.7 0.7 0.9], ...
     'FaceAlpha', 0.5, 'EdgeColor', 'none');

% Ghi chú phương trình ràng buộc g(x)
text(-2.9, 2.4, 1.5, '$g(x): x + y + z = 3$', ...
    'Interpreter', 'latex', 'FontSize', 16, 'Color', 'k', 'FontWeight', 'bold');

%% 4. Trực quan hóa Hàm mục tiêu (Objective Function)
% Tạo dữ liệu mặt cầu
[Xs, Ys, Zs] = sphere(80); 

% Vẽ mặt cầu mục tiêu
surf(Xs*R_opt, Ys*R_opt, Zs*R_opt, 'FaceColor', [1 0.8 0.4], ...
     'FaceAlpha', 0.4, 'EdgeColor', 'none');

% Ghi chú phương trình hàm mục tiêu f(x)
text(-1.16, -3.58, 1.82, '$f(x): x^2 + y^2 + z^2 = 3$', ...
    'Interpreter', 'latex', 'FontSize', 16, 'Color', [0.8 0.4 0], 'FontWeight', 'bold');

%% 5. Hiển thị Vector Gradient tại Điểm tối ưu
% Thiết lập hệ số tỉ lệ (Scaling factors) để hiển thị vector rõ ràng hơn
scale_g = 1.8;  % Hệ số tỉ lệ cho vector gradient ràng buộc
scale_f = 2.8;  % Hệ số tỉ lệ cho vector gradient hàm mục tiêu

% --- Vector Gradient của Ràng buộc (Nabla g) ---
% Vẽ vector pháp tuyến mặt phẳng (Màu đỏ)
quiver3(Opt(1), Opt(2), Opt(3), scale_g, scale_g, scale_g, ...
    'r', 'LineWidth', 4, 'MaxHeadSize', 0.5, 'AutoScale', 'off');

% Nhãn cho vector Nabla g
text(Opt(1)+scale_g, Opt(2)+scale_g, Opt(3)+scale_g - 0.2, '$\nabla g$', ...
    'Interpreter', 'latex', 'FontSize', 16, 'Color', 'r', 'FontWeight', 'bold');

% --- Vector Gradient của Hàm mục tiêu (Nabla f) ---
% Vẽ vector pháp tuyến mặt cầu (Màu xanh dương)
quiver3(Opt(1), Opt(2), Opt(3), scale_f, scale_f, scale_f, ...
    'b', 'LineWidth', 3, 'MaxHeadSize', 0.5, 'AutoScale', 'off');

% Nhãn cho vector Nabla f
text(Opt(1)+scale_f, Opt(2)+scale_f, Opt(3)+scale_f, '$\nabla f$', ...
    'Interpreter', 'latex', 'FontSize', 16, 'Color', 'b', 'FontWeight', 'bold');

%% 6. Cấu hình Ánh sáng và Góc nhìn (Camera & Lighting)
% Thiết lập ánh sáng Gouraud để tăng chiều sâu 3D
camlight left; camlight right;
lighting gouraud; 

% Đặt góc nhìn cố định
view(48, 37); 

% Thiết lập giới hạn không gian hiển thị
xlim([-1 5]); ylim([-1 5]); zlim([-1 5]);

hold off;