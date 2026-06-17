% =========================================================================
% Phương pháp MMA
% =========================================================================

clc; clear; close all;

% 1. ĐỊNH NGHĨA HÀM SỐ VÀ ĐẠO HÀM
g = @(x) x + x.^2 - (1/40).*x.^4;
dg = @(x) 1 + 2.*x - (1/10).*x.^3;

% Điểm khảo sát x0 = 1
x0 = 1;
g0 = g(x0);      % g(1) = 1.975
dg0 = dg(x0);    % g'(1) = 2.9

% Miền giá trị x để vẽ
x = linspace(-6, 6, 2000); % Tăng điểm ảnh để vẽ mượt hơn
y_true = g(x);

% 2. CÁC GIÁ TRỊ TIỆM CẬN TRÊN (U)
U_values = [1.5, 4, 20, 10000];
line_styles = {'--', ':', '-.', '-'}; 
line_colors = {'k', 'k', 'k', 'k'};   

% 3. VẼ ĐỒ THỊ
figure('Color', 'w', 'Position', [100, 100, 800, 600]);
hold on; grid on; box on;

% Vẽ hàm gốc g(x)
plot(x, y_true, 'k-', 'LineWidth', 2, 'DisplayName', 'Hàm gốc g(x)');

% Vòng lặp tính và vẽ MMA
for i = 1:length(U_values)
    U = U_values(i);
    
    % Tính toán hệ số (đạo hàm dương -> dùng U)
    p = (U - x0)^2 * dg0;
    r = g0 - p / (U - x0);
    g_mma = r + p ./ (U - x);
    
    % --- XỬ LÝ RIÊNG THEO YÊU CẦU ---
    % Với U = 1.5
    if U == 1.5
        g_mma(x >= 1.5) = NaN;
    end
    
    % Với U = 4
        if U == 4
         g_mma(abs(x - U) < 0.05) = NaN; % Chỉ ngắt tại điểm gián đoạn
    end

    % Giới hạn hiển thị trục y để hình không bị biến dạng
    g_mma(g_mma > 50 | g_mma < -50) = NaN;

    % Thiết lập Label
    if U == 10000
        legend_label = sprintf('Xấp xỉ MMA với U^0=10^4');
    else
        legend_label = sprintf('Xấp xỉ MMA với U^0=%.1f', U);
    end
    
    % Vẽ đường cong
    plot(x, g_mma, line_styles{i}, 'Color', line_colors{i}, ...
         'LineWidth', 1.2, 'DisplayName', legend_label);
     
    % Vẽ đường tiệm cận đứng minh họa cho U=1.5 và U=4
    if U <= 4
         xline(U, 'k:', 'LineWidth', 0.5, 'HandleVisibility', 'off');
    end
end

% 4. TRANG TRÍ
xlim([-6 6]);
ylim([-10 40]);
xlabel('x');
ylabel('g(x)');

% Đánh dấu điểm x0
plot(x0, g0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 16, 'HandleVisibility', 'off');
text(x0, g0-3, 'x^0=1', 'HorizontalAlignment', 'center');

legend('Location', 'northwest');
hold off;