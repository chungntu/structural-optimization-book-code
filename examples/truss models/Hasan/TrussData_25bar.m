function Truss_Data=TrussData_25bar

% Modulus of Elasticity (psi)
E=1e7;

% Node coordinates
dnkoor=[-37.5  0     200;
         37.5  0     200;
        -37.5  37.5  100;
         37.5  37.5  100;
         37.5 -37.5  100;
        -37.5 -37.5  100;
        -100   100     0;
         100   100	   0;
         100  -100     0;
        -100  -100     0];

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

% Support conditions
MesKos=[0 0 0;0	0 0;0 0	0;0	0 0;0 0 0;0 0 0;1 1 1;1 1 1;1 1 1;1 1 1];


% Loading     ----- > Load(dn_no,:)=[x y z] (lbs)
% Loading #1
yuk1=zeros(size(dnkoor));
yuk1([1:2],:)=[0 20000 -5000;0 -20000 -5000];

% Loading #2
yuk2(1,:)=[1000 10000 -5000];
yuk2(2,:)=[ 0 10000 -5000];
yuk2(3,:)=[500 0 0];
yuk2(6,:)=[500 0 0];

% Allowable Stress (psi)
maxBAS=[35.092; 11.590; 17.305; 35.092; 35.092; 6.759; 6.959; 11.082]*1000;
maxCEK=40000;

% Allowed Displacement
maxYER=0.35;%inch

% Unit weight
GS=.1;%lb/in^3

Truss_Data=struct('dnkoor',dnkoor,'MesKos',MesKos,'eldn',eldn,'E',E,'yuk1',yuk1,'yuk2',yuk2,'maxBAS',maxBAS','maxCEK',maxCEK,'maxYER',maxYER,'GS',GS);
