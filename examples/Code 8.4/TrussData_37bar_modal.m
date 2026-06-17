function Truss_Data=TrussData_37bar_modal

% Modulus of Elasticity
E=2.10e11;

% Node coordinates
dnkoor=zeros(20,3);
dnkoor=[0       0       0;
1       1       0;;
1       0       0;
2       1       0;;
2       0       0;
3       1       0;;
3       0       0;
4       1       0;;
4       0       0;
5       1       0;;
5       0       0;
6       1       0;;
6       0       0;
7       1       0;;
7       0       0;
8       1       0;;
8       0       0;
9       1       0;;
9       0       0;
10      0       0];

% Bar connections between nodes 
eldn=[1 3       ;
2       3       ;
3       4       ;
3       5       ;
4       5       ;
5       6       ;
5       7       ;
6       7       ;
7       8       ;
7       9       ;
8       9       ;
9       10      ;
9       11      ;
10      11      ;
10      13      ;
11      13      ;
12      13      ;
12      15      ;
13      15      ;
14      15      ;
14      17      ;
15      17      ;
16      17      ;
16      19      ;
17      19      ;
18      19      ;
19      20      ;
1       2       ;
2       4       ;
4       6       ;
6       8       ;
8       10      ;
10      12      ;
12      14      ;
14      16      ;
16      18      ;
18      20      ];

% Support conditions
MesKos=[1       1       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
0       0       1       ;
1       1       1       ];

% Fixed cross sections
A=zeros(size(eldn,1),1);
A(28:37)=4e-3; %m2

% Frequency limits (Hz)
limfre(1)=20;
limfre(2)=40;
limfre(3)=60;

% Unit weight
GS=7800;%kg/m^3

% added masses
add_mass=zeros(size(dnkoor,1),1);
add_mass(2:2:18)=10; %kg

% Bar grouping (14 symmetric groups for the 27 active members)
% Elements 28-37 are constant and excluded from active design groups
groups={[1,27], [4,25], [7,22], [10,19], [13,16], ... % Lower chords (5 groups)
        [2,26], [5,23], [8,20], [11,17], [14],    ... % Verticals (5 groups)
        [3,24], [6,21], [9,18], [12,15]};             % Diagonals (4 groups)

% Design variable bounds (19 variables total)
% Variables 1-5: Shape variables (Y-coordinates of upper nodes in meters)
% Variables 6-19: Sizing variables (Cross-sectional areas of the 14 groups in m^2)
LB = [ones(1,5)*0.5, ones(1,14)*1e-4];   % Y_min = 0.5m, A_min = 1 cm2
UB = [ones(1,5)*5.0, ones(1,14)*100e-4]; % Y_max = 5.0m, A_max = 100 cm2

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,'E',E,'GS',GS,'add_mass',add_mass,'limfre',limfre,'A',A,'groups',{groups},'LB',LB,'UB',UB);

