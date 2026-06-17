function Truss_Data=TrussData_10bar_modal

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

% Frequency limits (Hz)
limfre(1)=7;
limfre(2)=15;
limfre(3)=20;

% Unit weight (kg/m^3)
GS=2770;

% Added masses (kg) at free nodes
add_mass=zeros(size(dnkoor,1),1);
add_mass(1:4)=500; %kg

% Design variable bounds (m^2)
LB=ones(1,10)*1e-4;   % 1 cm^2
UB=ones(1,10)*50e-4;   % 50 cm^2

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,...
    'E',E,'GS',GS,'add_mass',add_mass,'limfre',limfre,...
    'LB',LB,'UB',UB);
