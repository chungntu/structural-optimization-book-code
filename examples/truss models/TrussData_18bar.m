function Truss_Data=TrussData_18bar

% Modulus of Elasticity (Pa)
E=6.9e10; % 69 GPa (~1e7 psi)

% Bar connections between nodes
eldn=[1	2	;
1	3	;
2	3	;
2	4	;
3	4	;
3	5	;
4	5	;
4	6	;
5	6	;
5	7	;
6	7	;
6	8	;
7	8	;
7	9	;
8	9	;
8	10	;
9	10	;
9	11];

% Support conditions
MesKos=[0	0	1	;
0	0	1	;
0	0	1	;
0	0	1	;
0	0	1	;
0	0	1	;
0	0	1	;
0	0	1	;
0	0	1	;
1	1	1	;
1	1	1	];

% Loading     ----- > Load(dn_no,:)=[x y z] (N)
yuk=zeros(size(MesKos));
yuk(1,:)=[0 -89000 0]; % 89 kN (~20000 lbs)
yuk(2,:)=[0 -89000 0];
yuk(4,:)=[0 -89000 0];
yuk(6,:)=[0 -89000 0];
yuk(8,:)=[0 -89000 0];

% Allowable Stress (Pa)
maxGER=1.38e8; % 138 MPa (~20000 psi)

% Allowed Displacement (m)
maxYER=0.025; % 25 mm (~1.0 in)

% Unit density (kg/m^3)
GS=2770; % 2770 kg/m^3 (~0.1 lb/in^3)

% Design variable bounds
LB=ones(1,12);
LB(1,1:4)=LB(1,1:4)*22 * 1e-4; % 22 cm2 (m2)
LB(1,5)=LB(1,5)*20; %m (x3)
LB(1,6)=LB(1,6)*-6; %m (y3)
LB(1,7)=LB(1,7)*13; %m (x5)
LB(1,8)=LB(1,8)*-6; %m (y5)
LB(1,9)=LB(1,9)*7; %m (x7)
LB(1,10)=LB(1,10)*-6; %m (y7)
LB(1,11)=LB(1,11)*1; %m (x9)
LB(1,12)=LB(1,12)*-6; %m (y9)

UB=ones(1,12);
UB(1,1:4)=UB(1,1:4)*116 * 1e-4; % 116 cm2 (m2)
UB(1,5)=UB(1,5)*31; %m (x3)
UB(1,6)=UB(1,6)*6; %m (y3)
UB(1,7)=UB(1,7)*25; %m (x5)
UB(1,8)=UB(1,8)*6; %m (y5)
UB(1,9)=UB(1,9)*18; %m (x7)
UB(1,10)=UB(1,10)*6; %m (y7)
UB(1,11)=UB(1,11)*12; %m (x9)
UB(1,12)=UB(1,12)*6; %m (y9)

% Base node coordinates (m)
% Coordinates for nodes 3,5,7,9 will be overwritten by optimizer
dnkoor = [
    31.75  6.35 0; % Node 1
    25.40  6.35 0; % Node 2
    19.69 -5.72 0; % Node 3 (var x3, y3 - using default initial limit)
    19.05  6.35 0; % Node 4
    13.34 -5.72 0; % Node 5 (var x5, y5)
    12.70  6.35 0; % Node 6
     6.99 -5.72 0; % Node 7 (var x7, y7)
     6.35  6.35 0; % Node 8
     0.64 -5.72 0; % Node 9 (var x9, y9)
     0.00  6.35 0; % Node 10
     0.00  0.00 0  % Node 11
];

% Bar grouping (4 areas, 8 node coordinates) -> 12 Design variables
% Area 1: bars 1,4,8,12,16 (Top chord)
% Area 2: bars 2,6,10,14,18 (Bottom chord)
% Area 3: bars 3,7,11,15 (Diagonals / verticals)
% Area 4: bars 5,9,13,17 (Diagonals)
groups={[1,4,8,12,16],[2,6,10,14,18],[3,7,11,15],[5,9,13,17]};

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,'E',E,'yuk',yuk,'maxGER',maxGER,'maxYER',maxYER,'GS',GS,'LB',LB,'UB',UB,'groups',{groups});

