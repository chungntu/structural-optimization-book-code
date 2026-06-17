function Truss_Data=TrussData_10bar

% Modulus of Elasticity (Pa)
E=7e10;  % 70 GPa

% Node coordinates (m)
% L = 10 m
dnkoor=10*[2 1 0;2 0 0;1 1 0;1 0 0;0 1 0;0 0 0];

% Bar connections between nodes
% Bar 1: 5-3   Bar 2: 3-1   Bar 3: 6-4   Bar 4: 4-2
% Bar 5: 4-3   Bar 6: 2-1   Bar 7: 5-4   Bar 8: 6-3
% Bar 9: 3-2   Bar 10: 4-1
eldn=[5 3;3 1;6 4;4 2;4 3;2 1;5 4;6 3;3 2;4 1];

% Support conditions (1=fixed, 0=free) [x y z]
% Nodes 5 and 6 are fixed supports
MesKos=[0 0 1;0 0 1;0 0 1;0 0 1;1 1 1;1 1 1];

% Loading (N) ---> Load(node,:)=[Fx Fy Fz]
% Downward loads at nodes 2 and 4
yuk=zeros(size(dnkoor));
yuk(2,:)=[0 -500000 0];  % 500 kN
yuk(4,:)=[0 -500000 0];  % 500 kN

% Allowable Stress (Pa)
maxGER=1.75e8;  % 175 MPa

% Allowed Displacement (m)
maxYER=0.05;  % 50 mm

% Unit weight (kg/m^3)
GS=2770;

% Design variable bounds (m^2)
LB=ones(1,10)*1e-4;   % 1 cm^2
UB=ones(1,10)*50e-4;   % 50 cm^2

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,...
    'E',E,'yuk',yuk,'maxGER',maxGER,'maxYER',maxYER,'GS',GS,...
    'LB',LB,'UB',UB);