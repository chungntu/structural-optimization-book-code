function [TRUSS]=Truss_analysis_17bar(Individual)
Truss_Data=TrussData_17bar;

Truss_Data.A=Individual';

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

% Stress
g1=(abs(gerilmeler)/Truss_Data.maxGER)-1;
gg(1)=sum(g1.*(g1>0));

% Displacement
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



end