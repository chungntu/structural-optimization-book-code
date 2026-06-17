% =========================================================================
% X\u1ea5p x\u1ec9 CONLIN
% =========================================================================

clc; clear; close all;

% 1. \u0110\u1ecaNH NGH\u0128A H\u00c0M S\u1ed0 V\u00c0 \u0110\u1ea0O H\u00c0M
g = @(x) x + x.^2 - (1/40).*x.^4;
dg = @(x) 1 + 2.*x - (1/10).*x.^3;

% T\u1ea1o mi\u1ec1n gi\u00e1 tr\u1ecb x \u0111\u1ec3 v\u1ebd
x = linspace(0.1, 9, 500);
y_true = g(x);

% 2. T\u00cdNH TO\u00c1N T\u1ea0I X1 = 1
x1 = 1;
g1 = g(x1);
dg1 = dg(x1);
gL1 = g1 + dg1 .* (x - x1);               % Tuy\u1ebfn t\u00ednh
gR1 = g1 + dg1 .* (x1 ./ x) .* (x - x1);  % Ngh\u1ecbch \u0111\u1ea3o

% 3. T\u00cdNH TO\u00c1N T\u1ea0I X2 = 6
x2 = 6;
g2 = g(x2);
dg2 = dg(x2);
gL2 = g2 + dg2 .* (x - x2);               % Tuy\u1ebfn t\u00ednh
gR2 = g2 + dg2 .* (x2 ./ x) .* (x - x2);  % Ngh\u1ecbch \u0111\u1ea3o

% 4. V\u1ebc \u0110\u1ed2 TH\u1eca
figure('Color', 'w', 'Position', [100, 100, 800, 500]);
hold on; grid on; box on;

% --- V\u1ebd c\u00e1c \u0111\u01b0\u1eddng ---
plot(x, y_true, 'k-', 'LineWidth', 2);     % H\u00e0m g\u1ed1c
plot(x, gL1, 'k--', 'LineWidth', 1.5);     % CONLIN t\u1ea1i x=1 (Tuy\u1ebfn t\u00ednh)
plot(x, gR1, 'k:', 'LineWidth', 1.2);      % So s\u00e1nh t\u1ea1i x=1
plot(x, gR2, 'b-.', 'LineWidth', 1.5);     % CONLIN t\u1ea1i x=6 (Ngh\u1ecbch \u0111\u1ea3o)
plot(x, gL2, 'b:', 'LineWidth', 1.2);      % So s\u00e1nh t\u1ea1i x=6

% --- \u0110\u00e1nh d\u1ea5u \u0111i\u1ec3m ---
plot(x1, g1, 'ro', 'MarkerFaceColor', 'r');
plot(x2, g2, 'ro', 'MarkerFaceColor', 'r');

% 5. TRANG TR\u00cd & CH\u00da TH\u00cdCH (TEXT NGANG)
ylim([-5 18]);
xlim([0 9]);
xlabel('x');
ylabel('g(x)');

% Ch\u00fa th\u00edch tr\u1ef1c ti\u1ebfp (Text n\u1eb1m ngang m\u1eb7c \u0111\u1ecbnh)
text(4, 15, 'g', 'FontSize', 16, 'FontWeight', 'bold');

% Khu v\u1ef1c x = 1
text(2.6, 8.5, 'g^C = g^L', 'FontSize', 16); % \u0110\u00e3 b\u1ecf Rotation
text(2.6, 4.5, 'g^R', 'FontSize', 16);       % \u0110\u00e3 b\u1ecf Rotation

% Khu v\u1ef1c x = 6
text(7.2, 5, 'g^C = g^R', 'FontSize', 16);
text(6.8, -2, 'g^L', 'FontSize', 16);

hold off;

