function [TRUSS]=Truss_analysis_120bar(Individual)

Truss_Data=TrussData_120bar;

Truss_Data.A(1:12,:)=Individual(1);
Truss_Data.A(13:24,:)=Individual(2);
Truss_Data.A(25:36,:)=Individual(3);
Truss_Data.A(37:60,:)=Individual(4);
Truss_Data.A(61:84,:)=Individual(5);
Truss_Data.A(85:96,:)=Individual(6);
Truss_Data.A(97:120,:)=Individual(7);

dnsay=size(Truss_Data.dnkoor,1);
elsay=size(Truss_Data.eldn,1);


topser=dnsay*3;
yer=zeros(topser,1);

[rijitlik,elboy]=stiffness_3D_truss(topser,elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,Truss_Data.A);

tutser=find(Truss_Data.MesKos'==1);

FF=Truss_Data.yuk';
F=FF(:);

ser=setdiff([1:topser]',[tutser]);
    U=inv(rijitlik(ser,ser))*F(ser);
    yer=zeros(topser,1);
    yer(ser)=U;

[gerilmeler]=stresses_3D_truss(elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,yer,elboy);


%% Constraints
% Stress Constraint 
maxCEK=0.6*Truss_Data.fy;
alfa=0.4993;
beta=0.6777;
r_i=alfa*(Truss_Data.A).^beta;
k=1;
LAMDA_i=k*elboy'./r_i;
Cc=sqrt(2*pi^2*Truss_Data.E/Truss_Data.fy);

maxBAS=zeros(size(gerilmeler,1),1);

for K=1:size(gerilmeler,1)
    if gerilmeler(K,1)<0
        if LAMDA_i(K) < Cc
            maxBAS(K)=((1-(LAMDA_i(K))^2/(2*Cc^2))*Truss_Data.fy)/(5/3+3*LAMDA_i(K)/(8*Cc)-LAMDA_i(K)^3/(8*Cc^3));
        else
            maxBAS(K)=12*pi^2*Truss_Data.E/(23*(LAMDA_i(K))^2);
        end

        g1(K,1)=(abs(gerilmeler(K,1)))/maxBAS(K)-1;%Basınç
    else
        g1(K,1)=(abs(gerilmeler(K,1)))/maxCEK-1;%Çekme
    end
end

gg(1)=sum(g1.*(g1>0));

% Displacement constraint
g2=abs(yer)/Truss_Data.maxYER-1;
gg(2)=sum(g2.*(g2>0));

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