
import numpy as np

class Mario:
    jumpCount=0
    state = "normal"
    #0:빨, 1:갈, 2:노
    arrRed=[[-4,-7,3,-6],[-5,-6,5,-5],[-4,0,2,1],[-5,1,5,2],[-6,2,-2,3],[2,2,6,3],[-2,3,-1,4],[1,3,2,4]]
    arrYellow=[[-2,-5,3,-4],[-3,-4,1,-3],[2,-4,5,-3],[-2,-3,6,-2],[-4,-2,1,-1],[-3,-1,4,0],[-6,3,-4,4],[4,3,6,4],[-6,4,-3,5],[3,4,6,5],[-6,5,-4,6],[4,5,6,6]]
    arrBrown=[[-5,-5,-2,-4],[-6,-4,-3,-3],[1,-4,2,-3],[-6,-3,-2,-2],[-6,-2,-4,-1],[1,-2,4,-1],[-2,2,2,3],[-4,3,-2,4],[-1,3,1,4],[2,3,4,4],[-3,4,3,5],[-4,5,4,6],[-4,6,-1,7],[1,6,4,7],[-5,7,-2,8],[2,7,5,8],[-6,8,-2,9],[2,8,6,9]]
    def __init__(self, width, height):
        self.size = 2 # 마리오의 크기 아이템 먹으면 커짐 
        self.noHit = 0 #아이템 먹고 공격당하면 잠깐 동안 무적 
        self.right=True
        self.isJumping = False
        self.isDown = False
        self.state = "normal"
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        # 총알 발사를 위한 캐릭터 중앙 점 추가
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.firstHeight = self.center[1]
        self.jumpHeight = 50
        self.isOn=False # 현재 땅을 밟고 있으면 True 
        self.isOnGroundNum = 0 # 현재 밟고 있는 땅의 번호 
    def isOnGround(self, ground): #땅을 밟고 섬 
        return self.position[3]==ground.position[1] and ground.position[0]<self.center[0]<ground.position[2]
    def notGround(self, ground): #height는 땅과 같지만 width가 다름
        return self.position[3]==ground.position[1] and (ground.position[0]>self.center[0]or self.center[0]>ground.position[2])
    def isUnderGround(self, ground): #땅에 머리 부딪힘

        return ground.position[1]<=self.position[1]<=ground.position[3]  and ground.position[0]<=self.center[0]<=ground.position[2]
            

    def isOnMonster(self,monster): #몬스터를 밟으면 true 
        return    (
            monster.position[0]<=self.center[0]<=monster.position[2] and monster.position[1]<=self.position[3]<=monster.center[1]
        )
    
    def hitted(self,monster) : #monster에 닿으면 true
        return(
            monster.position[0]<=self.center[0]<=monster.position[2] and self.position[3]>monster.center[1]

        )
    def sHitted(self,stone) : #stone에 닿으면 true
        return(
            stone.position[0]<=self.center[0]<=stone.position[2] and self.position[1]<=stone.position[3]<=self.position[3]
        )

    def monsterHitted(self,monster) : #monster에 닿았을 때 동작할 것 
        if self.isOnMonster(monster): #monster를 밟으면 몬스터가 죽음 
            monster.state="dead"
        elif self.hitted(monster) : #monster에 적았을 때
            if self.state=="item": #아이템을 먹은 상태라면 안 먹은 상태로 바꾸고 잠깐동안 무적
                self.size=2
                self.state="normal"
                self.noHit=20
            elif self.noHit==0: #아이템을 안 먹은 상태이고 무적이 아니라면 
                self.state="dead"
    def stoneHitted(self,stone):
        if self.sHitted(stone):
            if self.state=="item": #아이템을 먹은 상태라면 안 먹은 상태로 바꾸고 잠깐동안 무적
                self.size=2
                self.state="normal"
                self.noHit=20
            elif self.noHit==0: #아이템을 안 먹은 상태이고 무적이 아니라면 
                self.state="dead"

    def isOnTrap(self,trap):# trap을 밟았다면 true 아니면 false
        return    (
            trap.position[0]<=self.center[0]<=trap.position[2] and trap.position[1]<=self.position[3]<=trap.center[1]
        )

    def onTrap(self,trap) : #trap을 밟았을 때 동작
        if self.isOnTrap(trap):
            if self.state=="item": #아이템을 먹은 상태라면 안 먹은 상태로 바꾸고 잠깐동안 무적
                    self.size=2
                    self.state="normal"
                    self.noHit=20
            elif self.noHit==0: #아이템을 안 먹은 상태이고 무적이 아니라면 
                self.state="dead"

    def die(self):
        print("hello")
        return True
    def isOnItem(self,item): #아이템과 충돌
        #캐릭터의 x축 중앙이 item사이에 있고 캐릭터의 발이 item 사이에 있고 item이 보이는 상태 
        if(item.visible and item.position[0]<=self.center[0]<=item.position[2] and item.position[1]<=self.position[3]<=item.position[3]):

            self.state="item"
            self.size = 3
            item.visible=False
        #self.state="item"
    def isOnCoin(self,coin,command): #코인과 충돌하면 점수 증가 
        #캐릭터의 x축 중앙이 item사이에 있고 캐릭터의 발이 item 사이에 있고 item이 보이는 상태에 A를 눌렀을때 
        if(command['a_pressed'] and coin.visible and coin.position[0]<=self.center[0]<=coin.position[2] and coin.position[1]<=self.position[3]<=coin.position[3]):
            
            coin.visible = False
            return True


    def move(self, command = None, grounds = None):

        if self.noHit!=0:
            self.noHit-=1
    
        if command['left_pressed']:
            self.right=False
        elif command['right_pressed']:
            self.right=True
        if self.isJumping:

            for i in grounds:
                if self.isUnderGround(i): #머리가 부딪힌다면 
                    self.isDown=True
                    self.isJumping=False
                    res=[i.blockState,i.center]
                    i.blockState="normal"
                    return res
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
                if self.isOnGround(i): # 원래 추가 조건이 jumpCount!=0 이고 break가 있었음 
                    self.isJumping = False
                    self.isDown = False
                    self.jumpCount=0
                    self.isOn=True
                    self.isOnGroundNum=self.temp
                    
                self.temp+=1
            print(self.isOnGroundNum,self.isOn,self.jumpCount)
            #for i in grounds:
            if self.isOn and self.jumpCount==0 and self.notGround(grounds[self.isOnGroundNum]):
                #땅에 한 번 올라간 상태에 땅에 닿아있는 상태일 때
                self.jumpCount+=(240-grounds[self.isOnGroundNum].position[3])/5
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

    
        