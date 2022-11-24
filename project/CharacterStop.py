
import numpy as np

class CharacterStop:
    jumpCount=0
    state = "normal"
    #0:빨, 1:갈, 2:노
    arrRed=[[-4,-7,3,-6],[-5,-6,5,-5],[-4,0,2,1],[-5,1,5,2],[-6,2,-2,3],[2,2,6,3]]
    arrYellow=[[-2,-5,3,-4],[-3,-4,1,-3],[2,-4,5,-3],[-2,-3,6,-2],[-4,-2,1,-1],[-3,-1,4,0]]
    arrBrown=[[-5,-5,-2,-4],[-6,-4,-3,-3],[1,-4,2,-3],[-6,-3,-2,-2],[-6,-2,-4,-1],[1,-2,4,-1],[-2,2,2,3]]
    def __init__(self, width, height):
        self.right=True
        self.isJumping = False
        self.isDown = False
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        # 총알 발사를 위한 캐릭터 중앙 점 추가
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"
        self.firstHeight = self.center[1]
        self.jumpHeight = 50
        self.isOn=False # 현재 땅을 밟고 있으면 True 
        self.isOnGroundNum = 0 # 현재 밟고 있는 땅의 번호 
    def isOnGround(self, ground): #땅을 밟고 섬 
        if(self.position[3]==ground.position[1] and ground.position[0]<self.center[0]<ground.position[2]):
            return True
        return False
    def notGround(self, ground): #height는 땅과 같지만 width가 다름
        if(self.position[3]==ground.position[1] and (ground.position[0]>self.center[0]or self.center[0]>ground.position[2])):
            return True
        return False
    def isUnderGround(self, ground): #땅에 머리 부딪힘
        if(self.position[1]<=ground.position[3] and self.position[1]>=ground.position[1] and self.center[0]>=ground.position[0] and self.center[0]<=ground.position[2]):
            return True
        return False

    def isOnItem(self,item): #아이템과 충돌
        #캐릭터의 x축 중앙이 item사이에 있고 캐릭터의 발이 item 사이에 있을 때 
        if(item.position[0]<=self.center[0]<=item.position[2] and item.position[1]<=self.position[3]<=item.position[3]):

            self.state="item"
            item.visible=False
        #self.state="item"
    def move(self, command = None, grounds = None):
    
        
        if self.isJumping:

            for i in grounds:
                if self.isUnderGround(i): #머리가 부딪힌다면 
                    self.isDown=True
                    self.isJumping=False
                    if i.blockState=="item":
                        return True
            if  self.jumpCount<15:
                
                self.jumpCount+=1
                self.position[1] -= 5
                self.position[3] -= 5
            else:
                self.isDown=True
                self.isJumping=False

        elif self.isDown:
            self.temp=0
            for i in grounds:
                if self.isOnGround(i) and self.jumpCount!=0:
                    self.isJumping = False
                    self.isDown = False
                    self.jumpCount=0
                    self.isOn=True
                    self.isOnGroundNum=self.temp
                    break
                self.temp+=1
            print(self.isOnGroundNum,self.isOn,self.jumpCount)
            #for i in grounds:
            if self.isOn and self.jumpCount==0 and self.notGround(grounds[self.isOnGroundNum]):
                #땅에 한 번 올라간 상태에 땅에 닿아있는 상태일 때
                self.jumpCount+=(grounds[self.isOnGroundNum].position[3]-self.position[1])/5
                #한 번에 5씩 움직이기 때문에 ground의 y좌표와 캐릭터의 y좌표의 차이를 5로 나누어주면 된다. 
                self.isOn=False
                self.isDown=True
                self.isJumping=False
                #break
            if self.jumpCount>0:
                self.jumpCount-=1
                self.position[1] += 5
                self.position[3] += 5
                #여기서 땅에 닿으면 초기화시키는 코드 추가 
            else:
                self.isJumping=False
                self.isDown=False
            #self.isOnGroundNum=0
        



        elif command['up_pressed']:
            self.isJumping=True
        if command['right_pressed']:
            if self.notGround(grounds[self.isOnGroundNum]):
                self.isDown=True
        elif command['left_pressed']:
            if self.notGround(grounds[self.isOnGroundNum]):
                self.isDown=True


        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])

    def jumpStart(self):
        self.isJumping=True 

    
        