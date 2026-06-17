function Truss_Data=TrussData_10bar_modal

% Modulus of Elasticity
E=6.89e10;

% Node coordinates
dnkoor=9.144*[2 1 0;2 0 0;1 1 0;1 0 0;0 1 0;0 0 0];

% Bar connections between nodes
eldn=[5 3;3 1;6 4;4 2;4 3;2 1;5 4;6 3;3 2;4 1];

% Support conditions
MesKos=[0 0 1;0 0 1;0 0 1;0 0 1;1 1 1;1 1 1];

% Frequency limits (Hz)
limfre(1)=7;
limfre(2)=15;
limfre(3)=20;

% Unit weight
GS=2770;%kg/m^3

% added masses
add_mass=zeros(size(dnkoor,1),1);
add_mass(1:4)=454; %kg

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,'E',E,'GS',GS,'add_mass',add_mass,'limfre',limfre);

