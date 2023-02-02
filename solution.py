import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
class SOLUTION:
    def __init__(self, id):
        self.weights = np.zeros((c.numSensorNeurons, c.numMotorNeurons))
        for i in range(c.numSensorNeurons):
            for j in range(c.numMotorNeurons):
                self.weights[i,j] = np.random.rand()
        self.weights = self.weights*2-1
        self.myID = id

    def Start_Simulation(self, st):
        self.Create_World()
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
        self.Create_Body()
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)
        self.Create_Brain(self.myID)
        while not os.path.exists("brain" + str(self.myID) + ".nndf"):
            time.sleep(0.01)
      #
       # print(st)
        if st == "GUI":
            os.system("py hwi.py " + st + " " + str(self.myID))
        else:
            os.system("start /B py hwi.py " + st + " "+ str(self.myID))
       # os.system("py hwi.py " + st   + " " + str(self.myID))
    
    def Wait_For_Simulation_To_End(self):
      #  print("simulation" + str(self.myID))
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        del_string = "fitness" + str(self.myID) + ".txt"
      #  print(del_string)
        print("Fitness: " + str(self.fitness))
        os.remove(del_string)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="rectangle", pos=[0, 3, 1] , size=[5, 8, 1])
        pyrosim.Send_Cube(name="rectangle2", pos=[0, 0, 2] , size=[4, 4, 1])
        pyrosim.Send_Cube(name="rectangle3", pos=[3.5, 0, 4] , size=[2, 5, 8])
        pyrosim.Send_Cube(name="rectangle4", pos=[-3.5, 0, 4] , size=[2, 5, 8])

        pyrosim.End()

    # def Create_Body(self):
    #     pyrosim.Start_URDF("body.urdf")
    #     pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5] , size=[1, 1, 1])
    #     pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [-0.5, 0, 1])
    #     pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5] , size=[1, 1, 1])
    #     pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0.5, 0, 1])
    #     pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5] , size=[1, 1, 1])
    #     pyrosim.End()
    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 4] , size=[1, 1, 1])
        pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [0, 0.5, 4], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0] , size=[0.3, 1, 0.3])
        pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [0, -0.5, 4], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0] , size=[0.3, 1, 0.3])
        pyrosim.Send_Joint( name = "Torso_LeftLeg", parent = "Torso", child = "LeftLeg", type = "revolute", position = [-0.5, 0, 4], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.5, 0, 0] , size=[1, 0.3, 0.3])
        pyrosim.Send_Joint( name = "Torso_RightTorso", parent = "Torso", child = "RightTorso", type = "revolute", position = [0.5, 0, 4], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="RightTorso", pos=[0.25, 0, 0] , size=[1, 0.2, 0.5])
        pyrosim.Send_Joint( name = "RightTorso_TopTorso", parent = "RightTorso", child = "TopTorso", type = "revolute", position = [0, 0, 0.5], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="TopTorso", pos=[0.25, 0, 0] , size=[1, 0.2, 0.5])
        pyrosim.Send_Joint( name = "FrontLeg_FrontLowerLeg", parent = "FrontLeg", child = "FrontLowerLeg", type = "revolute", position = [0 , 1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="FrontLowerLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 2])
        pyrosim.Send_Joint( name = "BackLeg_BackLowerLeg", parent = "BackLeg", child = "BackLowerLeg", type = "revolute", position = [0 , -1, 0], jointAxis = "1 0 0")
        pyrosim.Send_Cube(name="BackLowerLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 2])
        pyrosim.Send_Joint( name = "LeftLeg_BackLeftLeg", parent = "LeftLeg", child = "BackLeftLeg", type = "revolute", position = [-1, 0, 0], jointAxis = "0 1 0")
        pyrosim.Send_Cube(name="BackLeftLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 2])
        #pyrosim.Send_Joint( name = "RightLeg_BackRightLeg", parent = "RightLeg", child = "BackRightLeg", type = "revolute", position = [1, 0, 0], jointAxis = "0 1 0")
        #pyrosim.Send_Cube(name="BackRightLeg", pos=[0, 0, -0.5] , size=[0.2, 0.2, 1])
        pyrosim.End()

    def Create_Brain(self,id):
        pyrosim.Start_NeuralNetwork("brain" + str(id) + ".nndf")
        linkNamelist = ["FrontLowerLeg", "BackLowerLeg", "BackLeftLeg"]#, "BackRightLeg"]
        jointNamelist = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightTorso", "RightTorso_TopTorso", "FrontLeg_FrontLowerLeg", "BackLeg_BackLowerLeg", "LeftLeg_BackLeftLeg"]#, "RightLeg_BackRightLeg", "Torso_RightLeg",]
        for num in range(c.numSensorNeurons):
           pyrosim.Send_Sensor_Neuron(name = num, linkName = linkNamelist[num]) 
        for nums in range(c.numMotorNeurons):
            pyrosim.Send_Motor_Neuron( name = nums+c.numSensorNeurons , jointName = jointNamelist[nums])

        for currentRow in range(c.numSensorNeurons-1):
            for currentColumn in range(c.numMotorNeurons-1):
                pyrosim.Send_Synapse(sourceNeuronName= currentRow, targetNeuronName= currentColumn + c.numSensorNeurons, weight= self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Mutate(self):
        sensor = random.randint(0, c.numSensorNeurons-1)
        motor = random.randint(0, c.numMotorNeurons-1)
        self.weights[sensor, motor] = random.random() * 2 - 1
        
    def SetID(self, id):
        self.myID = id