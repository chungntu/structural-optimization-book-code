function [TRUSS]=Truss_analysis_18bar(Individual)
Truss_Data=TrussData_18bar;

Truss_Data.A([1 4 8 12 16])=Individual(1);
Truss_Data.A([2 6 10 14 18])=Individual(2);
Truss_Data.A([3 7 11 15])=Individual(3);
Truss_Data.A([5 9 13 17])=Individual(4);
Truss_Data.dnkoor=[1250	250	0;1000	250	0;Individual(5)	Individual(6) 0;750	250	0;Individual(7)	Individual(8) 0;500	250	0;Individual(9)	Individual(10) 0;250 250 0;Individual(11) Individual(12) 0;0 250 0;0 0 0];

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
k=4;
for j=1:size(gerilmeler,1)
    if gerilmeler(j,1)<0
            maxBURK(j)=k*Truss_Data.E*Truss_Data.A(j)/((elboy(j))^2);
        g2(j,1)=(abs(gerilmeler(j,1)))/maxBURK(j)-1; %Basınç
    else
        g2(j,1)=0;
    end
end
gg(2)=sum(g2.*(g2>0));
%% Object Function
ObjVal=0;
for i=1:size(Truss_Data.eldn,1)
ObjVal=ObjVal+elboy(i)*Truss_Data.A(i)*Truss_Data.GS;
end
%% Penalized Obj. Func.
TRUSS.OBJVAL=ObjVal;
TRUSS.VIO=sum(gg);

PEN=10^8;
Z=ObjVal;
for k=1:length(gg)
     Z=Z+ PEN*gg(k);
end
TRUSS.PENALIZED=Z;

end