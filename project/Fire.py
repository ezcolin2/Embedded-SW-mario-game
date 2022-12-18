
import numpy as np

class Fire:
    def __init__(self, position,lastDirectionIsLeft):
        self.speed = 10
        self.position = np.array([position[0]-3, position[1]-3, position[0]+3, position[1]+3])
        self.direction = {'left' : False, 'right' : False}
        self.state = None
        if lastDirectionIsLeft:
            self.direction['left'] = True
        else:
            self.direction['right'] = True

        

    def move(self,command):

        if self.direction['left']:
            self.position[0] -= self.speed
            self.position[2] -= self.speed
            if command['left_pressed']: # 총알이 왼쪽 캐릭터가 왼쪽으로 움직이고 있다면 공격이 느리게 보여야 함
                self.position[0] += 5
                self.position[2] += 5
            elif command['right_pressed']: # 총알이 왼쪽 캐릭터가 오른쪽으로 움직이고 있다면 공격이 빠르게 보여야 함

                self.position[0] -= 5
                self.position[2] -= 5
            
        elif self.direction['right']:
            self.position[0] += self.speed
            self.position[2] += self.speed
            if command['right_pressed']: # 총알이 오른쪽 캐릭터가 오른쪽으로 움직이고 있다면 공격이 느리게 보여야 함
                self.position[0] -= 5
                self.position[2] -= 5
            elif command['left_pressed']: # 총알이 오른쪽 캐릭터가 왼쪽으로 움직이고 있다면 공격이 빠르게 보여야 함
                self.position[0] += 5
                self.position[2] += 5

            
    def hit(self, monsters):
        for monster in monsters:
            collision = self.overlap(self.position, monster.position)
            
            if collision:
                monster.state = 'dead'
                self.state = 'hit'
                return True
    def hitBoss(self, boss):
        if self.overlap(self.position,boss.position):
            boss.hp-=1
            return True

    def overlap(self, ego_position, other_position):
        '''
        두개의 사각형(bullet position, monster position)이 겹치는지 확인하는 함수
        좌표 표현 : [x1, y1, x2, y2]
        
        return :
            True : if overlap
            False : if not overlap
        '''
        return ego_position[0] > other_position[0] and ego_position[1] > other_position[1] \
                 and ego_position[2] < other_position[2] and ego_position[3] < other_position[3]