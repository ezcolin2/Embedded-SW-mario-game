
import numpy as np
import random

class Boss:
    arrBrown = [[-4,-6,4,-5],[-5,-5,5,-4],[-6,-4,6,-3],[-7,-3,-4,-2],[-1,-3,1,-2],
    [4,-3,7,-2],[-7,-2,-4,-1],[-1,-2,1,-1],[4,-2,7,-1],[-8,-1,-4,0],[-1,-1,1,0],
    [4,-1,8,0],[-8,0,-4,1],[-1,0,1,1],[-8,1,8,3]]
    arrWhite =[[-4,-3,-1,-1,],[1,-3,4,-1],[-4,-1,-3,0],[-2,-1,-1,0],[1,-1,2,0],[3,-1,4,0],[-4,0,-1,1],[1,0,4,1]]
    arrBlack = [[-3,-1,-2,0],[2,-1,3,0],[-5,4,-3,5],[-5,5,-2,6],[2,5,7,6],[-5,6,-1,7],
    [1,6,7,7],[-3,7,-1,8],[1,7,6,8]]
    arrSkin = [[-4,3,4,4],[-3,4,3,5],[-2,5,2,6]]
    
    def __init__(self, spawn_position):
        self.isJumping=True
        self.isDown=False

        self.jumpCount=0
        self.hp = 10
        self.state = 'alive'
        self.position = np.array([spawn_position[0] - 25, spawn_position[1] - 25, spawn_position[0] + 25, spawn_position[1] + 25])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.size = 3

    def move(self, command):
        self.direction = random.randrange(0,2)

        if command['left_pressed']:
            self.position[0]+=5
            self.position[2]+=5

            self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        elif command['right_pressed']:
            self.position[0]-=5
            self.position[2]-=5
            self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        if self.isJumping==True:
            self.jumpCount+=1
            self.position[1]-=10
            self.position[3]-=10
            self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
            if self.jumpCount==20:
                self.isJumping=False
                self.isDown=True
        if self.isDown==True:
            self.jumpCount-=1
            self.position[1]+=10
            self.position[3]+=10
            self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
            if self.jumpCount==0:
                self.isJumping=True
                self.isDown=False



