function Truss_Data=TrussData_17bar

% Modulus of Elasticity (Pa)
E=2.1e11;  % 210 GPa (steel)

% Node coordinates (m)
% Unit spacing = 2.5 m
dnkoor=2.5*[0 0 0; 0 1 0; 1 0 0; 1 1 0; 2 0 0; 2 1 0; 3 0 0; 3 1 0; 4 0 0];

% Bar connections between nodes
eldn=[2 4;2 3;1 3;3 4; 4 6;4 5;3 5;5 6;6 8;6 7;5 7;7 8;8 9;7 9;1 4;3 6;5 8];

% Support conditions (1=fixed, 0=free) [x y z]
% Nodes 1 and 2 are fixed supports
MesKos=[1 1 1;1 1 1;0 0 1;0 0 1;0 0 1;0 0 1;0 0 1;0 0 1;0 0 1];

% Loading (N) ---> Load(node,:)=[Fx Fy Fz]
yuk=zeros(size(dnkoor));
yuk(9,:)=[0 -500000 0];  % 500 kN

% Allowable Stress (Pa)
maxGER=3.5e8;  % 350 MPa

% Allowed Displacement (m)
maxYER=0.05;  % 50 mm

% Unit weight (kg/m^3)
GS=7400;  % steel

% Design variable bounds (m^2)
LB=ones(1,17)*1e-4;    % 1 cm^2
UB=ones(1,17)*300e-4;  % 300 cm^2

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,...
    'E',E,'yuk',yuk,'maxGER',maxGER,'maxYER',maxYER,'GS',GS,...
    'LB',LB,'UB',UB);
