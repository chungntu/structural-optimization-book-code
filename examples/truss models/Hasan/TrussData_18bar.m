function Truss_Data=TrussData_18bar

% Modulus of Elasticity (psi)
E=1e7;

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

% Loading     ----- > Load(dn_no,:)=[x y z] (lbs)
yuk=zeros(size(MesKos));
yuk(1,:)=[0 -20000 0];
yuk(2,:)=[0 -20000 0];
yuk(4,:)=[0 -20000 0];
yuk(6,:)=[0 -20000 0];
yuk(8,:)=[0 -20000 0];

% Allowable Stress (psi)
maxGER=20000;%psi

% Allowed Displacement (in)
maxYER=1.0; %in

% Unit weight
GS=0.1;%lb/in^3

Truss_Data=struct('MesKos',MesKos,'eldn',eldn,'E',E,'yuk',yuk,'maxGER',maxGER','maxYER',maxYER','GS',GS);

