from simulation import SIMULATION
import sys
directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
#print(sys.argv)
#print(directOrGUI)
#print("gui: ")
#print(directOrGUI)
#print(solutionID)
sim = SIMULATION(directOrGUI, solutionID)
sim.Run()
sim.Get_Fitness()