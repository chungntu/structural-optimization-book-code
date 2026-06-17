function Truss_Data=TrussData_17bar

% Modulus of Elasticity (psi)
E=3e7;

% Node coordinates
dnkoor=100*[0 0 0; 0 1 0; 1 0 0;1 1 0;2 0 0;2 1 0;3 0 0;3 1 0;4 0 0]; 

% Bar connections between nodes
eldn=[2 4;2 3;1 3;3 4; 4 6;4 5;3 5;5 6;6 8;6 7;5 7;7 8;8 9;7 9;1 4;3 6;5 8];
    
% Support conditions
MesKos=[1 1 1;1 1 1;0 0 1;0 0 1;0 0 1;0 0 1;0 0 1;0 0 1;0 0 1];

% Loading     ----- > Load(dn_no,:)=[x y z] (lbs)
yuk=zeros(size(dnkoor));
yuk(9,:)=[0 -1e5 0];

% Allowable Stress (psi)
maxGER=50000;%psi

% Allowed Displacement
maxYER=2;   %inch

% Unit weight
GS=0.268;%lb/in^3

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,'E',E,'yuk',yuk,'maxGER',maxGER','maxYER',maxYER,'GS',GS);

