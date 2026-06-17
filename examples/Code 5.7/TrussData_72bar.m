function Truss_Data=TrussData_72bar

% Modulus of Elasticity (Pa)
E=7e10;  % 70 GPa (aluminum)

% Node coordinates (m)
% 4-story tower: each story height = 1.5 m, plan size = 3.0 x 3.0 m
dnkoor=[0   0   0;
3.0 0   0;
3.0 3.0 0;
0   3.0 0;
0   0   1.5;
3.0 0   1.5;
3.0 3.0 1.5;
0   3.0 1.5;
0   0   3.0;
3.0 0   3.0;
3.0 3.0 3.0;
0   3.0 3.0;
0   0   4.5;
3.0 0   4.5;
3.0 3.0 4.5;
0   3.0 4.5;
0   0   6.0;
3.0 0   6.0;
3.0 3.0 6.0;
0   3.0 6.0];

% Bar connections between nodes
eldn=[1 5;
2 6;
3 7;
4 8;
2 5;
1 6;
2 7;
3 6;
3 8;
4 7;
1 8;
4 5;
5 6;
6 7;
7 8;
8 5;
5 7;
6 8;
5 9;
6 10;
7 11;
8 12;
9 6;
5 10;
6 11;
7 10;
7 12;
8 11;
5 12;
8 9;
9 10;
10 11;
11 12;
12 9;
9 11;
10 12;
9 13;
10 14;
11 15;
12 16;
10 13;
9 14;
10 15;
11 14;
11 16;
12 15;
9 16;
12 13;
13 14;
14 15;
15 16;
13 16;
13 15;
14 16;
13 17;
14 18;
15 19;
16 20;
14 17;
13 18;
14 19;
15 18;
15 20;
16 19;
13 20;
16 17;
17 18;
18 19;
19 20;
20 17;
17 19;
18 20];

% Bar grouping (16 groups, 16 design variables)
% Group 1:  bars 1-4     (story 1 vertical)
% Group 2:  bars 5-12    (story 1 diagonal)
% Group 3:  bars 13-16   (story 1 horizontal)
% Group 4:  bars 17-18   (story 1 cross)
% Group 5:  bars 19-22   (story 2 vertical)
% Group 6:  bars 23-30   (story 2 diagonal)
% Group 7:  bars 31-34   (story 2 horizontal)
% Group 8:  bars 35-36   (story 2 cross)
% Group 9:  bars 37-40   (story 3 vertical)
% Group 10: bars 41-48   (story 3 diagonal)
% Group 11: bars 49-52   (story 3 horizontal)
% Group 12: bars 53-54   (story 3 cross)
% Group 13: bars 55-58   (story 4 vertical)
% Group 14: bars 59-66   (story 4 diagonal)
% Group 15: bars 67-70   (story 4 horizontal)
% Group 16: bars 71-72   (story 4 cross)
groups={[1:4],[5:12],[13:16],[17:18],...
        [19:22],[23:30],[31:34],[35:36],...
        [37:40],[41:48],[49:52],[53:54],...
        [55:58],[59:66],[67:70],[71:72]};

% Support conditions (1=fixed, 0=free) [x y z]
% Nodes 1-4 are fixed supports
MesKos=[1 1 1;
1 1 1;
1 1 1;
1 1 1;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0;
0 0 0];

% Loading (N) ---> Load(node,:)=[Fx Fy Fz]
% Loading #1
yuk1=zeros(size(dnkoor));
yuk1(17,:)=[25000 25000 -25000];  % 25 kN each direction

% Loading #2
yuk2=zeros(size(dnkoor));
yuk2(17,:)=[0 0 -25000];  % 25 kN downward
yuk2(18,:)=[0 0 -25000];
yuk2(19,:)=[0 0 -25000];
yuk2(20,:)=[0 0 -25000];

% Allowable Stress (Pa)
maxGER=1.75e8;  % 175 MPa

% Allowed Displacement (m)
maxYER=0.006;  % 6 mm

% Unit weight (kg/m^3)
GS=2770;  % aluminum

% Design variable bounds (m^2)
LB=ones(1,16)*1e-4;    % 1 cm^2
UB=ones(1,16)*130e-4;  % 130 cm^2

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,...
    'E',E,'yuk1',yuk1,'yuk2',yuk2,...
    'maxGER',maxGER,'maxYER',maxYER,'GS',GS,...
    'groups',{groups},'LB',LB,'UB',UB);

