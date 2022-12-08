import numpy as np
import random

class Stone:

    def __init__(self, spawn_position):
        self.position = np.array([spawn_position[0] - 10, spawn_position[1] - 10, spawn_position[0] + 10, spawn_position[1] + 10])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.change = True #돌 위치 바꿈 
    def changeStone(self):
        if self.change:
            self.position[0]+=20
            self.position[2]+=20
            
        else:
            self.position[0]-=20
            self.position[2]-=20

    def move(self,command):
        

        if command['left_pressed']:
            self.position[0]+=5
            self.position[2]+=5

        elif command['right_pressed']:
            self.position[0]-=5
            self.position[2]-=5
        self.position[1]+=10
        self.position[3]+=10
        if self.position[1] >= 240:
            self.position[1]=0
            self.position[3]=20
            self.change = False if self.change else True
            self.changeStone()


        

