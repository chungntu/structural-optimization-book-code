function [TRUSS]=Truss_analysis_200bar(Individual)

Truss_Data=TrussData_200bar;

Truss_Data.A(1:4,:)=Individual(1);
Truss_Data.A([5,8,11,14,17],:)=Individual(2);
Truss_Data.A([19,20,21,22,23,24],:)=Individual(3);
Truss_Data.A([18,25,56,63,94,101,132,139,170,177],:)=Individual(4);
Truss_Data.A([26,29,32,35,38],:)=Individual(5);
Truss_Data.A([6,7,9,10,12,13,15,16,27,28,30,31,33,34,36,37],:)=Individual(6);
Truss_Data.A([39,40,41,42],:)=Individual(7);
Truss_Data.A([43,46,49,52,55],:)=Individual(8);
Truss_Data.A([57,58,59,60,61,62],:)=Individual(9);
Truss_Data.A([64,67,70,73,76],:)=Individual(10);
Truss_Data.A([44,45,47,48,50,51,53,54,65,66,68,69,71,72,74,75],:)=Individual(11);
Truss_Data.A([77,78,79,80],:)=Individual(12);
Truss_Data.A([81,84,87,90,93],:)=Individual(13);
Truss_Data.A([95,96,97,98,99,100],:)=Individual(14);
Truss_Data.A([102,105,108,111,114],:)=Individual(15);
Truss_Data.A([82,83,85,86,88,89,91,92,103,104,106,107,109,110,112,113],:)=Individual(16);
Truss_Data.A([115,116,117,118],:)=Individual(17);
Truss_Data.A([119,122,125,128,131],:)=Individual(18);
Truss_Data.A([133,134,135,136,137,138],:)=Individual(19);
Truss_Data.A([140,143,146,149,152],:)=Individual(20);
Truss_Data.A([120,121,123,124,126,127,129,130,141,142,144,145,147,148,150,151],:)=Individual(21);
Truss_Data.A([153,154,155,156],:)=Individual(22);
Truss_Data.A([157,160,163,166,169],:)=Individual(23);
Truss_Data.A([171,172,173,174,175,176],:)=Individual(24);
Truss_Data.A([178,181,184,187,190],:)=Individual(25);
Truss_Data.A([158,159,161,162,164,165,167,168,179,180,182,183,185,186,188,189],:)=Individual(26);
Truss_Data.A([191,192,193,194],:)=Individual(27);
Truss_Data.A([195,197,198,200],:)=Individual(28);
Truss_Data.A([196,199],:)=Individual(29);

dnsay=size(Truss_Data.dnkoor,1);
elsay=size(Truss_Data.eldn,1);


topser=dnsay*3;




[rijitlik,elboy]=stiffness_3D_truss(topser,elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,Truss_Data.A);

tutser=find(Truss_Data.MesKos'==1);

% case 1
yer1=zeros(topser,1);

FF1=Truss_Data.yuk1';
F1=FF1(:);

ser=setdiff([1:topser]',[tutser]);
    U1=inv(rijitlik(ser,ser))*F1(ser);
    yer1=zeros(topser,1);
    yer1(ser)=U1;

[gerilmeler1]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer1,elboy);

% case 2
yer2=zeros(topser,1);

FF2=Truss_Data.yuk2';
F2=FF2(:);

ser=setdiff([1:topser]',[tutser]);
    U2=inv(rijitlik(ser,ser))*F2(ser);
    yer2=zeros(topser,1);
    yer2(ser)=U2;

[gerilmeler2]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer2,elboy);

% case3
yer3=zeros(topser,1);

FF3=Truss_Data.yuk3';
F3=FF3(:);

ser=setdiff([1:topser]',[tutser]);
    U3=inv(rijitlik(ser,ser))*F3(ser);
    yer3=zeros(topser,1);
    yer3(ser)=U3;

[gerilmeler3]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer3,elboy);

%% Constraints

% Stress
g1=(abs(gerilmeler1)/Truss_Data.maxGER)-1;
gg(1)=sum(g1.*(g1>0));

g2=(abs(gerilmeler2)/Truss_Data.maxGER)-1;
gg(2)=sum(g2.*(g2>0));

g3=(abs(gerilmeler3)/Truss_Data.maxGER)-1;
gg(3)=sum(g3.*(g3>0));

%% Object Function
ObjVal=0;
for i=1:size(Truss_Data.eldn,1)
ObjVal=ObjVal+elboy(i)*Truss_Data.A(i)*Truss_Data.GS;
end
TRUSS.OBJVAL=ObjVal;
TRUSS.VIO=sum(gg);
%% Penalized Obj. Func.
PEN=10^8;
Z=ObjVal;
for k=1:length(gg)
     Z=Z+ PEN*gg(k);
end
TRUSS.PENALIZED=Z;