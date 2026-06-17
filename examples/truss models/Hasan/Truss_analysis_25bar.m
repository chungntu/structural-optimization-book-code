function [TRUSS]=Truss_analysis_25bar(Individual)

Truss_Data=TrussData_25bar;


Truss_Data.MeM_maxBAS(1,:)=Truss_Data.maxBAS(1);
Truss_Data.MeM_maxBAS(2:5,:)=Truss_Data.maxBAS(2);
Truss_Data.MeM_maxBAS(6:9,:)=Truss_Data.maxBAS(3);
Truss_Data.MeM_maxBAS(10:11,:)=Truss_Data.maxBAS(4);
Truss_Data.MeM_maxBAS(12:13,:)=Truss_Data.maxBAS(5);
Truss_Data.MeM_maxBAS(14:17,:)=Truss_Data.maxBAS(6);
Truss_Data.MeM_maxBAS(18:21,:)=Truss_Data.maxBAS(7);
Truss_Data.MeM_maxBAS(22:25,:)=Truss_Data.maxBAS(8);


Truss_Data.A(1,:)=Individual(1);
Truss_Data.A(2:5,:)=Individual(2);
Truss_Data.A(6:9,:)=Individual(3);
Truss_Data.A(10:11,:)=Individual(4);
Truss_Data.A(12:13,:)=Individual(5);
Truss_Data.A(14:17,:)=Individual(6);
Truss_Data.A(18:21,:)=Individual(7);
Truss_Data.A(22:25,:)=Individual(8);


dnsay=size(Truss_Data.dnkoor,1);
elsay=size(Truss_Data.eldn,1);


topser=dnsay*3;
yer=zeros(topser,1);

[rijitlik,elboy]=stiffness_3D_truss(topser,elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,Truss_Data.A);

tutser=find(Truss_Data.MesKos'==1);

% Loading #1
FF1=Truss_Data.yuk1';
F1=FF1(:);

ser=setdiff([1:topser]',[tutser]);
    U=inv(rijitlik(ser,ser))*F1(ser);
    yer1=zeros(topser,1);
    yer1(ser)=U;

[gerilmeler1]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer1,elboy);

% Loading #2
FF2=Truss_Data.yuk2';
F2=FF2(:);

ser=setdiff([1:topser]',[tutser]);
    U=inv(rijitlik(ser,ser))*F2(ser);
    yer2=zeros(topser,1);
    yer2(ser)=U;

[gerilmeler2]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer2,elboy);



%% Constraints
% Stress Constraint for loading #1
for K=1:size(gerilmeler1,1)
    if gerilmeler1(K,1)<0
        g1_case1(K,1)=(abs(gerilmeler1(K,1)))/Truss_Data.MeM_maxBAS(K,1)-1;%Compresion
    else
        g1_case1(K,1)=(abs(gerilmeler1(K,1)))/Truss_Data.maxCEK-1;%Tension
    end
end
gg(1)=sum(g1_case1.*(g1_case1>0));

% Displacement constraint for loading #1
g2_case1=abs(yer1)/Truss_Data.maxYER-1;
gg(2)=sum(g2_case1.*(g2_case1>0));

% Stress Constraint for loading #2
for K=1:size(gerilmeler2,1)
    if gerilmeler2(K,1)<0
        g1_case2(K,1)=(abs(gerilmeler2(K,1)))/Truss_Data.MeM_maxBAS(K,1)-1;%Compresion
    else
        g1_case2(K,1)=(abs(gerilmeler2(K,1)))/Truss_Data.maxCEK-1;%Tension
    end
end
gg(3)=sum(g1_case2.*(g1_case2>0));

% Displacement constraint for loading #2
g2_case2=abs(yer2)/Truss_Data.maxYER-1;
gg(4)=sum(g2_case2.*(g2_case2>0));


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
