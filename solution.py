import numpy as np
import pyrosim.pyrosim as pyrosim
import os
import random
import time
class SOLUTION:
    def __init__(self, id):
        self.weights = 1 #initializing all the selfs
        self.blocks = 0
        self.sensor_list = []
        self.sensor_num = 0
        self.motor_num = 0
        self.myID = id
        self.joints_list = []
        self.joints_dir = {}
        self.collision = {}
        self.joints_dict = {}
        self.links_dict = {}
        self.outside_link = {}
        self.linksmade = self.blocks
        self.open_spots_dict = {}
        self.block_list_dim_dict = {}

    def Start_Simulation(self, st):
        self.Create_World() # make sure world and body and brain are created before used
        while not os.path.exists("world.sdf"):
            time.sleep(0.01)
        if self.blocks == 0:
            self.Create_Body()
            self.Create_Brain(self.myID)
        self.Create_Future()
        if self.blocks != 0:
            self.Update_Brain()
        while not os.path.exists("brain" + str(self.myID) + ".nndf"):
            time.sleep(0.01)
        #self.Create_brain2(self.myID)
        if st == "GUI":
            os.system("py hwi.py " + st + " " + str(self.myID)) #hwi is the program that runs simulation
        else:
            os.system("start /B py hwi.py " + st + " "+ str(self.myID)) #if no GUI run direct
    
    def Wait_For_Simulation_To_End(self): #prints fitness
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        while True:
            try:
                f = open("fitness" + str(self.myID) + ".txt", "r")
                break
            except:
                pass
        f = open("fitness" + str(self.myID) + ".txt", "r")
        self.fitness = float(f.read())
        f.close()
        del_string = "fitness" + str(self.myID) + ".txt"
        #print("Fitness: " + str(self.fitness))
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

    def add_joint_cube(self, j):# helper function to add subsequent joints and links.
        temp = 0 #temp variable for while loop
        temp3 = False #2nd temp variable for 2nd while loop/
        while temp3 == False: #outer while loop to make sure 
            while (temp) <= 0:#inner while loop to make sure that the link selected has possible faces to proceed on.
                joint_spot_from = random.randint(1,j-1) #which link to connect to
                temp = len(self.open_spots_dict[joint_spot_from])-1 #open faces for link
            link_joint = random.randint(0, len(self.open_spots_dict[joint_spot_from])-1) #which face on the opening to connect to
            a = self.open_spots_dict[joint_spot_from] #Correct link
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
        self.open_spots_dict[joint_spot_from].remove(link_joint) #remove opening from previous
        joint_made = str(joint_spot_from) + "_" + str(j) #make joint
        self.joints_list.append(joint_made) #add to list of joints
        temp = self.block_list_dim_dict[j] #dimensions of current link
        prev = self.block_list_dim_dict[joint_spot_from] #dimensions of link connecting from
        self.joints_dir[j] = link_joint #add joint direction to dictionary
        self.outside_link[joint_spot_from] = False
        self.outside_link[j] = True
        poss = self.joint_maker(self.joints_dir[joint_spot_from], link_joint, prev) #sets joint position
        if link_joint == 1: #remove opposing availability for new block
            self.open_spots_dict[j] = [1, 3, 4, 5, 6] #set new openings, and makes sensor cube or non sensor as set below.
            self.joints_dict[j] = [joint_made, str(joint_spot_from), str(j), "revolute", poss, "0 0 1"]
            if j in self.sensor_list:
                self.links_dict[j] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(j), [temp[0]/2, 0, 0], temp]
            else:
                self.links_dict[j] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(j), [temp[0]/2, 0, 0], temp]
        elif link_joint == 2:   
            self.open_spots_dict[j] = [2, 3, 4, 5, 6]
            self.joints_dict[j] = [joint_made, str(joint_spot_from), str(j), "revolute", poss, "0 0 1"]
            if j in self.sensor_list:
                self.links_dict[j] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(j), [-temp[0]/2, 0, 0], temp]
            else:
                self.links_dict[j] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(j), [-temp[0]/2, 0, 0], temp]
        elif link_joint == 3:
            self.open_spots_dict[j] = [1, 2, 3, 5, 6]
            self.joints_dict[j] = [joint_made, str(joint_spot_from), str(j), "revolute", poss, "1 0 1"]
            if j in self.sensor_list:
                self.links_dict[j] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(j), [0, temp[1]/2, 0], temp]
            else:
                self.links_dict[j] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(j), [0, temp[1]/2, 0], temp]
        elif link_joint == 4:
            self.open_spots_dict[j] = [1, 2, 4, 5, 6]
            self.joints_dict[j] = [joint_made, str(joint_spot_from), str(j), "revolute", poss, "1 0 1"]
            if j in self.sensor_list:
                self.links_dict[j] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(j), [0, -temp[1]/2, 0], temp]
            else:
                self.links_dict[j] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(j), [0, -temp[1]/2, 0], temp]
        elif link_joint == 5:
            self.open_spots_dict[j] = [1, 2, 3, 4, 5]
            self.joints_dict[j] = [joint_made, str(joint_spot_from), str(j), "revolute", poss, "1 1 0"]
            if j in self.sensor_list:
                self.links_dict[j] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(j), [0, 0, temp[2]/2], temp]
            else:
                self.links_dict[j] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(j), [0, 0, temp[2]/2], temp]
        elif link_joint == 6:
            self.open_spots_dict[j] = [1, 2, 3, 4, 6]
            self.joints_dict[j] = [joint_made, str(joint_spot_from), str(j), "revolute", poss, "1 1 0"]
            if j in self.sensor_list:
                self.links_dict[j] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(j), [0, 0, temp[2]/2], temp]
            else:
                self.links_dict[j] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(j), [0, 0, -temp[2]/2], temp]


    def Create_Body(self): #initial body creation, only called once.
        self.joints_list = [] #list of joint names
        self.sensor_list = [] # list of sensors
        self.block_list_dim_dict = {}  #dictionary of link sizes in xyz
        self.open_spots_dict = {} #dictionary storing open faces for each link
        self.links_dict = {}#dictionary storing link parameters
        self.joints_dict = {}#dictionary storing joint parameters
        self.outside_link = {}#dictionary recording if its an outside link or not
        self.blocks = random.randint(4, 8) #random number of links
        #self.blocks = 5
        self.linksmade = self.blocks
        for i in range(self.blocks):
            if i == 0:
                self.sensor_list.append(i)
            elif random.random() < .5:
                self.sensor_list.append(i) #randomize sensors
        self.sensor_num = len(self.sensor_list) #records number of sensors
        for i in range(self.blocks): #create randomized xyz for each link
            x_side = random.random()*.4+0.2 #not too small
            y_side = random.random()*.4+0.2
            z_side = random.random()*.4+0.2
            self.block_list_dim_dict[i] = [x_side, y_side, z_side]
        self.open_spots_dict[0] = [1, 2, 3, 4, 5] #dont allow -z direction so it doesn't go into the floor as often, every other side is possible
        link_joint = random.randint(1, 5) #pick random face for first link
        self.open_spots_dict[0].remove(link_joint) #remove from dictionary of open faces
        joint_made = str(0) + '_' + str(1) #title joint from parent and child
        self.joints_list.append(joint_made) #adds joints into joint_list
        varrr = self.block_list_dim_dict[0] #dimensions of first link
        temp1 = self.block_list_dim_dict[1] #dimensions of second link
        self.joints_dir[1] = link_joint #joint direction of first joint 
        self.collision[0] = [0, 0, 0] #relative position of first link
        self.outside_link[0] = False
        if 0 in self.sensor_list: #if first block is sensor, make green otherwise cyan
            self.links_dict[0] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(0), [0, 0, 1], varrr]
        else:
            self.links_dict[0] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(0), [0, 0, 1], varrr]
        if link_joint == 1: #if +x direction, create open spots without -x, set new block position to 1,0,0. Make joint and link.
            self.open_spots_dict[1] = [1, 3, 4, 5, 6]
            self.collision[1] = [1, 0, 0]
            self.joints_dict[1] = [str(0)+"_"+str(1), str(0), str(1), "revolute", [varrr[0]/2, 0, 1], "0 0 1"]
            if 1 in self.sensor_list:
                self.links_dict[1] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(1), [temp1[0]/2, 0, 0], temp1]
            else:
                self.links_dict[1] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(1), [temp1[0]/2, 0, 0], temp1]
        elif link_joint == 2:
            self.open_spots_dict[1] = [2, 3, 4, 5, 6]
            self.collision[1] = [-1, 0, 0]
            self.joints_dict[1] = [str(0)+"_"+str(1), str(0), str(1), "revolute", [-varrr[0]/2, 0, 1], "0 0 1"]
            if 1 in self.sensor_list:
                self.links_dict[1] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(1), [-temp1[0]/2, 0, 0], temp1]
            else:
                self.links_dict[1] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(1), [-temp1[0]/2, 0, 0], temp1]
        elif link_joint == 3:
            self.open_spots_dict[1] = [1, 2, 3, 5, 6]
            self.collision[1] = [0, 1, 0]
            self.joints_dict[1] = [str(0)+"_"+str(1), str(0), str(1), "revolute", [0, varrr[1]/2, 1], "1 0 1"]
            if 1 in self.sensor_list:
                self.links_dict[1] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(1), [0, temp1[1]/2, 0], temp1]
            else:
                self.links_dict[1] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(1), [0, temp1[1]/2, 0], temp1]

        elif link_joint == 4:
            self.open_spots_dict[1] = [1, 2, 4, 5, 6]
            self.collision[1] = [0, -1, 0]
            self.joints_dict[1] = [str(0)+"_"+str(1), str(0), str(1), "revolute", [0, -varrr[1]/2, 1], "1 0 1"]
            if 1 in self.sensor_list:
                self.links_dict[1] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(1), [0, -temp1[1]/2, 0], temp1]
            else:
                self.links_dict[1] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(1), [0, -temp1[1]/2, 0], temp1]
        elif link_joint == 5:
            self.open_spots_dict[1] = [1, 2, 3, 4, 5]
            self.collision[1] = [0, 0, 1]
            self.joints_dict[1] = [str(0)+"_"+str(1), str(0), str(1), "revolute", [0, 0, varrr[2]/2+1], "1 1 0"]
            if 1 in self.sensor_list:
                self.links_dict[1] = ['<material name="Green">', '    <color rgba="0 1.0 0.0 1.0"/>', str(1), [0, 0, temp1[2]/2], temp1]
            else:
                self.links_dict[1] = ['<material name="Cyan">', '    <color rgba="0 1.0 1.0 1.0"/>', str(1), [0, 0, temp1[2]/2], temp1]
        self.outside_link[1] = False
        for j in range(2,self.blocks): #for following joints and links
            self.add_joint_cube(j)

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
        self.weights = self.weights * 4 -1
        for currentRow in range(sensors):
            for currentColumn in range(motors):
                pyrosim.Send_Synapse(sourceNeuronName= currentRow, targetNeuronName= currentColumn + sensors, weight= self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Create_Future(self): #function called to activate pyrosim cubes and joints from two dictionaries.
        pyrosim.Start_URDF("body" + str(self.myID) + ".urdf")
        link_param = self.links_dict[0]
        pyrosim.Send_Cube(str1=link_param[0] , str2=link_param[1], name=link_param[2], pos=link_param[3] , size=link_param[4])
        for i in range(1, self.linksmade):
            joint_param = self.joints_dict[i]
            pyrosim.Send_Joint(name = joint_param[0], parent = joint_param[1], child = joint_param[2], type = joint_param[3], position = joint_param[4], jointAxis = joint_param[5])
            link_param = self.links_dict[i]
            pyrosim.Send_Cube(str1=link_param[0] , str2=link_param[1], name=link_param[2], pos=link_param[3] , size=link_param[4])
        pyrosim.End()
        
    def Update_Brain(self):#function to create brain after first call
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
        sensors = 0
        motors = 0
        for num in range(self.blocks):
            if num in self.sensor_list: #sensors based off links
                pyrosim.Send_Sensor_Neuron(name = sensors, linkName = str(num)) 
                sensors += 1
        for i in range(self.blocks, self.linksmade):
            pyrosim.Send_Sensor_Neuron(name = sensors, linkName = str(i))
            sensors += 1
        for i in range(self.blocks):
            if i < self.blocks - 1:    #motors based off joints
                pyrosim.Send_Motor_Neuron( name = sensors + motors , jointName = self.joints_list[i])
                motors += 1
        for i in range(self.blocks, self.linksmade):
            pyrosim.Send_Motor_Neuron(name = sensors + motors, jointName = self.joints_dict[i][0])
            motors += 1
        self.motor_num = motors
        self.weights = np.random.rand(sensors, motors)
        self.weights = self.weights * 4 -1
        for currentRow in range(sensors):
            for currentColumn in range(motors):
                pyrosim.Send_Synapse(sourceNeuronName= currentRow, targetNeuronName= currentColumn + sensors, weight= self.weights[currentRow, currentColumn])

        pyrosim.End()

    def Mutate(self):
        #print(self.linksmade)
        chance = random.randint(0, 1)
        if chance == 0:
            var_temp = False
            while var_temp == False:
                outside_link_spot = random.randint(2, self.linksmade-1)
                var_temp = self.outside_link[outside_link_spot]
            x_side = random.random()*.7+0.2
            y_side = random.random()*.7+0.2
            z_side = random.random()*.7+0.2
            self.block_list_dim_dict[self.linksmade] = [x_side, y_side, z_side]
            self.add_joint_cube(self.linksmade)
            self.linksmade += 1
        elif chance == 1:
            sensor = random.randint(0, self.sensor_num -1)
            motor = random.randint(0, self.motor_num-1)
            self.weights[sensor, motor] = random.random() * 2 - 1
        #pick outside link
        #delete link
        
    def SetID(self, id):
        self.myID = id