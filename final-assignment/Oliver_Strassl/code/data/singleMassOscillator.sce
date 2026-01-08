clc
clear

//----------------------------------------------------------------------
// I N I T I A L I Z A T I O N  O F  F R E E D Y N  A P I
//----------------------------------------------------------------------
// define directories
//change directory to directory where FreeDynAPI is located
cd('C:/me/mbs/public_release/FreeDynAPI');
//FreeDynAPI is located in bin directory
fdApiDir = fullfile(pwd(),"bin");
//define path of example FreeDyn Input file (FDS)
fdsFilePath = 'demo\demo_01\singleMassOscillator.fds';
//run API sce file
exec("fdApi\fdApi.sce",-1);
// call main function of fdApi => get API-function handles
fdApi(fdApiDir);
//----------------------------------------------------------------------

// create model by passing path to model file (.fds)
[modelIndex,errorString] = fdApi_createModel(fdsFilePath,'screen');
if(stripblanks(errorString) ~= "")
    disp(errorString)
    return;
end

fdApi_setModelAsActive(modelIndex);

// start simulation (simulation and solver settings according to .fds file)
solveEomSuc = fdApi_solveEoM();
if(~solveEomSuc)
    disp("Simulation not successful!");
    return;
end

//----------------------------------------------------------------------
// P O S T P R O C E S S I N G
//----------------------------------------------------------------------
// get number of time steps
nTimeSteps = fdApi_getNumTimeSteps();

//read states and filter Y-displacements
[vQ,vQd,vQdd,vL] = fdApi_generateStateVecs();
time = zeros(nTimeSteps,1);
yCoord = zeros(nTimeSteps,1);
for i = 1:nTimeSteps
    [time(i,1),vQ] = fdApi_getStatesAtTimeInd(i,vQ);  
    yCoord(i,1) = vQ(2);
end

//----------------------------------------------------------------------
// P L O T  R E S U L T S
//----------------------------------------------------------------------
scf(1)
plot(time,yCoord);
a=gca();
a.data_bounds = [0,-0.05;1.,0.2];
a.children(1).children(1).foreground = 2;
a.children(1).children(1).thickness = 2;
a.x_label.text = "$\text{time [s]}$";
a.x_label.font_size = 3;
a.y_label.text = "$\text{y-coordinate [m]}$";
a.y_label.font_size = 3;
a.grid = [1,1];

// read and plot measure "mea_y"
meaVals = fdApi_generateMeaVec();
meaIndex = find(stripblanks(fdApi_getMeasureNames()) == "mea_y",1);
time = zeros(nTimeSteps,1);
yCoord = zeros(nTimeSteps,1);
for i = 1:nTimeSteps
    [time(i,1),meaVals] = fdApi_getMeaAtTimeIndex(i,meaVals);   
    yCoord(i,1) = meaVals(meaIndex);
end

//plot results
scf(2)
plot(time,yCoord);
a=gca();
a.data_bounds = [0,-0.05;1.,0.2];
a.children(1).children(1).foreground = 2;
a.children(1).children(1).thickness = 2;
a.x_label.text = "$\text{time [s]}$";
a.x_label.font_size = 3;
a.y_label.text = "$\text{y-coordinate [m]}$";
a.y_label.font_size = 3;
a.grid = [1,1];

// delete model after last interaction
fdApi_deleteModel(modelIndex);
