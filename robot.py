import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import constants as c
class ROBOT:
    def __init__(self, solutionID):
       # self.solutionID = solutionID
        self.robotId = p.loadURDF("body.urdf")  
        self.nn = NEURAL_NETWORK("brain" + solutionID + ".nndf")
        #print(solutionID)
        del_string = "brain" + solutionID + ".nndf"
       # print(del_string)
      #  os.system("py del " + del_string)
        os.remove(del_string)

    def Prepare_To_Sense(self):
        self.sensors = dict()
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = dict()
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)
    
    def Sense(self, i):
        for name in self.sensors.values():
            name.Get_Value(i)
    
    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[bytes(jointName.encode())].Set_Value(desiredAngle, self.robotId)

               # self.motors[jointName.Set_Value(desiredAngle, self.robotId)
              #  print("desiredAngle: " + str(desiredAngle))
              #  print("jointName: " + jointName)
               # print("neuronName: " + neuronName)
              #  print(" ")
       # for i in self.motors.values():
       #     i.Set_Value(t, self.robotId)

    def Save_Data(self):
        self.sensors.Save_Values()
        self.motors.Save_Values()

    def Think(self):
        self.nn.Update()
       # self.nn.Print()

    def Get_Fitness(self, solutionID):
        basePositionAndOrientation = p.getBasePositionAndOrientation(self.robotId)
        print(basePositionAndOrientation)
        basePosition = basePositionAndOrientation[0]
        xCoordinateOfLinkZero = basePosition[0]
        #stateOfLinkZero = p.getLinkState(self.robotId,0)    
        #positionOfLinkZero = stateOfLinkZero[0]
        #xCoordinateOfLinkZero = positionOfLinkZero[0]
       # print(stateOfLinkZero)
      #  print(positionOfLinkZero)
      #  print(xCoordinateOfLinkZero)
        #f = open("fitness" + self.solutionID + ".txt" , "w")\
        f = open("tmp" + str(solutionID) + ".txt" , "w")
        f.write(str(xCoordinateOfLinkZero))
        f.close()
        os.rename("tmp"+str(solutionID)+".txt" , "fitness"+str(solutionID)+".txt")
        #exit()
        