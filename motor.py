import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
    #    self.Prepare_To_Act()


    # def Prepare_To_Act(self):
    #     self.amplitude = c.Bamplitude
    #     self.frequency = c.Bfrequency
    #     self.offset = c.BphaseOffset
    #     print(self.jointName)
    #     if self.jointName == b'Torso_BackLeg':
    #         self.motorValues = np.sin((np.linspace(0, np.pi*2, c.iter)*self.frequency+self.offset))*self.amplitude
    #     else:
    #         self.motorValues = np.sin((np.linspace(0, np.pi*2, c.iter)*self.frequency*2+self.offset))*self.amplitude


    def Set_Value(self, desiredAngle, robotId):
        pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = desiredAngle, maxForce = 100)

  #  def Save_Values(self):
  #      np.save('storage_motor.npy', self.values)