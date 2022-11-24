
import numpy as np

class Fire:
    def __init__(self, position,lastDirectionIsLeft):
        self.appearance = 'rectangle'
        self.speed = 10
        self.damage = 10
        self.position = np.array([position[0]-3, position[1]-3, position[0]+3, position[1]+3])
        self.direction = {'left' : False, 'right' : False}
        self.state = None
        self.outline = "#0000FF"
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

            
    def collision_check(self, enemys):
        for enemy in enemys:
            collision = self.overlap(self.position, enemy.position)
            
            if collision:
                enemy.state = 'die'
                self.state = 'hit'

    def overlap(self, ego_position, other_position):
        '''
        두개의 사각형(bullet position, enemy position)이 겹치는지 확인하는 함수
        좌표 표현 : [x1, y1, x2, y2]
        
        return :
            True : if overlap
            False : if not overlap
        '''
        return ego_position[0] > other_position[0] and ego_position[1] > other_position[1] \
                 and ego_position[2] < other_position[2] and ego_position[3] < other_position[3]