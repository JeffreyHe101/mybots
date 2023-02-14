import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
class SOLUTION:
    def __init__(self, id):
        self.weights = 1
        self.blocks = 1
        self.sensor_list = []
        self.sensor_num = 0
        self.motor_num = 0
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
        if st == "GUI":
            os.system("py hwi.py " + st + " " + str(self.myID))
        else:
            os.system("start /B py hwi.py " + st + " "+ str(self.myID))
    
    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        del_string = "fitness" + str(self.myID) + ".txt"
        print("Fitness: " + str(self.fitness))
        os.remove(del_string)

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")

        pyrosim.End()

    def Create_Body(self):
        self.sensor_list = []
        self.blocks = random.randint(10, 20)
        for i in range(self.blocks):
            if random.random() < 0.5:
                self.sensor_list.append(i)
        self.sensor_num = len(self.sensor_list)
        pyrosim.Start_URDF("body.urdf")
        xnext, ynext, znext = 0, 0, 0
        for i in range(self.blocks):
            xdim, ydim, zdim = xnext, ynext, znext
            if i == 0:
                xdim, ydim, zdim, xnext, ynext, znext = random.random(), random.random(), random.random(), random.random(), random.random(), random.random()
                if i in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(i), pos=[0, 0, zdim/2] , size=[xdim,ydim,zdim])
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(i), pos=[0, 0, zdim/2] , size=[xdim,ydim,zdim])
                pyrosim.Send_Joint( name = str(i)+"_"+str(i+1) , parent= str(i) , child =  str(i+1), type = "revolute", position = [xdim/2-xnext, 0, 0], jointAxis = "0 0 1")
            elif i == (self.blocks-1):
                if i in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(i), pos=[0, 0, zdim/2] , size=[xdim,ydim,zdim])
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(i), pos=[0, 0, zdim/2] , size=[xdim,ydim,zdim]) 
            else:
                if i in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(i), pos=[0, 0, zdim/2] , size=[xdim,ydim,zdim])
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(i), pos=[0, 0, zdim/2] , size=[xdim,ydim,zdim]) 
                    xnext = random.random()
                    ynext = random.random()
                    znext = random.random()
                pyrosim.Send_Joint( name = str(i)+"_"+str(i+1) , parent= str(i) , child =  str(i+1), type = "revolute", position = [xdim/2 - xnext, 0, 0], jointAxis = "0 0 1")
        pyrosim.End()

    def Create_Brain(self,id):
        pyrosim.Start_NeuralNetwork("brain" + str(id) + ".nndf")
        sensors = 0
        motors = 0
        for num in range(self.blocks):
            if num in self.sensor_list:
                pyrosim.Send_Sensor_Neuron(name = sensors, linkName = str(num)) 
                sensors += 1
        for i in range(self.blocks):
            if i < self.blocks - 1:    
                pyrosim.Send_Motor_Neuron( name = sensors + motors , jointName = str(i)+"_"+str(i+1))
                motors += 1
        self.motor_num = motors
        self.weights = np.random.rand(sensors, motors)
        self.weights = self.weights * 2 -1
        for currentRow in range(sensors):
            for currentColumn in range(motors):
                pyrosim.Send_Synapse(sourceNeuronName= currentRow, targetNeuronName= currentColumn + sensors, weight= self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Mutate(self):
        sensor = random.randint(0, self.sensor_num -1)
        motor = random.randint(0, self.motor_num-1)
        self.weights[sensor, motor] = random.random() * 2 - 1
        
    def SetID(self, id):
        self.myID = id