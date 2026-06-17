function [TRUSS]=Truss_analysis_72bar(Individual)

Truss_Data=TrussData_72bar;

Truss_Data.A(1:4,:)=Individual(1);
Truss_Data.A(5:12,:)=Individual(2);
Truss_Data.A(13:16,:)=Individual(3);
Truss_Data.A(17:18,:)=Individual(4);
Truss_Data.A(19:22,:)=Individual(5);
Truss_Data.A(23:30,:)=Individual(6);
Truss_Data.A(31:34,:)=Individual(7);
Truss_Data.A(35:36,:)=Individual(8);
Truss_Data.A(37:40,:)=Individual(9);
Truss_Data.A(41:48,:)=Individual(10);
Truss_Data.A(49:52,:)=Individual(11);
Truss_Data.A(53:54,:)=Individual(12);
Truss_Data.A(55:58,:)=Individual(13);
Truss_Data.A(59:66,:)=Individual(14);
Truss_Data.A(67:70,:)=Individual(15);
Truss_Data.A(71:72,:)=Individual(16);

dnsay=size(Truss_Data.dnkoor,1);
elsay=size(Truss_Data.eldn,1);


topser=dnsay*3;
yer1=zeros(topser,1);

[rijitlik,elboy]=stiffness_3D_truss(topser,elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,Truss_Data.A);

tutser=find(Truss_Data.MesKos'==1);

FF1=Truss_Data.yuk1';
F1=FF1(:);

ser=setdiff([1:topser]',[tutser]);
    U1=inv(rijitlik(ser,ser))*F1(ser);
    yer1=zeros(topser,1);
    yer1(ser)=U1;

[gerilmeler1]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer1,elboy);


yer2=zeros(topser,1);
FF2=Truss_Data.yuk2';
F2=FF2(:);

ser=setdiff([1:topser]',[tutser]);
    U2=inv(rijitlik(ser,ser))*F2(ser);
    yer2=zeros(topser,1);
    yer2(ser)=U2;

[gerilmeler2]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer2,elboy);


%% Constraints

% Stress Constraint for loading #1
g1=(abs(gerilmeler1)/Truss_Data.maxGER)-1;
gg(1)=sum(g1.*(g1>0));

% Displacement constraint for loading #1
g2=abs(yer1)/Truss_Data.maxYER-1;
gg(2)=sum(g2.*(g2>0));

% Stress Constraint for loading #2
g3=(abs(gerilmeler2)/Truss_Data.maxGER)-1;
gg(3)=sum(g3.*(g3>0));

% Displacement constraint for loading #2
g4=abs(yer2)/Truss_Data.maxYER-1;
gg(4)=sum(g4.*(g4>0));

%% Object Function
ObjVal=0;
for i=1:size(Truss_Data.eldn,1)
ObjVal=ObjVal+elboy(i)*Truss_Data.A(i)*Truss_Data.GS;
end

%% Penalized Obj. Func.
PEN=10^8;
Z=ObjVal;
for k=1:length(gg)
      Z=Z+ PEN*gg(k);
end
TRUSS.PENALIZED=Z;
