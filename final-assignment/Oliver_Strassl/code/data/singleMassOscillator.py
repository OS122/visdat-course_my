
import os
import sys
import numpy as np
from ctypes import *
import matplotlib.pyplot as plt

sys.path.insert(0, 'C:\\Users\\olive\\OneDrive\\Dokumente\\Freedyn\\FreeDynAPI_2024.9\\FreeDynAPI\\fdApi')
import fdApi

## define directories
#define path of example FreeDyn Input file (FDS)
fdsFilePath = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'singleMassOscillator.fds'))

## initialize FreeDyn API
fdApi.init()

## create model by passing path to model file (.fds)
modelIndex = fdApi.createModel(fdsFilePath,'no')
if(modelIndex < 0):
    sys.exit()

## set model as active (so that there is no need for passing modelIndex in future calls)
fdApi.setModelAsActive(modelIndex)

## get model infos
modelInfos = fdApi.getModelInfos()
print("model infos:")
print("\tnumAllDofs: "   + str(modelInfos["numAllDofs"]))
print("\tnumPhyDofs: "   + str(modelInfos["numPhyDofs"]))
print("\tnumIntDof: "    + str(modelInfos["numIntDof"]))
print("\tnumExtDof: "    + str(modelInfos["numExtDof"]))
print("\tnumBodies: "    + str(modelInfos["numBodies"]))
print("\tnumExtConstr: " + str(modelInfos["numExtConstr"]))
print("\tnumForces: "    + str(modelInfos["numForces"]))
print("\tnumMeasures: "  + str(modelInfos["numMeasures"]))

## start simulation (simulation and solver settings according to .fds file)
solveEomSuc = fdApi.solveEoM()
if(solveEomSuc < 0):
    print("Simulation not successful!")
    sys.exit()

## postprocessing
# get number of time steps
nTimeSteps = fdApi.getNumTimeSteps()

## read states and filter Y-displacements
states = fdApi.generateStateVectors()
time = np.zeros((nTimeSteps,1))
yCoord = np.zeros((nTimeSteps,1))
for i in range(nTimeSteps):
    time[i,0] = fdApi.getStatesAtTimeIndex(i,states["Q"])
    yCoord[i,0] = states["Q"][1,0]

## plot results
plt.ion()
plt.plot(time, yCoord)
plt.xlabel('time [s]')
plt.ylabel('displacement [m]')
plt.grid(True)
plt.show()

## read and plot measure "mea_y"
vMeasures = fdApi.generateMeasureVector()

measureNames = fdApi.getMeasureNames()
meaIndex = measureNames.index("mea_y")
yCoord = np.zeros((nTimeSteps,1))
for i in range(nTimeSteps):
    fdApi.getMeasuresAtTimeIndex(i, vMeasures)
    yCoord[i,0] = vMeasures[meaIndex,0]

## plot results
plt.plot(time, yCoord)
plt.xlabel('time [s]')
plt.ylabel('displacement [m]')
plt.grid(True)
plt.show()

## delete model after last interaction
fdApi.deleteModel(modelIndex)

# Keep the plot open at the end
plt.ioff()
plt.show()