function Truss_Data=TrussData_25bar

% Modulus of Elasticity (Pa)
E=7e10;  % 70 GPa (aluminum)

% Node coordinates (m)
dnkoor=[-1.0   0     5.0;
         1.0   0     5.0;
        -1.0   1.0   2.5;
         1.0   1.0   2.5;
         1.0  -1.0   2.5;
        -1.0  -1.0   2.5;
        -2.5   2.5   0;
         2.5   2.5   0;
         2.5  -2.5   0;
        -2.5  -2.5   0];

% Bar connections between nodes
eldn=[1 2;
      1 4;
      2 3;
      1 5;
      2 6;
      2 5;
      2 4;
      1 3;
      1 6;
      3 6;
      4 5;
      3 4;
      5 6;
      3 10;
      6 7;
      4 9;
      5 8;
      3 8;
      4 7;
      6 9;
      5 10;
      3 7;
      4 8;
      5 9;
      6 10];

% Bar grouping (8 groups, 8 design variables)
% Group 1: bar 1          (top cross)
% Group 2: bars 2-5       (top-to-mid diagonal)
% Group 3: bars 6-9       (top-to-mid diagonal)
% Group 4: bars 10-11     (mid horizontal)
% Group 5: bars 12-13     (mid horizontal)
% Group 6: bars 14-17     (mid-to-base diagonal)
% Group 7: bars 18-21     (mid-to-base diagonal)
% Group 8: bars 22-25     (mid-to-base vertical)
groups={[1],[2:5],[6:9],[10:11],[12:13],[14:17],[18:21],[22:25]};

% Support conditions (1=fixed, 0=free) [x y z]
% Nodes 7-10 are fixed supports
MesKos=[0 0 0;0 0 0;0 0 0;0 0 0;0 0 0;0 0 0;1 1 1;1 1 1;1 1 1;1 1 1];

% Loading (N) ---> Load(node,:)=[Fx Fy Fz]
% Loading #1
yuk1=zeros(size(dnkoor));
yuk1(1,:)=[0      90000 -25000];   % 90 kN, -25 kN
yuk1(2,:)=[0     -90000 -25000];   % -90 kN, -25 kN

% Loading #2
yuk2=zeros(size(dnkoor));
yuk2(1,:)=[5000   45000 -25000];   % 5 kN, 45 kN, -25 kN
yuk2(2,:)=[0      45000 -25000];   % 45 kN, -25 kN
yuk2(3,:)=[2500   0      0];       % 2.5 kN
yuk2(6,:)=[2500   0      0];       % 2.5 kN

% Allowable Stress (Pa) - per group (recalculated for SI coordinates)
maxBAS=[220; 78; 121; 220; 220; 48; 49; 82]*1e6;  % MPa (compression)
maxCEK=275e6;  % 275 MPa (tension)

% Allowed Displacement (m)
maxYER=0.009;  % 9 mm

% Unit weight (kg/m^3)
GS=2770;  % aluminum

% Design variable bounds (m^2)
LB=ones(1,8)*0.1e-4;   % 0.1 cm^2
UB=ones(1,8)*22e-4;    % 22 cm^2

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,...
    'E',E,'yuk1',yuk1,'yuk2',yuk2,...
    'maxBAS',maxBAS','maxCEK',maxCEK,'maxYER',maxYER,'GS',GS,...
    'LB',LB,'UB',UB);
