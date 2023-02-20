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
        self.joints_list = []
        self.joints_dir = {}
        self.collision = {}

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

    def checker(self, prev, curr, a):
        pos = [0, 0, 0]
        if prev == 1:
            pos[0] = pos[0] + a[0]/2
        elif prev == 2:
            pos[0] = pos[0] - a[0]/2
        elif prev == 3:
            pos[1] = pos[1] + a[1]/2
        elif prev == 4:
            pos[1] = pos[1] - a[1]/2
        elif prev == 5:
            pos[2] = pos[2] + a[2]/2
        elif prev == 6:
            pos[2] = pos[2] - a[2]/2
        if curr == 1:
            pos[0] = pos[0] + a[0]/2
        elif curr == 2:
            pos[0] = pos[0] - a[0]/2
        elif curr == 3:
            pos[1] = pos[1] + a[1]/2
        elif curr == 4:
            pos[1] = pos[1] - a[1]/2
        elif curr == 5:
            pos[2] = pos[2] + a[2]/2
        elif curr == 6:
            pos[2] = pos[2] - a[2]/2
        return pos

    def Create_Body(self):
        self.joints_list = []
        self.sensor_list = []
        self.blocks = 8
        for i in range(self.blocks):
            if random.random() < .5:
                self.sensor_list.append(i)
        self.sensor_num = len(self.sensor_list)
        pyrosim.Start_URDF("body.urdf")
        block_list_dim_dict = {}
        for i in range(self.blocks):
            x_side = random.random()+0.2
            y_side = random.random()+0.2
            z_side = random.random()+0.2
            block_list_dim_dict[i] = [x_side, y_side, z_side]
        block_list_pos_dict = {}
        block_list_pos_dict[0] = [(0, block_list_dim_dict[0][0]), (0, block_list_dim_dict[0][1]), (0, block_list_dim_dict[0][2])]
        open_spots_dict = {}
        open_spots_dict[0] = [1, 2, 3, 4, 5]
        link_joint = random.randint(1, 5) 
        open_spots_dict[0].remove(link_joint)
        joint_made = '0' + '_' + str(1)
        self.joints_list.append(joint_made)
        varrr = block_list_dim_dict[0]
        temp1 = block_list_dim_dict[1]
        self.joints_dir[1] = link_joint
        self.collision[0] = [0, 0, 0]
        if 0 in self.sensor_list:
            pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(0), pos=[0, 0, 0] , size=varrr)
        else:
            pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(0), pos=[0, 0, 0] , size=varrr)
        if link_joint == 1:
            open_spots_dict[1] = [1, 3, 4, 5, 6]
            self.collision[1] = [1, 0, 0]
            pyrosim.Send_Joint( name = str(0)+"_"+str(1) , parent= str(0) , child =  str(1), type = "revolute", position = [varrr[0]/2, 0, 0], jointAxis = "0 0 1")
            if 1 in self.sensor_list:
                pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(1), pos=[temp1[0]/2, 0, 0] , size=temp1)
            else:
                pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(1), pos=[temp1[0]/2, 0, 0] , size=temp1)
        elif link_joint == 2:
            open_spots_dict[1] = [2, 3, 4, 5, 6]
            self.collision[1] = [-1, 0, 0]
            pyrosim.Send_Joint( name = str(0)+"_"+str(1) , parent= str(0) , child =  str(1), type = "revolute", position = [-varrr[0]/2, 0, 0], jointAxis = "0 0 1")
            if 1 in self.sensor_list:
                pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(1), pos=[-temp1[0]/2, 0, 0] , size=temp1)
            else:
                pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(1), pos=[-temp1[0]/2, 0, 0] , size=temp1)
        elif link_joint == 3:
            open_spots_dict[1] = [1, 2, 3, 5, 6]
            self.collision[1] = [0, 1, 0]
            pyrosim.Send_Joint( name = str(0)+"_"+str(1) , parent= str(0) , child =  str(1), type = "revolute", position = [0, varrr[1]/2, 0], jointAxis = "1 0 1")
            if 1 in self.sensor_list:
                pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(1), pos=[0, temp1[1]/2, 0] , size=temp1)
            else:
                pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(1), pos=[0, temp1[1]/2, 0] , size=temp1)

        elif link_joint == 4:
            open_spots_dict[1] = [1, 2, 4, 5, 6]
            self.collision[1] = [0, -1, 0]
            pyrosim.Send_Joint( name = str(0)+"_"+str(1) , parent= str(0) , child =  str(1), type = "revolute", position = [0, -varrr[1]/2, 0], jointAxis = "1 0 1")
            if 1 in self.sensor_list:
                pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(1), pos=[0, -temp1[1]/2, 0] , size=temp1)
            else:
                pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(1), pos=[0, -temp1[1]/2, 0] , size=temp1)
        elif link_joint == 5:
            open_spots_dict[1] = [1, 2, 3, 4, 5]
            self.collision[1] = [0, 0, 1]
            pyrosim.Send_Joint( name = str(0)+"_"+str(1) , parent= str(0) , child =  str(1), type = "revolute", position = [0, 0, varrr[2]/2], jointAxis = "1 1 0")
            if 1 in self.sensor_list:
                pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(1), pos=[0, 0, temp1[2]/2] , size=temp1)
            else:
                pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(1), pos=[0, 0, temp1[2]/2] , size=temp1)
        
        for j in range(2,self.blocks):
            temp = 0
            temp3 = False
            while temp3 == False:
                while (temp) <= 0:
                    joint_spot_from = random.randint(1,j-1) #which block to connect to
                    temp = len(open_spots_dict[joint_spot_from])-1 
                link_joint = random.randint(0, len(open_spots_dict[joint_spot_from])-1) #which face on the opening to connect to
                a = open_spots_dict[joint_spot_from] #Correct block
                link_joint = a[link_joint]
                prev_block_coord = self.collision[joint_spot_from]
                if link_joint == 1:
                    new_block_coord = [prev_block_coord[0] + 1, prev_block_coord[1], prev_block_coord[2]]
                elif link_joint == 2:
                    new_block_coord = [prev_block_coord[0] - 1, prev_block_coord[1], prev_block_coord[2]]
                elif link_joint == 3:
                    new_block_coord = [prev_block_coord[0], prev_block_coord[1] + 1, prev_block_coord[2]]
                elif link_joint == 4:
                    new_block_coord = [prev_block_coord[0], prev_block_coord[1] - 1, prev_block_coord[2]]
                elif link_joint == 5:
                    new_block_coord = [prev_block_coord[0], prev_block_coord[1], prev_block_coord[2] + 1]
                elif link_joint == 6:
                    new_block_coord = [prev_block_coord[0], prev_block_coord[1], prev_block_coord[2] - 1]
                if new_block_coord[2] >= 0:
                    if new_block_coord not in [*self.collision.values()]:
                        temp3 = True
                        self.collision[j] = new_block_coord
            open_spots_dict[joint_spot_from].remove(link_joint) #remove opening from previous
            joint_made = str(joint_spot_from) + "_" + str(j) #make joint
            self.joints_list.append(joint_made) #add to list of joints
            temp = block_list_dim_dict[j]
            prev = block_list_dim_dict[joint_spot_from]
            self.joints_dir[j] = link_joint

            poss = self.checker(self.joints_dir[joint_spot_from], link_joint, prev)
            if link_joint == 1: #remove opposing availability for new block
                open_spots_dict[j] = [1, 3, 4, 5, 6]
                pyrosim.Send_Joint( name = joint_made , parent= str(joint_spot_from) , child =  str(j), type = "revolute", position = poss, jointAxis = "0 0 1")
                if j in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(j), pos=[temp[0]/2, 0, 0] , size=temp)
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(j), pos=[temp[0]/2, 0, 0] , size=temp)
            elif link_joint == 2:   
                open_spots_dict[j] = [2, 3, 4, 5, 6]
                pyrosim.Send_Joint( name = joint_made , parent= str(joint_spot_from) , child =  str(j), type = "revolute", position = poss, jointAxis = "0 0 1")
                if j in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(j), pos=[-temp[0]/2, 0, 0] , size=temp)
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(j), pos=[-temp[0]/2, 0, 0] , size=temp)
            elif link_joint == 3:
                open_spots_dict[j] = [1, 2, 3, 5, 6]
                pyrosim.Send_Joint( name = joint_made , parent= str(joint_spot_from) , child =  str(j), type = "revolute", position = poss, jointAxis = "1 0 1")
                if j in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(j), pos=[0, temp[1]/2, 0] , size=temp)
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(j), pos=[0, temp[1]/2, 0] , size=temp)
            elif link_joint == 4:
                open_spots_dict[j] = [1, 2, 4, 5, 6]
                pyrosim.Send_Joint( name = joint_made , parent= str(joint_spot_from) , child =  str(j), type = "revolute", position = poss, jointAxis = "1 0 1")
                if j in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(j), pos=[0, -temp[1]/2, 0] , size=temp)
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(j), pos=[0, -temp[1]/2, 0] , size=temp)
            elif link_joint == 5:
                open_spots_dict[j] = [1, 2, 3, 4, 5]
                pyrosim.Send_Joint( name = joint_made , parent= str(joint_spot_from) , child =  str(j), type = "revolute", position = poss, jointAxis = "1 1 0")
                if j in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(j), pos=[0, 0, temp[2]/2] , size=temp)
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(j), pos=[0, 0, temp[2]/2] , size=temp)
            elif link_joint == 6:
                open_spots_dict[j] = [1, 2, 3, 4, 6]
                pyrosim.Send_Joint( name = joint_made , parent= str(joint_spot_from) , child =  str(j), type = "revolute", position = poss, jointAxis = "1 1 0")
                if j in self.sensor_list:
                    pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(j), pos=[0, 0, -temp[2]/2] , size=temp)
                else:
                    pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(j), pos=[0, 0, -temp[2]/2] , size=temp)
        print(self.joints_list)
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
                pyrosim.Send_Motor_Neuron( name = sensors + motors , jointName = self.joints_list[i])
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