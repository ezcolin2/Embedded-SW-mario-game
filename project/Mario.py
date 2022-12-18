
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

        if self.noHit!=0:#공격 당하고나면 잠시동안 무적
            self.noHit-=1
    
        if command['left_pressed']:
            self.right=False
        elif command['right_pressed']:
            self.right=True
        if self.isJumping: #위로 올라갈 때 (점프 중)

            for i in grounds:
                if self.isUnderGround(i): #머리가 부딪힌다면 
                    self.isDown=True
                    self.isJumping=False
                    res=[i.blockState,i.center] #블록 상태(아이템, 코인, 일반)와 center값을 리턴함 
                    #main에서 코인 블록 center값과 동일한 코인을 찾아서 그 코인을 보이게 하기 위함
                    i.blockState="normal" #아이템과 코인 블록의 경우 머리로 터치하면 일반 블록으로 바꿈
                    return res
            if  self.jumpCount<15: #점프는 총 15번 위로 움직임 
                
                self.jumpCount+=1
                self.position[1] -= 5
                self.position[3] -= 5
            else:
                self.isDown=True
                self.isJumping=False

        elif self.isDown: #아래로 내려갈 때 (점프 중)
            self.temp=0
            for i in grounds:
                if self.isOnGround(i): #내려오는 와중에 땅이 존재한다면 즉시 멈춰야 한다.
                #공중 땅에 착지할 때는 내려오는 중이고 jumpCount가 양수이기 때문에 이를 초기화시켜줘야 한다.
                    
                    self.isJumping = False
                    self.isDown = False
                    self.jumpCount=0
                    self.isOnGroundNum=self.temp #isOnGroundNum은 현재 올라와있는 땅의 인덱스를 의미한다.
                    
                self.temp+=1
            
            if self.jumpCount==0 and self.notGround(grounds[self.isOnGroundNum]):
                #jumpCount가 0이라는 뜻은 위로 올라간만큼 내려왔다는 뜻이다.
                #공중 땅에서 점프를 했는데 내려올 때 원래 있던 땅에 착지한 게 아니라면 조금 더 내려와야 한다.
                self.jumpCount+=(240-grounds[self.isOnGroundNum].position[3])/5
                #한 번에 5씩 움직이기 때문에 ground의 y좌표와 캐릭터의 y좌표의 차이를 5로 나누어주면 된다.
                self.isDown=True
                self.isJumping=False
                #break
            if self.jumpCount>0:
                self.jumpCount-=1
                self.position[1] += 5
                self.position[3] += 5
            else:
                self.isJumping=False
                self.isDown=False
        

        elif command['up_pressed']:
            self.isJumping=True
        if command['right_pressed']:
            #오른쪽으로 가고 있는데 땅이 없다면 isDown을 True로 만들어 내려갈 때(점프 중)상태를 만들어준다.
            #물론 jumpCount가 0이기 때문에 아래로 내려가지는 않는다.
            #이는 isOnGroundNum, 즉 현재 올라와 있는 땅의 번호를 갱신하기 위함이다.
            if self.notGround(grounds[self.isOnGroundNum]):
                self.isDown=True
        elif command['left_pressed']:
            if self.notGround(grounds[self.isOnGroundNum]):
                self.isDown=True


        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])


    
        