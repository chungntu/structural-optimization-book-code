function FDB_AGDE_Case3(OPTIM_DATA)
%% PARAMETERS
UB=OPTIM_DATA.UB;
LB=OPTIM_DATA.LB;
RT=OPTIM_DATA.RT;
MXFE_D=OPTIM_DATA.MXFE_D;
POP=OPTIM_DATA.POP;
ObjectiveFunction=OPTIM_DATA.ObjectiveFunction;
D=size(LB,2);
MXFE=MXFE_D*D;

%% ALGORITHM
run=1;

while(run<=RT)
    X = zeros(1,D); % trial vector
population = zeros(POP,D); % population
Fit = zeros(1,POP); % fitness of the population
r = zeros(3,1); % randomly selected indices
rand('state',sum(100*clock));
 FES(1)=0;
 FUNCEVA=0;
 tStart(run)=tic;
 
for j = 1:POP % initialize each individual
    population(j,:) = LB + ((UB-LB).*rand(1,D)); % within b.constraints
    [TRUSS]=ObjectiveFunction(population(j,:));
    Fit(1,j)=TRUSS.PENALIZED;
    FES(1)=FES(1)+1;
    FUNCEVA=FUNCEVA+1;
end

[~, iBest]=min(Fit);

Cr_All=zeros(1,2);
NW=zeros(1,2);

iter=1;

while   FUNCEVA<MXFE
    if iter~=1
    FES(iter)=FES(iter-1);
    end
    
    CrPriods_Index=zeros(1,POP);
    Sr=zeros(1,2);
    CrPriods_Count=zeros(1,2);
    for j = 1:POP % for each individual
         %%%%%%%%ADAPTIVE CR RULE  %%%%%%%%%%%%%%%%%%%%%%%%%
            Ali = rand;
            if(iter<=1) % Do for the first Generation
                if (Ali<=1/2)
                    CR=0.05+0.1*rand(1,1);
                    CrPriods_Index(j)=1;
                
                else
                    CR=0.9+0.1*rand(1,1);
                    CrPriods_Index(j)=2;    
                end
                CrPriods_Count(CrPriods_Index(j))=CrPriods_Count(CrPriods_Index(j)) + 1;
            else
                 if (Ali<=NW(1))
                    CR=0.05+0.1*rand(1,1);
                    CrPriods_Index(j)=1;
                
                 else
                    CR=0.9+0.1*rand(1,1);
                    CrPriods_Index(j)=2;    
                end
                CrPriods_Count(CrPriods_Index(j))=CrPriods_Count(CrPriods_Index(j)) + 1;
            end

            %%%%%%%%%%%%%%%%%END OF CR RULE%%%%%%%%%%%%%%%%%%%%%%%%%%%
                f=Fit;
                [~, in]=sort(f,'ascend');%fdb 
            index_im=round(0.10*POP);
            AA=[in(1:index_im)];
            BB=[in(POP-index_im+1:POP)];
            CC=[in(index_im+1:POP-index_im)];   
                 
               
            % choose three random individuals from population,
            % mutually different 
                paraIndex=floor (rand(1,1)*length(AA))+1;
                paraIndex1=floor (rand(1,1)*length(BB))+1;
                r(1) = AA(paraIndex);
                r(2) = BB(paraIndex1);
                r(3) = rouletteFitnessDistanceBalance(population, Fit);

                F=0.1+0.9*rand(1,1);
               
                Rnd = floor(rand()*D) + 1;
                for i = 1:D
                    if ( rand()<CR ) || ( Rnd==i )
                        X(i)=population(r(3),i)+(F*(population(r(1),i)-(population(r(2),i))));
                    else
                        X(i) = population(j,i);
                    end
                end
        % end%end of All cases
        % verify boundary constraints
        % verify boundary constraints
        for i = 1:D
            if (X(i)<LB(i))||(X(i)>UB(i))
                X(i) = LB(i) + ((UB(i)-LB(i))*rand());
            end
        end
        % select the best individual
        % between trial and current ones
        % calculate fitness of trial individual   
      	[TRUSS]=ObjectiveFunction(X);
     	f=TRUSS.PENALIZED;
        FES(iter)=FES(iter)+1;
       	FUNCEVA=FUNCEVA+1; 
        % if trial is better or equal than current
        if f <= Fit(j)
            % CRRatio(find(A==CRs(j)))=CRRatio(find(A==CRs(j)))+1-(min(f,Fit(j))/max(f,Fit(j)));
           Sr (CrPriods_Index(j)) = Sr(CrPriods_Index(j)) +1;
            population(j,:) = X; % replace current by trial
            Fit(j) = f ;
            % if trial is better than the best
            if f <= Fit(iBest)
                iBest = j ; % update the best痴 index
            end
        else
        end
    end
    CrPriods_Count(CrPriods_Count==0)=0.0001;
    Sr=Sr./CrPriods_Count;
%%%%%%%%%%%%%%%%USING SR ONLY%%%%%%%%%%5    
    if(sum(Sr)==0)
        W=[1/2 1/2];
    else
        W=Sr/sum(Sr);
    end
    
%%%%%%%%%%%%%%%%%%%%%%%%%%5
    NW=(NW*(iter-1)+W)/iter;
    Cr_All=Cr_All+CrPriods_Count;
 
    
 [fmin,K]=min(Fit) ;
 BestBirey=population(K,:);
 BestCost(iter)=fmin;

    fprintf('Iter: %5.0f   FEs : %8d ---> Obj. Func : %10.3f \n',iter,FES(iter),BestCost(iter))

iter=iter+1;    
    
end
[val,ind]=min(BestCost);
SUM_FUNCEVA(run)=FUNCEVA;
Fes(run)=FES(ind);
MxFes(run)=FES(end);
bestt(run)=val;
BESTITER(run)=ind;
GlobalParams(run,:)=BestBirey;
tEnd(run)=toc(tStart(run));

run=run+1;
end

fprintf('*****  BEST SOLUTION ************************************* \n');
[val_eniyi,ind_eniyi]=min(bestt);
fprintf('Best Solution run number = %d \n',ind_eniyi);
fprintf('Best Solution            = %f \n',val_eniyi);
fprintf('Best Design Variables    : \n');
fprintf('%g\t',GlobalParams(ind_eniyi,:));
fprintf('\n\n');
fprintf('********************************************************** \n');
for kk=1:RT
fprintf('RUN %2d --> Best Solution = %f || Calculation Duration : %.2f s\n',kk,bestt(kk),tEnd(kk));
end
end