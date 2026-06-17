% --- DONG LENH CHAY O TREN CUNG ---
top99(60,20,0.5,3.0,1.5,1)
% ----------------------------------

% Dinh nghia cac function o ben duoi
function top99(nelx,nely,volfrac,penal,rmin,nLoadCase)

% KHOI TAO
x(1:nely,1:nelx) = volfrac; 
loop = 0; 
change = 1;
passive = [];

% BAT DAU VONG LAP TOI UU
while change > 0.01  
    loop = loop + 1;
    xold = x;
    
    % Phan tich phan tu huu han
    [U] = FE(nelx,nely,x,penal,nLoadCase);         
    
    % Tinh toan ham muc tieu
    [KE] = localK;
    c = 0;
    dc = zeros(nely,nelx);
    for ely = 1:nely
        for elx = 1:nelx
            n1 = (nely+1)*(elx-1)+ely; 
            n2 = (nely+1)* elx   +ely;
            Ue = U([2*n1-1;2*n1; 2*n2-1;2*n2; 2*n2+1;2*n2+2; 2*n1+1;2*n1+2],1);
            c = c + x(ely,elx)^penal*Ue'*KE*Ue;
            dc(ely,elx) = -penal*x(ely,elx)^(penal-1)*Ue'*KE*Ue;
        end
    end
    
    % Loc do nhay
    [dc] = check(nelx,nely,rmin,x,dc);    
    
    % Cap nhat bien thiet ke
    [x] = OC(nelx,nely,x,volfrac,dc,passive);
    
    % In ket qua
    change = max(max(abs(x-xold)));
    disp([' It.: ' sprintf('%4i',loop) ' Obj.: ' sprintf('%10.4f',c) ...
          ' Vol.: ' sprintf('%6.3f',sum(sum(x))/(nelx*nely)) ...
          ' ch.: ' sprintf('%6.3f',change )])
          
    % Ve bieu do
    colormap(gray); imagesc(-x); axis equal; axis tight; axis off;drawnow;
end
end

%%%%%%%%%% CAC HAM CON (LOCAL FUNCTIONS) %%%%%%%%%%

function [dcn] = check(nelx,nely,rmin,x,dc)
dcn = zeros(nely,nelx);
for i = 1:nelx
  for j = 1:nely
    sum = 0;
    for k = max(i-floor(rmin),1):min(i+floor(rmin),nelx)
      for l = max(j-floor(rmin),1):min(j+floor(rmin),nely)
        fac = rmin-sqrt((i-k)^2+(j-l)^2);
        sum = sum+max(0,fac);
        dcn(j,i) = dcn(j,i) + max(0,fac)*x(l,k)*dc(l,k);
      end
    end
    dcn(j,i) = dcn(j,i)/(x(j,i)*sum);
  end
end
end

function [U] = FE(nelx,nely,x,penal,nLoadCase)
[KE] = localK;
K = sparse(2*(nelx+1)*(nely+1), 2*(nelx+1)*(nely+1));
F = sparse(2*(nely+1)*(nelx+1),nLoadCase); 
U = sparse(2*(nely+1)*(nelx+1),nLoadCase);

for elx = 1:nelx
    for ely = 1:nely
        n1 = (nely+1)*(elx-1)+ely; 
        n2 = (nely+1)* elx   +ely;
        edof = [2*n1-1; 2*n1; 2*n2-1; 2*n2; 2*n2+1; 2*n2+2; 2*n1+1; 2*n1+2];
        K(edof,edof) = K(edof,edof) + x(ely,elx)^penal*KE;
    end
end

% DIEU KIEN BIEN (MBB Beam)
F(2,1) = -1;
fixeddofs = union([1:2:2*(nely+1)],[2*(nelx+1)*(nely+1)]);

alldofs = [1:2*(nely+1)*(nelx+1)];
freedofs = setdiff(alldofs,fixeddofs);

U(freedofs,:) = K(freedofs,freedofs) \ F(freedofs,:);
U(fixeddofs,:) = 0;
end

function [KE] = localK
E = 1.; 
nu = 0.3;
k = [ 1/2-nu/6   1/8+nu/8 -1/4-nu/12 -1/8+3*nu/8 ... 
     -1/4+nu/12 -1/8-nu/8  nu/6       1/8-3*nu/8 ];
KE = E/(1-nu^2)*[ k(1) k(2) k(3) k(4) k(5) k(6) k(7) k(8)
                  k(2) k(1) k(8) k(7) k(6) k(5) k(4) k(3)
                  k(3) k(8) k(1) k(6) k(7) k(4) k(5) k(2)
                  k(4) k(7) k(6) k(1) k(8) k(3) k(2) k(5)
                  k(5) k(6) k(7) k(8) k(1) k(2) k(3) k(4)
                  k(6) k(5) k(4) k(3) k(2) k(1) k(8) k(7)
                  k(7) k(4) k(5) k(2) k(3) k(8) k(1) k(6)
                  k(8) k(3) k(2) k(5) k(4) k(7) k(6) k(1)];
end

function [xnew] = OC(nelx,nely,x,volfrac,dc,passive)
l1 = 0; l2 = 100000; move = 0.1;
while (l2-l1 > 1e-4)
    lmid = 0.5*(l2+l1);
    xnew = max(0.001,max(x-move,min(1,min(x+move,x.*sqrt(-dc./lmid)))));
    if ~isempty(passive)
        xnew(passive==1) = 0.001; 
    end
    if sum(sum(xnew)) - volfrac*nelx*nely > 0
        l1 = lmid;
    else
        l2 = lmid;
    end
end
end