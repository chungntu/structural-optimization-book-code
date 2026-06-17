%% Structural Truss Problems Benchmark Suite
% Please Cite : Ozturk, H.T., Kahraman H.T., (2023) "Meta-heuristic Search Algorithms in Truss Optimization:
% Research on Stability and Complexity, Applied Soft Computing, (in press).

%% Settings
% Select Problem
% 1 : 17  Bar Planar Truss Problem
% 2 : 18  Bar Planar Truss Problem
% 3 : 200 Bar Planar Truss Problem
% 4 : 25  Bar Space Truss Problem
% 5 : 72  Bar Space Truss Problem
% 6 : 120 Bar Space Truss Problem
% 7 : 10  Bar Truss Problem with Frequency Constraint 
% 8 : 37  Bar Truss Problem with Frequency Constraint 
% 9 : 52  Bar Truss Problem with Frequency Constraint 
problem_type = 6;

% Select Algorithm
% 1 : FDB_AGDE_Case1
% 2 : FDB_AGDE_Case2
% 3 : FDB_AGDE_Case3
Algo_type = 1;
                     
OPTIM_DATA.POP = 50 ;               % Population size
OPTIM_DATA.RT = 1;                 % Runtime
OPTIM_DATA.MXFE_D = 10000;          % maxFEs = OPTIM_DATA.MXFE_D * D


%% MAIN CODE

switch problem_type
            case 1
            OPTIM_DATA.ObjectiveFunction = @(Indi) Truss_analysis_17bar(Indi);

            case 2
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_analysis_18bar(Individual);

            case 3
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_analysis_200bar(Individual);

			case 4
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_analysis_25bar(Individual);

			case 5
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_analysis_72bar(Individual);

			case 6
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_analysis_120bar(Individual);

            case 7
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_modal_analysis_10bar(Individual);

            case 8          			
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_modal_analysis_37bar(Individual);

            case 9
            OPTIM_DATA.ObjectiveFunction = @(Individual) Truss_modal_analysis_52bar(Individual);

end
			
[OPTIM_DATA.LB OPTIM_DATA.UB]=problem_bounds(problem_type);


switch Algo_type

	case 1
	FDB_AGDE_Case1(OPTIM_DATA)
	case 2
	FDB_AGDE_Case2(OPTIM_DATA)
	case 3
	FDB_AGDE_Case3(OPTIM_DATA)
	
end
	
