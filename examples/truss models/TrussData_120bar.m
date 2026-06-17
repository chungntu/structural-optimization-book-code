function Truss_Data=TrussData_120bar

% Modulus of Elasticity (Pa)
E=2.1e11;  % 210 GPa (steel)

% Node coordinates (m)
% Dome structure with 4 levels:
%   Level 1 (apex):     1 node,  R = 0 m,    z = 7.0 m
%   Level 2 (12 nodes): R = 7.0 m,  z = 5.0 m
%   Level 3 (24 nodes): R = 12.5 m, z = 3.0 m
%   Level 4 (12 nodes): R = 16.0 m, z = 0 m (supports)

% Apex
dnkoor(1,:) = [0 0 7.0];

% Level 2: 12 nodes at R=7.0, z=5.0
R2 = 7.0;  z2 = 5.0;
for i = 1:12
    ang = (i-1)*30 * pi/180;
    dnkoor(1+i,:) = [R2*cos(ang)  R2*sin(ang)  z2];
end

% Level 3: 24 nodes at R=12.5, z=3.0
R3 = 12.5;  z3 = 3.0;
for i = 1:24
    ang = (i-1)*15 * pi/180;
    dnkoor(13+i,:) = [R3*cos(ang)  R3*sin(ang)  z3];
end

% Level 4: 12 nodes at R=16.0, z=0 (supports)
R4 = 16.0;  z4 = 0;
for i = 1:12
    ang = (i-1)*30 * pi/180;
    dnkoor(37+i,:) = [R4*cos(ang)  R4*sin(ang)  z4];
end

% Bar connections between nodes
eldn=[1 2;
1 3;
1 4;
1 5;
1 6;
1 7;
1 8;
1 9;
1 10;
1 11;
1 12;
1 13;
2 3;
3 4;
4 5;
5 6;
6 7;
7 8;
8 9;
9 10;
10 11;
11 12;
12 13;
13 2;
2 14;
3 16;
4 18;
5 20;
6 22;
7 24;
8 26;
9 28;
10 30;
11 32;
12 34;
13 36;
2 15;
3 15;
3 17;
4 17;
4 19;
5 19;
5 21;
6 21;
6 23;
7 23;
7 25;
8 25;
8 27;
9 27;
9 29;
10 29;
10 31;
11 31;
11 33;
12 33;
12 35;
13 35;
13 37;
2 37;
14 15;
15 16;
16 17;
17 18;
18 19;
19 20;
20 21;
21 22;
22 23;
23 24;
24 25;
25 26;
26 27;
27 28;
28 29;
29 30;
30 31;
31 32;
32 33;
33 34;
34 35;
35 36;
36 37;
37 14;
14 38;
16 39;
18 40;
20 41;
22 42;
24 43;
26 44;
28 45;
30 46;
32 47;
34 48;
36 49;
15 38;
15 39;
17 39;
17 40;
19 40;
19 41;
21 41;
21 42;
23 42;
23 43;
25 43;
25 44;
27 44;
27 45;
29 45;
29 46;
31 46;
31 47;
33 47;
33 48;
35 48;
35 49;
37 49;
37 38];

% Bar grouping (7 groups, 7 design variables)
% Group 1: bars 1-12    (apex to level 2)
% Group 2: bars 13-24   (level 2 ring)
% Group 3: bars 25-36   (level 2 to level 3, radial)
% Group 4: bars 37-60   (level 2 to level 3, diagonal)
% Group 5: bars 61-84   (level 3 ring)
% Group 6: bars 85-96   (level 3 to level 4, radial)
% Group 7: bars 97-120  (level 3 to level 4, diagonal)
groups={[1:12],[13:24],[25:36],[37:60],[61:84],[85:96],[97:120]};

% Support conditions (1=fixed, 0=free) [x y z]
% Nodes 38-49 (level 4) are fixed supports
MesKos = zeros(49,3);
MesKos(38:49,:) = ones(12,3);

% Loading (N) ---> Load(node,:)=[Fx Fy Fz]
yuk=zeros(size(dnkoor));
yuk(1,:)=[0 0 -60000];    % 60 kN (apex)
for i=2:13
    yuk(i,:)=[0 0 -30000]; % 30 kN (level 2)
end
for i=14:37
    yuk(i,:)=[0 0 -10000]; % 10 kN (level 3)
end

% Steel yield strength (Pa)
fy=4e8;  % 400 MPa

% Allowed Displacement (m)
maxYER=0.005;  % 5 mm

% Unit weight (kg/m^3)
GS=7850;  % steel

% Design variable bounds (m^2)
LB=ones(1,7)*5e-4;    % 5 cm^2
UB=ones(1,7)*130e-4;  % 130 cm^2

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,...
    'E',E,'yuk',yuk,'fy',fy,'maxYER',maxYER,'GS',GS,...
    'groups',{groups},'LB',LB,'UB',UB);
