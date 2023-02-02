from robot import ROBOT
from world import WORLD
import pybullet as p
import pyrosim.pyrosim as pyrosim
import time
import pybullet_data
import constants as c
class SIMULATION:
    def __init__(self, st, solutionID):
        self.directOrGUI = st
        self.solutionID = solutionID
        if self.directOrGUI == "GUI":
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)    
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)
        pyrosim.Prepare_To_Simulate(self.robot.robotId)
        self.robot.Prepare_To_Sense()
        self.robot.Prepare_To_Act()


    def Run(self):
        for i in range(c.iter):
           # print(i)
            p.stepSimulation()
            self.robot.Sense(i)
            self.robot.Think()
            self.robot.Act(i)
        #    print(self.directOrGUI)
            if self.directOrGUI == "GUI":
                time.sleep(c.sleep_time)

    def __del__(self):
        #self.robot.Save_data()
        p.disconnect()
    
    def Get_Fitness(self):
        self.robot.Get_Fitness(self.solutionID)
