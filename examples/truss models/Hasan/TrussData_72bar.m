function Truss_Data=TrussData_72bar

% Modulus of Elasticity (psi)
E=1e7;

% Node coordinates
dnkoor=[0	0	0;
120	0	0;
120	120	0;
0	120	0;
0	0	60;
120	0	60;
120	120	60;
0	120	60;
0	0	120;
120	0	120;
120	120	120;
0	120	120;
0	0	180;
120	0	180;
120	120	180;
0	120	180;
0	0	240;
120	0	240;
120	120	240;
0	120	240];

% Bar connections between nodes
eldn=[1	5;
2	6;
3	7;
4	8;
2	5;
1	6;
2	7;
3	6;
3	8;
4	7;
1	8;
4	5;
5	6;
6	7;
7	8;
8	5;
5	7;
6	8;
5	9;
6	10;
7	11;
8	12;
9	6;
5	10;
6	11;
7	10;
7	12;
8	11;
5	12;
8	9;
9	10;
10	11;
11	12;
12	9;
9	11;
10	12;
9	13;
10	14;
11	15;
12	16;
10	13;
9	14;
10	15;
11	14;
11	16;
12	15;
9	16;
12	13;
13	14;
14	15;
15	16;
13	16;
13	15;
14	16;
13	17;
14	18;
15	19;
16	20;
14	17;
13	18;
14	19;
15	18;
15	20;
16	19;
13	20;
16	17;
17	18;
18	19;
19	20;
20	17;
17	19;
18	20];

% Support conditions
MesKos=[1	1	1;
1	1	1;
1	1	1;
1	1	1;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0;
0	0	0];


% Loading     ----- > Load(dn_no,:)=[x y z] (lbs)
% Loading #1
yuk1=zeros(size(dnkoor));
yuk1(17,:)=[5000 5000 -5000];

% Loading #2
yuk2=zeros(size(dnkoor));
yuk2(17,:)=[0 0 -5000];
yuk2(18,:)=[0 0 -5000];
yuk2(19,:)=[0 0 -5000];
yuk2(20,:)=[0 0 -5000];

% Allowable Stress (psi)
maxGER=25000;

% Allowed Displacement
maxYER=0.25;%inch

% Unit weight
GS=.1;%lb/in^3

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,'E',E,'yuk1',yuk1,'yuk2',yuk2,'maxGER',maxGER','maxYER',maxYER,'GS',GS);
