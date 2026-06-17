% TỐI ƯU HÓA CẤU TRÚC GIÀN
clear; clc; close all;

%% 1. THIẾT LẬP & TẠO LƯỚI
nelx = 8; nely = 4; Vol = 0.1; E = 1; % Thông số cơ bản
[X,Y] = meshgrid(0:nelx, 0:nely); nodes = [X(:) Y(:)]; 
num_nodes = size(nodes,1);
bars = []; map = reshape(1:num_nodes, nely+1, nelx+1);

% Tạo kết nối (Ground Structure)
for i=1:nelx, for j=1:nely
    n = [map(j,i) map(j,i+1); map(j+1,i) map(j+1,i+1)];
    bars = [bars; n(1,1) n(1,2); n(2,1) n(2,2); n(1,1) n(2,1); ...
            n(1,2) n(2,2); n(1,1) n(2,2); n(2,1) n(1,2)];
end; end
bars = unique(sort(bars,2),'rows'); nb = size(bars,1);

% Tính toán hình học
d = nodes(bars(:,2),:) - nodes(bars(:,1),:);
L = sqrt(sum(d.^2,2)); C = d(:,1)./L; S = d(:,2)./L;

%% 2. FEM & TẢI TRỌNG
dofs = 2*num_nodes;
fixed = find(nodes(:,1)==0); 
free = setdiff(1:dofs, [2*fixed-1; 2*fixed]);
load_n = find(nodes(:,1)==nelx & nodes(:,2)==0);
F = sparse(2*load_n, 1, -1, dofs, 1);

% Hàm độ cứng phần tử
KeFunc = @(a,l,c,s) (E*a/l)*[c^2 c*s -c^2 -c*s; c*s s^2 -c*s -s^2; ...
                            -c^2 -c*s c^2 c*s; -c*s -s^2 c*s s^2];

%% 3. VÒNG LẶP TỐI ƯU (OPTIMALITY CRITERIA)
x = Vol*ones(nb,1); loop = 0; change = 1;
while change > 1e-6 && loop < 200
    loop = loop + 1; xold = x;
    
    % Phân tích phần tử hữu hạn
    K = sparse(dofs, dofs);
    for i=1:nb
        idx = [2*bars(i,1)-1:2*bars(i,1), 2*bars(i,2)-1:2*bars(i,2)];
        K(idx,idx) = K(idx,idx) + KeFunc(x(i), L(i), C(i), S(i));
    end
    U = zeros(dofs,1); U(free) = K(free,free) \ F(free);
    
    % Tính độ nhạy
    dc = zeros(nb,1);
    for i=1:nb
        idx = [2*bars(i,1)-1:2*bars(i,1), 2*bars(i,2)-1:2*bars(i,2)];
        dc(i) = -U(idx)' * KeFunc(1, L(i), C(i), S(i)) * U(idx);
    end
    
    % Cập nhật biến thiết kế
    l1=0; l2=1e9; move=0.2;
    while (l2-l1)/(l1+l2) > 1e-6
        lm = 0.5*(l1+l2); xnew = max(1e-9, max(x-move, min(1, min(x+move, x.*sqrt(-dc./(lm*L))))));
        if sum(xnew.*L) > Vol*sum(L), l1=lm; else, l2=lm; end
    end
    change = max(abs(xnew-x)); x = xnew;
    fprintf('Iter: %3d | Obj: %.4f | Vol: %.3f\n', loop, F'*U, sum(x.*L)/sum(L));
end

%% 4. HIỂN THỊ KẾT QUẢ
figure('Color','w'); axis equal off; hold on;
title(['Compliance: ' num2str(F'*U)]);
for i=1:nb
    if x(i) > 0.01 % Chỉ vẽ thanh có kích thước đáng kể
        plot(nodes(bars(i,:),1), nodes(bars(i,:),2), 'k', 'LineWidth', 5*x(i));
    end
end
plot(nodes(fixed,1), nodes(fixed,2), 'k^', 'MarkerFaceColor','k'); % Vẽ gối


