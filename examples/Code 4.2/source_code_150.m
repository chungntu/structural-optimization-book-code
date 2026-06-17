% TỐI ƯU HÓA BẰNG QUY HOẠCH TOÀN PHƯƠNG TUẦN TỰ (SQP)
% lưu ý cần Optimization Toolbox
%     min   f(x) = (x1 - 5)^2 + (x2 - 4)^2
%     s.t.  g1(x): x1 + 2*x2 - 10 <= 0
%           g2(x): x1 - 4 <= 0
clc; clear;
% 1. Khởi tạo thông số ban đầu
x = [0; 0];          % Điểm khởi tạo x0
tol = 1e-6;          % Sai số cho phép để dừng thuật toán
max_iter = 50;       % Số vòng lặp tối đa
H = eye(2);          % Khởi tạo ma trận Hessian
% 2. Vòng lặp chính SQP (Sequential Quadratic Programming)
for k = 1:max_iter
    % Bước A: Tính toán giá trị tại điểm lặp hiện tại và đạo hàm
    f_val = (x(1)-5)^2 + (x(2)-4)^2;
    grad_f = [2*(x(1)-5); 
              2*(x(2)-4)]; 
    % Tính giá trị các hàm ràng buộc và ma trận đạo hàm các ràng buộc
    g_val = [x(1) + 2*x(2) - 10; x(1) - 4];
    grad_g = [1, 2; 1, 0];
    % Bước B: Thiết lập và giải bài toán con quy hoạch toàn phương
    opts = optimoptions('quadprog', 'Display', 'off');
    [d, ~, exitflag] = quadprog(H, grad_f, grad_g, -g_val, [],[],[],[],[], opts);
    % Bước C: Cập nhật nghiệm và kiểm tra điều kiện hội tụ
    x = x + d;
    if norm(d) < tol
        break; 
    end
end
% 3. Hiển thị kết quả tối ưu
fprintf('Nghiệm tối ưu x*:         [%0.4f; %0.4f]\n', x);
fprintf('Giá trị hàm mục tiêu f*:  %0.4f\n', (x(1)-5)^2 + (x(2)-4)^2);