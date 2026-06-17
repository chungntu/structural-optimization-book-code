function Truss_Data=TrussData_52bar_modal

% Modulus of Elasticity
E=2.10e11;

% Shape variables explanation (Nominal initial values for reference)
% ZA (m): Z-coordinate of the tip node
% XB (m): X-radius of the upper intermediate ring
% ZB (m): Z-coordinate of the upper intermediate ring
% XF (m): X-radius of the lower intermediate ring
% ZF (m): Z-coordinate of the lower intermediate ring
%
% Note: The actual coordinates are built dynamically during optimization.
% These are the nominal base coordinates to provide a starting geometry.
ZA = 6.0;
XB = 2.0;
ZB = 5.0;
XF = 4.0;
ZF = 3.0;

% Node coordinates (m)
dnkoor=[0	0	ZA;
XB	0	ZB;
0	XB	ZB;
-XB	0	ZB;
0	-XB	ZB;
XF	0	ZF;
XF*cos(45/180*pi)	XF*cos(45/180*pi)	ZF;
0	XF	ZF;
-XF*cos(45/180*pi)	XF*cos(45/180*pi)	ZF;
-XF	0	ZF;
-XF*cos(45/180*pi)	-XF*cos(45/180*pi)	ZF;
0	-XF	ZF;
XF*cos(45/180*pi)	-XF*cos(45/180*pi)	ZF;
6	0	0;
6*cos(45/180*pi)	6*cos(45/180*pi)	0;
0	6	0;
-6*cos(45/180*pi)	6*cos(45/180*pi)	0;
-6	0	0;
-6*cos(45/180*pi)	-6*cos(45/180*pi)	0;
0	-6	0;
6*cos(45/180*pi) -6*cos(45/180*pi) 0];

% Bar connections between nodes 
eldn=[1	4	;
1	5	;
1	2	;
1	3	;
4	10	;
5	12	;
2	6	;
3	8	;
4	11	;
11	5	;
5	13	;
2	13	;
2	7	;
3	7	;
3	9	;
4	9	;
4	5	;
5	2	;
2	3	;
3	4	;
10	11	;
11	12	;
12	13	;
13	6	;
6	7	;
7	8	;
8	9	;
9	10	;
10	18	;
11	19	;
12	20	;
13	21	;
6	14	;
7	15	;
8	16	;
9	17	;
10	19	;
12	19	;
12	21	;
6	21	;
6	15	;
8	15	;
8	17	;
10	17	;
11	18	;
11	20	;
13	20	;
13	14	;
7	14	;
7	16	;
9	16	;
9	18	];

% Support conditions
MesKos=[0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
0	0	0	;
1	1	1	;
1	1	1	;
1	1	1	;
1	1	1	;
1	1	1	;
1	1	1	;
1	1	1	;
1	1	1	];

% Frequency limits (Hz)
limfre(1)=16;
limfre(2)=28;

% Unit weight
GS=7800;%kg/m^3

% added masses
add_mass=zeros(size(MesKos,1));
add_mass(1:13)=50; %kg

% Bar grouping (8 groups for the 52 members)
groups={[1:4], [5:8], [9:16], [17:20], [21:28], [29:36], [37:44], [45:52]};

% Design variable bounds (13 variables total)
% Variables 1-5: Shape variables (ZA, XB, ZB, XF, ZF in m)
% Variables 6-13: Sizing variables (Cross-sectional areas of the 8 groups in m^2)
LB=ones(1,13);
LB(1,1)=4;      %m (ZA)
LB(1,2)=0.01;   %m (XB)
LB(1,3)=3.7;    %m (ZB)
LB(1,4)=2.01;   %m (XF)
LB(1,5)=2.5;    %m (ZF)
LB(1,6:13)=0.0001; %m2 (1 cm2)

UB=ones(1,13);
UB(1,1)=8;      %m (ZA)
UB(1,2)=4;      %m (XB)
UB(1,3)=7.7;    %m (ZB)
UB(1,4)=6;      %m (XF)
UB(1,5)=6.5;    %m (ZF)
UB(1,6:13)=0.001;  %m2 (10 cm2)

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,'E',E,'GS',GS,'add_mass',add_mass,'limfre',limfre,'groups',{groups},'LB',LB,'UB',UB);

