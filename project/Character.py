import numpy as np

class Character:
    jumpCount=0
    def __init__(self, width, height):
        self.isJumping = False
        self.isDown = False
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        # 총알 발사를 위한 캐릭터 중앙 점 추가
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"

    def move(self, command = None):
        
        if self.isJumping:
            if  self.jumpCount<10:
                self.jumpCount+=1
                self.position[1] -= 5
                self.position[3] -= 5
            else:
                self.isDown=True
                self.isJumping=False

        elif self.isDown:
            if self.jumpCount>0:
                self.jumpCount-=1
                self.position[1] += 3
                self.position[3] += 3
                #여기서 땅에 닿으면 초기화시키는 코드 추가 
            else:
                self.isJumping=False
                self.isDown=False
        elif command['up_pressed']:
            self.isJumping=True

        if command['left_pressed']:
            self.position[0] -= 5
            self.position[2] -= 5
            
        if command['right_pressed']:
            self.position[0] += 5
            self.position[2] += 5
                
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
