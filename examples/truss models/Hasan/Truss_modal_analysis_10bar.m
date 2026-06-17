function [TRUSS]=Truss_modal_analysis_10bar(Individual)

Truss_Data=TrussData_10bar_modal;

Truss_Data.A=Individual';

eleman_dn=Truss_Data.eldn;
dnsay=size(Truss_Data.dnkoor,1);
elsay=size(eleman_dn,1);

topser=dnsay*3;
yer=zeros(topser,1);

[rijitlik,elboy]=stiffness_3D_truss(topser,elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.E,Truss_Data.A);
[mass_mat]=mass_truss(topser,elsay,Truss_Data.eldn,Truss_Data.dnkoor,Truss_Data.GS,Truss_Data.A);

for i=1:dnsay
mass_mat(3*i-2,3*i-2)=mass_mat(3*i-2,3*i-2)+Truss_Data.add_mass(i);
mass_mat(3*i-1,3*i-1)=mass_mat(3*i-1,3*i-1)+Truss_Data.add_mass(i);
mass_mat(3*i,3*i)=mass_mat(3*i,3*i)+Truss_Data.add_mass(i);
end

tutser=find(Truss_Data.MesKos'==1);
ser=setdiff([1:topser]',[tutser]);
[FI,LAMDA]=eig(inv(mass_mat(ser,ser))*rijitlik(ser,ser));

[LAMDA_sorted, ind]=sort(diag(LAMDA),'ascend');

Frekans=sqrt(LAMDA_sorted)/(2*pi);

%% Constraints

for i=1:3
g(i)=(Truss_Data.limfre(i)/Frekans(i))-1;
gg(i)=g(i)*(g(i)>0);
end

%% Object Function
ObjVal=0;
for i=1:size(Truss_Data.eldn,1)
ObjVal=ObjVal+elboy(i)*Truss_Data.A(i)*Truss_Data.GS;
end
%% Penalized Obj. Func.
PEN=10^18;
Z=ObjVal;
for k=1:length(gg)
     Z=Z+ PEN*gg(k);
end
TRUSS.PENALIZED=Z;