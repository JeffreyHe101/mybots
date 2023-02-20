import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
class SOLUTION:
    def __init__(self, id):
        self.weights = 1 #initializing all the selfs
        self.blocks = 1
        self.sensor_list = []
        self.sensor_num = 0
        self.motor_num = 0
        self.myID = id
        self.joints_list = []
        self.joints_dir = {}
        self.collision = {}

    def Start_Simulation(self, st):
        self.Create_World() # make sure world and body and brain are created before used
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
        self.Create_Body()
        while not os.path.exists("body.urdf"):
            time.sleep(0.01)
        self.Create_Brain(self.myID)
        while not os.path.exists("brain" + str(self.myID) + ".nndf"):
            time.sleep(0.01)
        if st == "GUI":
            os.system("py hwi.py " + st + " " + str(self.myID)) #hwi is the program that runs simulation
        else:
            os.system("start /B py hwi.py " + st + " "+ str(self.myID)) #if no GUI run direct
    
    def Wait_For_Simulation_To_End(self): #prints fitness
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        del_string = "fitness" + str(self.myID) + ".txt"
        print("Fitness: " + str(self.fitness))
        os.remove(del_string)

    def Create_World(self): #starts empty world
        pyrosim.Start_SDF("world.sdf")

        pyrosim.End()

    def joint_maker(self, prev, curr, a):# Determines the next joint position relative to the previous joint for the block and the projected face
        pos = [0, 0, 0] #relative position starts at 0
        if prev == 1:# prev is the previous joint, depending on which direction it faces the next joint is projected by half the distance
            pos[0] = pos[0] + a[0]/2 #the x,y,z position are modified for both previous joint and current joint positioning.
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
        return pos #return corrected joint position

    def Create_Body(self):
        self.joints_list = [] #list of joint names
        self.sensor_list = [] # list of sensors
        block_list_dim_dict = {}  #dictionary of link sizes in xyz
        open_spots_dict = {} #dictionary storing open faces for each link
        self.blocks = random.randint(5, 15) #random number of links
        for i in range(self.blocks):
            if random.random() < .5:
                self.sensor_list.append(i) #randomize sensors
        self.sensor_num = len(self.sensor_list) #records number of sensors
        pyrosim.Start_URDF("body.urdf")
        for i in range(self.blocks): #create randomized xyz for each link
            x_side = random.random()+0.2 #not too small
            y_side = random.random()+0.2
            z_side = random.random()+0.2
            block_list_dim_dict[i] = [x_side, y_side, z_side]
        open_spots_dict[0] = [1, 2, 3, 4, 5] #dont allow -z direction so it doesn't go into the floor as often, every other side is possible
        link_joint = random.randint(1, 5) #pick random face for first link
        open_spots_dict[0].remove(link_joint) #remove from dictionary of open faces
        joint_made = str(0) + '_' + str(1) #title joint from parent and child
        self.joints_list.append(joint_made) #adds joints into joint_list
        varrr = block_list_dim_dict[0] #dimensions of first link
        temp1 = block_list_dim_dict[1] #dimensions of second link
        self.joints_dir[1] = link_joint #joint direction of first joint
        self.collision[0] = [0, 0, 0] #relative position of first link
        if 0 in self.sensor_list: #if first block is sensor, make green otherwise cyan
            pyrosim.Send_Cube(str1='<material name="Green">', str2='    <color rgba="0 1.0 0.0 1.0"/>', name=str(0), pos=[0, 0, 0] , size=varrr)
        else:
            pyrosim.Send_Cube(str1='<material name="Cyan">', str2='    <color rgba="0 1.0 1.0 1.0"/>', name=str(0), pos=[0, 0, 0] , size=varrr)
        if link_joint == 1: #if +x direction, create open spots without -x, set new block position to 1,0,0. Make joint and link.
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
        
        for j in range(2,self.blocks): #for following joints and links
            temp = 0 #temp variable for while loop
            temp3 = False #2nd temp variable for 2nd while loop/
            while temp3 == False: #outer while loop to make sure 
                while (temp) <= 0:#inner while loop to make sure that the link selected has possible faces to proceed on.
                    joint_spot_from = random.randint(1,j-1) #which link to connect to
                    temp = len(open_spots_dict[joint_spot_from])-1 #open faces for link
                link_joint = random.randint(0, len(open_spots_dict[joint_spot_from])-1) #which face on the opening to connect to
                a = open_spots_dict[joint_spot_from] #Correct link
                link_joint = a[link_joint]
                prev_block_coord = self.collision[joint_spot_from] #previous link relative coordinate
                if link_joint == 1: #potential new link relative coordinate
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
                if new_block_coord[2] >= 0: #check if the new link position is already in the dictionary, if so redo.
                    if new_block_coord not in [*self.collision.values()]:
                        temp3 = True
                        self.collision[j] = new_block_coord # add new link position to dictionary with relative position of each link
            open_spots_dict[joint_spot_from].remove(link_joint) #remove opening from previous
            joint_made = str(joint_spot_from) + "_" + str(j) #make joint
            self.joints_list.append(joint_made) #add to list of joints
            temp = block_list_dim_dict[j] #dimensions of current link
            prev = block_list_dim_dict[joint_spot_from] #dimensions of link connecting from
            self.joints_dir[j] = link_joint #add joint direction to dictionary

            poss = self.joint_maker(self.joints_dir[joint_spot_from], link_joint, prev) #sets joint position
            if link_joint == 1: #remove opposing availability for new block
                open_spots_dict[j] = [1, 3, 4, 5, 6] #set new openings, and makes sensor cube or non sensor as set below.
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
        print(self.joints_list) #prints joint list
        pyrosim.End()

    def Create_Brain(self,id):
        pyrosim.Start_NeuralNetwork("brain" + str(id) + ".nndf")
        sensors = 0
        motors = 0
        for num in range(self.blocks):
            if num in self.sensor_list: #sensors based off links
                pyrosim.Send_Sensor_Neuron(name = sensors, linkName = str(num)) 
                sensors += 1
        for i in range(self.blocks):
            if i < self.blocks - 1:    #motors based off joints
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