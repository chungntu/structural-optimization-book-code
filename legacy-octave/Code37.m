% =========================================================================
% Ph\u01b0\u01a1ng ph\u00e1p MMA
% =========================================================================

clc; clear; close all;

% 1. \u0110\u1ecaNH NGH\u0128A H\u00c0M S\u1ed0 V\u00c0 \u0110\u1ea0O H\u00c0M
g = @(x) x + x.^2 - (1/40).*x.^4;
dg = @(x) 1 + 2.*x - (1/10).*x.^3;

% \u0110i\u1ec3m kh\u1ea3o s\u00e1t x0 = 1
x0 = 1;
g0 = g(x0);      % g(1) = 1.975
dg0 = dg(x0);    % g'(1) = 2.9

% Mi\u1ec1n gi\u00e1 tr\u1ecb x \u0111\u1ec3 v\u1ebd
x = linspace(-6, 6, 2000); % T\u0103ng \u0111i\u1ec3m \u1ea3nh \u0111\u1ec3 v\u1ebd m\u01b0\u1ee3t h\u01a1n
y_true = g(x);

% 2. C\u00c1C GI\u00c1 TR\u1eca TI\u1ec6M C\u1eacN TR\u00caN (U)
U_values = [1.5, 4, 20, 10000];
line_styles = {'--', ':', '-.', '-'};
line_colors = {'k', 'k', 'k', 'k'};

% 3. V\u1ebc \u0110\u1ed2 TH\u1eca
figure('Color', 'w', 'Position', [100, 100, 800, 600]);
hold on; grid on; box on;

% V\u1ebd h\u00e0m g\u1ed1c g(x)
plot(x, y_true, 'k-', 'LineWidth', 2, 'DisplayName', 'H\u00e0m g\u1ed1c g(x)');

% V\u00f2ng l\u1eb7p t\u00ednh v\u00e0 v\u1ebd MMA
for i = 1:length(U_values)
    U = U_values(i);

    % T\u00ednh to\u00e1n h\u1ec7 s\u1ed1 (\u0111\u1ea1o h\u00e0m d\u01b0\u01a1ng -> d\u00f9ng U)
    p = (U - x0)^2 * dg0;
    r = g0 - p / (U - x0);
    g_mma = r + p ./ (U - x);

    % --- X\u1eec L\u00dd RI\u00caNG THEO Y\u00caU C\u1ea6U ---
    % V\u1edbi U = 1.5
    if U == 1.5
        g_mma(x >= 1.5) = NaN;
    end

    % V\u1edbi U = 4
        if U == 4
         g_mma(abs(x - U) < 0.05) = NaN; % Ch\u1ec9 ng\u1eaft t\u1ea1i \u0111i\u1ec3m gi\u00e1n \u0111o\u1ea1n
    end

    % Gi\u1edbi h\u1ea1n hi\u1ec3n th\u1ecb tr\u1ee5c y \u0111\u1ec3 h\u00ecnh kh\u00f4ng b\u1ecb bi\u1ebfn d\u1ea1ng
    g_mma(g_mma > 50 | g_mma < -50) = NaN;

    % Thi\u1ebft l\u1eadp Label
    if U == 10000
        legend_label = sprintf('X\u1ea5p x\u1ec9 MMA v\u1edbi U^0=10^4');
    else
        legend_label = sprintf('X\u1ea5p x\u1ec9 MMA v\u1edbi U^0=%.1f', U);
    end

    % V\u1ebd \u0111\u01b0\u1eddng cong
    plot(x, g_mma, line_styles{i}, 'Color', line_colors{i}, ...
         'LineWidth', 1.2, 'DisplayName', legend_label);

    % V\u1ebd \u0111\u01b0\u1eddng ti\u1ec7m c\u1eadn \u0111\u1ee9ng minh h\u1ecda cho U=1.5 v\u00e0 U=4
    if U <= 4
         xline(U, 'k:', 'LineWidth', 0.5, 'HandleVisibility', 'off');
    end
end

% 4. TRANG TR\u00cd
xlim([-6 6]);
ylim([-10 40]);
xlabel('x');
ylabel('g(x)');

% \u0110\u00e1nh d\u1ea5u \u0111i\u1ec3m x0
plot(x0, g0, 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 16, 'HandleVisibility', 'off');
text(x0, g0-3, 'x^0=1', 'HorizontalAlignment', 'center');

legend('Location', 'northwest');
hold off;


